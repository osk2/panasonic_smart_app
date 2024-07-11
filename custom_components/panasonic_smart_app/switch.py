from datetime import timedelta
import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_UNAVAILABLE

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    DEVICE_TYPE_AC,
    DEVICE_TYPE_DEHUMIDIFIER,
    DEVICE_TYPE_PURIFIER,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DEVICE_CLASS_SWITCH,
    LABEL_NANOE,
    LABEL_NANOEX,
    LABEL_ECONAVI,
    LABEL_BUZZER,
    LABEL_TURBO,
    LABEL_CLIMATE_MOLD_PREVENTION,
    LABEL_CLIMATE_SLEEP,
    LABEL_CLIMATE_CLEAN,
    LABEL_POWER,
    LABEL_DEHUMIDIFIER_BUZZER,
    ICON_TANK,
    ICON_NANOE,
    ICON_NANOEX,
    ICON_ECONAVI,
    ICON_BUZZER,
    ICON_TURBO,
    ICON_SLEEP,
    ICON_MOLD_PREVENTION,
    ICON_CLEAN,
    ICON_PURIFIER,
    ICON_BUZZER,
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
        command_types = list(
            map(lambda c: c["CommandType"].lower(), current_device_commands)
        )

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
                    PanasonicACMoldPrevention(
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

        if device_type == DEVICE_TYPE_PURIFIER:
            if "0x00" in command_types:
                switches.append(
                    PanasonicPurifierPower(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )
            if "0x07" in command_types:
                switches.append(
                    PanasonicPurifierNanoeX(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )

        if device_type == DEVICE_TYPE_DEHUMIDIFIER:
            if "0x0d" in command_types:
                switches.append(
                    PanasonicDehumidifierNanoeX(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )

            if "0x00" in command_types:
                switches.append(
                    PanasonicDehumidifierPower(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )

            if "0x18" in command_types:
                switches.append(
                    PanasonicDehumidifierBuzzer(
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
        _nanoe_status = status.get("0x1B")
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
        _turbo_status = status.get("0x1A", None)
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


class PanasonicACMoldPrevention(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic AC mold prevention switch """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_CLIMATE_MOLD_PREVENTION}"

    @property
    def icon(self) -> str:
        return ICON_MOLD_PREVENTION

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _mold_prevention_status = status.get("0x17")
        if _mold_prevention_status == None:
            return STATE_UNAVAILABLE
        _is_on = bool(int(_mold_prevention_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on mold prevention")
        await self.client.set_command(self.auth, 23, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off mold prevention")
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


class PanasonicPurifierPower(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic Purifier power """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        return status.get("0x00", None) != None

    @property
    def label(self):
        return LABEL_POWER

    @property
    def icon(self) -> str:
        return ICON_PURIFIER

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _power_status = status.get("0x00")
        if _power_status == None:
            return STATE_UNAVAILABLE
        _is_on = bool(int(_power_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on nanoeX")
        await self.client.set_command(self.auth, 128, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off nanoeX")
        await self.client.set_command(self.auth, 128, 0)
        await self.coordinator.async_request_refresh()



class PanasonicPurifierNanoeX(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic Purifier nanoeX switch """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_NANOEX}"

    @property
    def icon(self) -> str:
        return ICON_NANOEX

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _nanoe_status = status.get("0x07")
        if _nanoe_status == None:
            return STATE_UNAVAILABLE
        _is_on = bool(int(_nanoe_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on nanoeX")
        await self.client.set_command(self.auth, 135, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off nanoeX")
        await self.client.set_command(self.auth, 135, 0)
        await self.coordinator.async_request_refresh()

class PanasonicDehumidifierNanoeX(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic Dehumidifier nanoeX switch """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_NANOEX}"

    @property
    def icon(self) -> str:
        return ICON_NANOEX

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _nanoe_status = status.get("0x0D")
        if _nanoe_status == None:
            return STATE_UNAVAILABLE
        _is_on = bool(int(_nanoe_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on nanoeX")
        await self.client.set_command(self.auth, 0x80 + 0x0D, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off nanoeX")
        await self.client.set_command(self.auth, 0x80 + 0x0D, 0)
        await self.coordinator.async_request_refresh()

class PanasonicDehumidifierPower(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic Dehumidifier power """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        return status.get("0x00", None) != None

    @property
    def label(self):
        return f"{self.nickname} {LABEL_POWER}"

    @property
    def icon(self) -> str:
        return ICON_TANK

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _power_status = status.get("0x00")
        if _power_status == None:
            return STATE_UNAVAILABLE
        _is_on = bool(int(_power_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on Dehumidifier")
        await self.client.set_command(self.auth, 0x80 + 0x00, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off Dehumidifier")
        await self.client.set_command(self.auth, 0x80 + 0x00, 0)
        await self.coordinator.async_request_refresh()

class PanasonicDehumidifierBuzzer(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic Dehumidifier buzzer """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        return status.get("0x00", None) != None

    @property
    def label(self):
        return f"{self.nickname} {LABEL_DEHUMIDIFIER_BUZZER}"

    @property
    def icon(self) -> str:
        return ICON_BUZZER

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _buzzer_status = status.get("0x18")
        if _buzzer_status == None:
            return STATE_UNAVAILABLE
        _is_off = not bool(int(_buzzer_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_off}")
        return _is_off

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on Dehumidifier buzzer")
        await self.client.set_command(self.auth, 0x80 + 0x18, 0) # invert
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off Dehumidifier buzzer")
        await self.client.set_command(self.auth, 0x80 + 0x18, 1) # invert
        await self.coordinator.async_request_refresh()

