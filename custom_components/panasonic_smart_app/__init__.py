import asyncio
import async_timeout
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .smartApp import SmartApp
from .const import (
    DATA_CLIENT,
    DATA_COORDINATOR,
    DOMAIN,
    DEFAULT_NAME,
    PLATFORMS,
    UPDATE_INTERVAL,
    DEVICE_STATUS_CODES,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)
    session = async_get_clientsession(hass)
    client = SmartApp(session, username, password)

    _LOGGER.info(
        "\n\
      Loading your Panasonic devices. This may takes few minutes to complete.\n\
    "
    )
    await client.login()

    def chunks(L, n): return [L[x: x+n] for x in range(0, len(L), n)]

    async def async_update_data():
        try:
            _LOGGER.info("Updating device info...")
            devices = await client.get_devices()
            for device in devices:
                device_type = int(device.get("DeviceType"))
                if device_type in DEVICE_STATUS_CODES.keys():
                    status_codes = chunks(DEVICE_STATUS_CODES[device_type], 6)
                    device["status"] = {}
                    for codes in status_codes:
                        device["status"].update(
                            await client.get_device_info(
                                device.get("Auth"),
                                codes
                            )
                        )
            return devices
        except BaseException as ex:
            _LOGGER.error(ex)
            raise UpdateFailed("Failed on initialize")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DEFAULT_NAME,
        update_method=async_update_data,
        update_interval=timedelta(seconds=UPDATE_INTERVAL),
    )

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: client,
        DATA_COORDINATOR: coordinator,
    }

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
