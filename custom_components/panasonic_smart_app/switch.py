from datetime import timedelta
import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_UNAVAILABLE

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    DEVICE_TYPE_AC,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DEVICE_CLASS_SWITCH,
    LABEL_NANOE,
    LABEL_ECONAVI,
    LABEL_BUZZER,
    LABEL_TURBO,
    LABEL_CLIMATE_DRYER,
    LABEL_CLIMATE_SLEEP,
    LABEL_CLIMATE_CLEAN,
    ICON_NANOE,
    ICON_ECONAVI,
    ICON_BUZZER,
    ICON_TURBO,
    ICON_SLEEP,
    ICON_DRYER,
    ICON_CLEAN,
)

_LOGGER = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    commands = client.get_commands()
    switches = []

    for index, device in enumerate(devices):
        device_type = int(device.get("DeviceType"))
        current_device_commands = [
            command
            for command in commands
            if command["ModelType"] == device.get("ModelType")
        ][0]["JSON"][0]["list"]
        command_types = list(map(lambda c: c["CommandType"].lower(), current_device_commands))

        if device_type == DEVICE_TYPE_AC:

            if "0x08" in command_types:
                switches.append(
                    PanasonicACNanoe(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )
            if "0x1b" in command_types:
                switches.append(
                    PanasonicACEconavi(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )
            if "0x1e" in command_types:
                switches.append(
                    PanasonicACBuzzer(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )
            if "0x1a" in command_types:
                switches.append(
                    PanasonicACTurbo(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )
            if "0x05" in command_types:
                switches.append(
                    PanasonicACSleepMode(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )
            if "0x17" in command_types:
                switches.append(
                    PanasonicACDryer(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )
            if "0x18" in command_types:
                switches.append(
                    PanasonicACSelfClean(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )

    async_add_entities(switches, True)

    return True


class PanasonicACNanoe(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic AC nanoe switch """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_NANOE}"

    @property
    def icon(self) -> str:
        return ICON_NANOE

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _nanoe_status = status.get("0x08")
        if _nanoe_status == None:
            return STATE_UNAVAILABLE
        _is_on = bool(int(_nanoe_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on nanoe")
        await self.client.set_command(self.auth, 136, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off nanoe")
        await self.client.set_command(self.auth, 136, 0)
        await self.coordinator.async_request_refresh()


class PanasonicACEconavi(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic AC ECONAVI switch """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_ECONAVI}"

    @property
    def icon(self) -> str:
        return ICON_ECONAVI

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _nanoe_status = status.get("0x1b")
        if _nanoe_status == None:
            return STATE_UNAVAILABLE
        _is_on = bool(int(_nanoe_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on ECONAVI")
        await self.client.set_command(self.auth, 155, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off ECONAVI")
        await self.client.set_command(self.auth, 155, 0)
        await self.coordinator.async_request_refresh()


class PanasonicACBuzzer(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic AC buzzer switch """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_BUZZER}"

    @property
    def icon(self) -> str:
        return ICON_BUZZER

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _buzzer_status = status.get("0x1E")
        if _buzzer_status == None:
            return STATE_UNAVAILABLE
        _is_on = not bool(int(_buzzer_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on buzzer")
        await self.client.set_command(self.auth, 30, 0)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off buzzer")
        await self.client.set_command(self.auth, 30, 1)
        await self.coordinator.async_request_refresh()


class PanasonicACTurbo(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic AC turbo switch """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_TURBO}"

    @property
    def icon(self) -> str:
        return ICON_TURBO

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _turbo_status = status.get("0x1a", None)
        if _turbo_status == None:
            return STATE_UNAVAILABLE
        _is_on = bool(int(_turbo_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on turbo mode")
        await self.client.set_command(self.auth, 154, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off turbo mode")
        await self.client.set_command(self.auth, 154, 0)
        await self.coordinator.async_request_refresh()


class PanasonicACSleepMode(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic AC sleep mode switch """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_CLIMATE_SLEEP}"

    @property
    def icon(self) -> str:
        return ICON_SLEEP

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _sleep_mode_status = status.get("0x05")
        if _sleep_mode_status == None:
            return STATE_UNAVAILABLE
        _is_on = bool(int(_sleep_mode_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on sleep mode")
        await self.client.set_command(self.auth, 5, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off sleep mode")
        await self.client.set_command(self.auth, 5, 0)
        await self.coordinator.async_request_refresh()


class PanasonicACDryer(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic AC dryer switch """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_CLIMATE_DRYER}"

    @property
    def icon(self) -> str:
        return ICON_DRYER

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _dryer_status = status.get("0x17")
        if _dryer_status == None:
            return STATE_UNAVAILABLE
        _is_on = bool(int(_dryer_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on dryer")
        await self.client.set_command(self.auth, 23, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off dryer")
        await self.client.set_command(self.auth, 23, 0)
        await self.coordinator.async_request_refresh()


class PanasonicACSelfClean(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic AC self clean switch """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_CLIMATE_CLEAN}"

    @property
    def icon(self) -> str:
        return ICON_CLEAN

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _self_clean_status = status.get("0x18")
        if _self_clean_status == None:
            return STATE_UNAVAILABLE
        _is_on = bool(int(_self_clean_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on self clean")
        await self.client.set_command(self.auth, 24, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off self clean")
        await self.client.set_command(self.auth, 24, 0)
        await self.coordinator.async_request_refresh()
