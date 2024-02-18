import logging
from homeassistant.components.select import SelectEntity

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    DEVICE_TYPE_AC,
    DEVICE_TYPE_DEHUMIDIFIER,
    DEVICE_TYPE_PURIFIER,
    DATA_CLIENT,
    DATA_COORDINATOR,
    LABEL_DEHUMIDIFIER_FAN_MODE,
    LABEL_PURIFIER_FAN_LEVEL,
    LABEL_CLIMATE_FAN_POSITION,
    LABEL_CLIMATE_MOTION_DETECTION,
    LABEL_CLIMATE_INDICATOR,
    ICON_FAN,
    ICON_LIGHT,
    ICON_MOTION_SENSOR,
)

_LOGGER = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    commands = client.get_commands()
    select = []

    for index, device in enumerate(devices):
        device_type = int(device.get("DeviceType"))
        current_device_commands = [
            command
            for command in commands
            if command["ModelType"] == device.get("ModelType")
        ][0]["JSON"][0]["list"]
        command_types = list(
            map(lambda c: c["CommandType"].lower(), current_device_commands)
        )

        if device_type == DEVICE_TYPE_DEHUMIDIFIER:

            if "0x0E" in command_types:
                select.append(
                    PanasonoicDehumidifierFanModeSelect(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )

        if device_type == DEVICE_TYPE_AC:

            if "0x19" in command_types:
                select.append(
                    PanasonoicACMotionDetection(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )
            if "0x1f" in command_types:
                select.append(
                    PanasonoicACIndicatorLightSelect(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )

        if device_type == DEVICE_TYPE_PURIFIER:
            if "0x01" in command_types:
                select.append(
                    PanasonoicPurifierFanLevelSelect(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )

    async_add_entities(select, True)

    return True


class PanasonoicDehumidifierFanModeSelect(PanasonicBaseEntity, SelectEntity):
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
            await self.client.set_command(self.auth, 142, target_option[0][1])
            await self.coordinator.async_request_refresh()
        else:
            return


class PanasonoicACMotionDetection(PanasonicBaseEntity, SelectEntity):
    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_CLIMATE_MOTION_DETECTION}"

    @property
    def icon(self) -> str:
        return ICON_MOTION_SENSOR

    @property
    def options(self) -> list:
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x19", self.commands)
        )[0]["Parameters"]

        def mode_extractor(mode):
            return mode[0]

        mode_list = list(map(mode_extractor, raw_mode_list))
        return mode_list

    @property
    def current_option(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x19", self.commands)
        )[0]["Parameters"]
        target_option = list(
            filter(lambda m: m[1] == int(status.get("0x19") or 0), raw_mode_list)
        )[0]
        _current_option = target_option[0] if len(target_option) > 0 else ""
        _LOGGER.debug(f"[{self.label}] current_option: {_current_option}")
        return _current_option

    async def async_select_option(self, option: str) -> None:
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x19", self.commands)
        )[0]["Parameters"]
        target_option = list(filter(lambda m: m[0] == option, raw_mode_list))
        if len(target_option) > 0:
            _LOGGER.debug(f"[{self.label}] Set motion detection to {option}")
            await self.client.set_command(self.auth, 153, target_option[0][1])
            await self.coordinator.async_request_refresh()
        else:
            return


class PanasonoicACIndicatorLightSelect(PanasonicBaseEntity, SelectEntity):
    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_CLIMATE_INDICATOR}"

    @property
    def icon(self) -> str:
        return ICON_LIGHT

    @property
    def options(self) -> list:
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x1f", self.commands)
        )[0]["Parameters"]

        def mode_extractor(mode):
            return mode[0]

        mode_list = list(map(mode_extractor, raw_mode_list))
        return mode_list

    @property
    def current_option(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x1f", self.commands)
        )[0]["Parameters"]
        target_option = list(
            filter(lambda m: m[1] == int(status.get("0x1F") or 0), raw_mode_list)
        )[0]
        _current_option = target_option[0] if len(target_option) > 0 else ""
        _LOGGER.debug(f"[{self.label}] current_option: {_current_option}")
        return _current_option

    async def async_select_option(self, option: str) -> None:
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x1f", self.commands)
        )[0]["Parameters"]
        _LOGGER.debug(raw_mode_list)
        target_option = list(filter(lambda m: m[0] == option, raw_mode_list))
        if len(target_option) > 0:
            _LOGGER.debug(f"[{self.label}] Set motion detection to {option}")
            await self.client.set_command(self.auth, 159, target_option[0][1])
            await self.coordinator.async_request_refresh()
        else:
            return


class PanasonoicPurifierFanLevelSelect(PanasonicBaseEntity, SelectEntity):
    _attr_has_entity_name = True

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self) -> str:
        return LABEL_PURIFIER_FAN_LEVEL

    @property
    def icon(self) -> str:
        return ICON_FAN

    @property
    def options(self) -> list:
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x01", self.commands)
        )[0]["Parameters"]

        def mode_extractor(mode):
            return mode[0]

        mode_list = list(map(mode_extractor, raw_mode_list))
        return mode_list

    @property
    def current_option(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x01", self.commands)
        )[0]["Parameters"]
        target_option = list(
            filter(lambda m: m[1] == int(status.get("0x01") or 0), raw_mode_list)
        )[0]
        _current_option = target_option[0] if len(target_option) > 0 else ""
        _LOGGER.debug(f"[{self.label}] current_option: {_current_option}")
        return _current_option

    async def async_select_option(self, option: str) -> None:
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x01", self.commands)
        )[0]["Parameters"]
        target_option = list(filter(lambda m: m[0] == option, raw_mode_list))
        if len(target_option) > 0:
            _LOGGER.debug(f"[{self.label}] Set fan mode to {option}")
            await self.client.set_command(self.auth, 129, target_option[0][1])
            await self.coordinator.async_request_refresh()
        else:
            return
