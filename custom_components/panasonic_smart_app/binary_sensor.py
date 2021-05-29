from datetime import timedelta
import logging
from homeassistant.components.binary_sensor import BinarySensorEntity

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    UPDATE_INTERVAL,
    DEVICE_TYPE_DEHUMIDIFIER,
    DATA_CLIENT,
    DATA_COORDINATOR,
    LABEL_TANK,
    ICON_TANK,
)

_LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(seconds=UPDATE_INTERVAL)


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    sensors = []

    for device in devices:
        if int(device["Devices"][0]["DeviceType"]) == DEVICE_TYPE_DEHUMIDIFIER:
            sensors.append(
                PanasonoicTankSensor(
                    client,
                    device,
                )
            )

    async_add_entities(sensors, True)

    return True


class PanasonoicTankSensor(PanasonicBaseEntity, BinarySensorEntity):
    async def async_update(self):
        _LOGGER.debug(f"------- UPDATING {self.nickname} {self.label} -------")
        try:
            self._status = await self.client.get_device_info(
                self.auth,
                options=["0x0a"],
            )

        except:
            _LOGGER.error(f"[{self.nickname}] Error occured while updating status")
        else:
            self._is_tank_full = bool(int(self._status.get("0x0a")))
            _LOGGER.debug(f"[{self.nickname}] _is_tank_full: {self._is_tank_full}")

    @property
    def label(self) -> str:
        return LABEL_TANK

    @property
    def icon(self) -> str:
        return ICON_TANK

    @property
    def is_on(self) -> bool:
        return self._is_tank_full
