import logging
from abc import ABC, abstractmethod

from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass
from homeassistant.const import STATE_UNAVAILABLE

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    DEVICE_TYPE_AC,
    DEVICE_TYPE_REFRIGERATOR,
    DEVICE_TYPE_DEHUMIDIFIER,
    DEVICE_TYPE_PURIFIER,
    DEVICE_TYPE_SWITCH,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DEVICE_CLASS_SWITCH,
    LABEL_SMART_SWITCH,
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
    LABEL_REFRIGERATOR_STOP_ICE_MAKING,
    LABEL_REFRIGERATOR_QUICK_ICE_MAKING,
    ICON_NANOE,
    ICON_NANOEX,
    ICON_ECONAVI,
    ICON_BUZZER,
    ICON_TURBO,
    ICON_SLEEP,
    ICON_MOLD_PREVENTION,
    ICON_CLEAN,
    ICON_PURIFIER,
    ICON_STOP_ICE_MAKING,
    ICON_QUICK_ICE_MAKING,
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
            # Process AC device switches
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

        elif device_type == DEVICE_TYPE_PURIFIER:
            # Process purifier device switches
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

        elif device_type == DEVICE_TYPE_DEHUMIDIFIER:
            # Process dehumidifier device switches
            if "0x0d" in command_types:
                switches.append(
                    PanasonicDehumidifierNanoeX(
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

        elif device_type == DEVICE_TYPE_REFRIGERATOR:
            # Process refrigerator device switches
            for switch_type in (
                PanasonicRefrigeratorStopIceMakingSwitch,
                PanasonicRefrigeratorQuickIceMakingSwitch,
            ):
                if switch_type.command_type in device["status"]:
                    switches.append(
                        switch_type(
                            coordinator,
                            index,
                            client,
                            device,
                        )
                    )

        elif device_type == DEVICE_TYPE_SWITCH:
            # Process smart switch device with sub-devices
            if "Devices" in device and isinstance(device["Devices"], list):
                for sub_device in device["Devices"]:
                    switch_device = device.copy()
                    switch_device["SubDevice"] = sub_device
                    switches.append(
                        PanasonicSmartSwitch(
                            coordinator,
                            index,
                            client,
                            switch_device,
                        )
                    )
                    _LOGGER.debug(
                        "Added smart switch: %s - Circuit %s", 
                        device.get("NickName", ""),
                        sub_device.get("Name", f"Circuit {sub_device['DeviceID']}")
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
        _LOGGER.debug("[%s] is_on: %s", self.label, _is_on)
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug("[%s] Turning on nanoe", self.label)
        await self.client.set_command(self.auth, 136, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug("[%s] Turning off nanoe", self.label)
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
        _LOGGER.debug("[%s] is_on: %s", self.label, _is_on)
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug("[%s] Turning on ECONAVI", self.label)
        await self.client.set_command(self.auth, 155, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug("[%s] Turning off ECONAVI", self.label)
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
        _LOGGER.debug("[%s] is_on: %s", self.label, _is_on)
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug("[%s] Turning on buzzer", self.label)
        await self.client.set_command(self.auth, 30, 0)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug("[%s] Turning off buzzer", self.label)
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
        _LOGGER.debug("[%s] is_on: %s", self.label, _is_on)
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug("[%s] Turning on turbo mode", self.label)
        await self.client.set_command(self.auth, 154, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug("[%s] Turning off turbo mode", self.label)
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
        _LOGGER.debug("[%s] is_on: %s", self.label, _is_on)
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug("[%s] Turning on sleep mode", self.label)
        await self.client.set_command(self.auth, 5, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug("[%s] Turning off sleep mode", self.label)
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
        _LOGGER.debug("[%s] is_on: %s", self.label, _is_on)
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug("[%s] Turning on mold prevention", self.label)
        await self.client.set_command(self.auth, 23, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug("[%s] Turning off mold prevention", self.label)
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
        _LOGGER.debug("[%s] is_on: %s", self.label, _is_on)
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug("[%s] Turning on self clean", self.label)
        await self.client.set_command(self.auth, 24, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug("[%s] Turning off self clean", self.label)
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
        _LOGGER.debug("[%s] is_on: %s", self.label, _is_on)
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug("[%s] Turning on nanoeX", self.label)
        await self.client.set_command(self.auth, 128, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug("[%s] Turning off nanoeX", self.label)
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
        _LOGGER.debug("[%s] is_on: %s", self.label, _is_on)
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug("[%s] Turning on nanoeX", self.label)
        await self.client.set_command(self.auth, 135, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug("[%s] Turning off nanoeX", self.label)
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
        _LOGGER.debug("[%s] is_on: %s", self.label, _is_on)
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug("[%s] Turning on nanoeX", self.label)
        await self.client.set_command(self.auth, 0x80 + 0x0D, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug("[%s] Turning off nanoeX", self.label)
        await self.client.set_command(self.auth, 0x80 + 0x0D, 0)
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
        _LOGGER.debug("[%s] is_on: %s", self.label, _is_off)
        return _is_off

    async def async_turn_on(self) -> None:
        _LOGGER.debug("[%s] Turning on Dehumidifier buzzer", self.label)
        await self.client.set_command(self.auth, 0x80 + 0x18, 0) # invert
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug("[%s] Turning off Dehumidifier buzzer", self.label)
        await self.client.set_command(self.auth, 0x80 + 0x18, 1) # invert
        await self.coordinator.async_request_refresh()


class PanasonicRefrigeratorSwitchABC(PanasonicBaseEntity, SwitchEntity, ABC):
    """Abstract class for switches of Panasonic refrigerator."""

    @property
    @abstractmethod
    def icon(self) -> str:
        """Icon of this entity."""

    @property
    @abstractmethod
    def command_name(self) -> str:
        """Command name from Panasonic UserGetRegisteredGwList2 API. Used for label."""

    @property
    @abstractmethod
    def command_type(self) -> str:
        """
        Command type from Panasonic UserGetRegisteredGwList2 API. Used to get and set
        the status.
        """

    @property
    def device_class(self) -> SwitchDeviceClass:
        return SwitchDeviceClass.SWITCH

    @property
    def is_on(self) -> bool | None:
        status = self.coordinator.data[self.index]["status"]

        try:
            _is_on = int(status[self.command_type]) == 1
        except (KeyError, ValueError):
            _LOGGER.exception("Error while getting status for %s", self.label)
            return None

        _LOGGER.debug("[%s] is_on: %s", self.label, _is_on)

        return _is_on

    async def async_turn_on(self, **_kwargs) -> None:
        """Turn on the switch."""
        _LOGGER.debug("[%s] Turning on", self.label)

        await self.client.set_command(
            deviceId=self.auth,
            command=int(self.command_type, 16),
            value=1,
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_kwargs) -> None:
        """Turn off the switch."""
        _LOGGER.debug("[%s] Turning off", self.label)

        await self.client.set_command(
            deviceId=self.auth,
            command=int(self.command_type, 16),
            value=0,
        )
        await self.coordinator.async_request_refresh()

    @property
    def label(self) -> str:
        return f"{self.nickname} {self.command_name}"


class PanasonicRefrigeratorStopIceMakingSwitch(PanasonicRefrigeratorSwitchABC):
    """Stop ice making switch of Panasonic refrigerator."""

    command_name = LABEL_REFRIGERATOR_STOP_ICE_MAKING
    command_type = "0x52"
    icon = ICON_STOP_ICE_MAKING


class PanasonicRefrigeratorQuickIceMakingSwitch(PanasonicRefrigeratorSwitchABC):
    """Quick ice making switch of Panasonic refrigerator."""

    command_name = LABEL_REFRIGERATOR_QUICK_ICE_MAKING
    command_type = "0x53"
    icon = ICON_QUICK_ICE_MAKING


class PanasonicSmartSwitch(PanasonicBaseEntity, SwitchEntity):
    """Panasonic Smart switch"""

    def __init__(self, coordinator, index, client, device):
        super().__init__(coordinator, index, client, device)
        # Store the sub-device info separately for easy access
        self.sub_device = device.get("SubDevice", {})

    @property
    def icon(self) -> str:
        return "mdi:light-switch"

    @property
    def device_class(self) -> SwitchDeviceClass:
        return SwitchDeviceClass.SWITCH

    @property
    def is_on(self) -> bool:
        device_status = self.coordinator.data[self.index]["status"]
        # Get total circuit status from 0x70
        circuit_status = int(device_status.get("0x70", "0"), 16)
        # The device index in Devices array corresponds to bit position
        # e.g. device 1 = bit 0, device 2 = bit 1, etc.
        device_bit = 1 << (self.sub_device["DeviceID"] - 1)
        status = bool(circuit_status & device_bit)
        _LOGGER.debug("[%s] is_on: %s", self.label, status)
        return status

    async def async_turn_on(self, **_kwargs) -> None:
        """ turn on switch """
        _LOGGER.debug("[%s] Turning on switch %d", self.label, self.sub_device["DeviceID"])
        # 0x70 command controls all circuits, need to maintain other states
        device_status = self.coordinator.data[self.index]["status"]
        current_status = int(device_status.get("0x70", "0"), 16)
        device_bit = 1 << (self.sub_device["DeviceID"] - 1)
        new_status = current_status | device_bit  # Set device bit to 1
        await self.client.set_command(self.auth, 0x70, new_status)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_kwargs) -> None:
        """ turn off switch """
        _LOGGER.debug("[%s] Turning off switch %d", self.label, self.sub_device["DeviceID"])
        # 0x70 command controls all circuits, need to maintain other states
        device_status = self.coordinator.data[self.index]["status"]
        current_status = int(device_status.get("0x70", "0"), 16)
        device_bit = 1 << (self.sub_device["DeviceID"] - 1)
        new_status = current_status & ~device_bit  # Clear device bit to 0
        await self.client.set_command(self.auth, 0x70, new_status)
        await self.coordinator.async_request_refresh()

    @property
    def label(self) -> str:
        sub_device_name = self.sub_device.get('Name')
        if not sub_device_name:
            sub_device_name = LABEL_SMART_SWITCH
        return f"{self.nickname} {sub_device_name}"
