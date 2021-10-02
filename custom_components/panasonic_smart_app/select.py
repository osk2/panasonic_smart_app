from datetime import timedelta
import logging
from homeassistant.components.select import SelectEntity

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    DEVICE_TYPE_DEHUMIDIFIER,
    DATA_CLIENT,
    DATA_COORDINATOR,
    LABEL_DEHUMIDIFIER_FAN_MODE,
    ICON_FAN,
)

_LOGGER = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    sensors = []

    for index, device in enumerate(devices):
        if int(device.get("DeviceType")) == DEVICE_TYPE_DEHUMIDIFIER:
            sensors.append(
                PanasonoicFanModeSensor(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )

    async_add_entities(sensors, True)

    return True


class PanasonoicFanModeSensor(PanasonicBaseEntity, SelectEntity):
    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_DEHUMIDIFIER_FAN_MODE}"

    @property
    def icon(self) -> str:
        return ICON_FAN

    @property
    def options(self) -> list:
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x0E", self.commands)
        )[0]["Parameters"]

        def mode_extractor(mode):
            return mode[0]

        mode_list = list(map(mode_extractor, raw_mode_list))
        return mode_list

    @property
    def current_option(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x0E", self.commands)
        )[0]["Parameters"]
        target_option = list(
            filter(lambda m: m[1] == int(status.get("0x0E") or 0), raw_mode_list)
        )[0]
        _current_option = target_option[0] if len(target_option) > 0 else ""
        _LOGGER.debug(f"[{self.label}] current_option: {_current_option}")
        return _current_option

    async def async_select_option(self, option: str) -> None:
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x0E", self.commands)
        )[0]["Parameters"]
        target_option = list(filter(lambda m: m[0] == option, raw_mode_list))
        if len(target_option) > 0:
            _LOGGER.debug(f"[{self.label}] Set fan mode to {option}")
            await self.client.set_command(self.auth, 142, target_option[0])
            await self.coordinator.async_request_refresh()
        else:
            return
