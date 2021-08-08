from datetime import timedelta
import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_UNAVAILABLE

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    UPDATE_INTERVAL,
    DEVICE_TYPE_AC,
    DATA_CLIENT,
    DATA_COORDINATOR,
    LABEL_NANOE,
    LABEL_ECONAVI,
    LABEL_BUZZER,
    LABEL_TURBO,
    ICON_NANOE,
    ICON_ECONAVI,
    ICON_BUZZER,
    ICON_TURBO
)

_LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(seconds=UPDATE_INTERVAL)


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    switches = []

    for index, device in enumerate(devices):
        device_type = int(device.get("DeviceType"))

        if device_type == DEVICE_TYPE_AC:
            switches.append(
                PanasonicACNanoe(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )
            switches.append(
                PanasonicACEconavi(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )
            switches.append(
                PanasonicACBuzzer(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )
            switches.append(
                PanasonicACTurbo(
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
        _is_on_status = bool(int(status.get("0x00") or 0))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_NANOE}"

    @property
    def icon(self) -> str:
        return ICON_NANOE

    @property
    def device_class(self) -> str:
        return "switch"

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
        _is_on_status = bool(int(status.get("0x00") or 0))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_ECONAVI}"

    @property
    def icon(self) -> str:
        return ICON_ECONAVI

    @property
    def device_class(self) -> str:
        return "switch"

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
        _is_on_status = bool(int(status.get("0x00") or 0))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_BUZZER}"

    @property
    def icon(self) -> str:
        return ICON_BUZZER

    @property
    def device_class(self) -> str:
        return "switch"

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _nanoe_status = status.get("0x1e")
        if _nanoe_status == None:
            return STATE_UNAVAILABLE
        _is_on = bool(int(_nanoe_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on buzzer")
        await self.client.set_command(self.auth, 158, 0)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off buzzer")
        await self.client.set_command(self.auth, 158, 1)
        await self.coordinator.async_request_refresh()


class PanasonicACTurbo(PanasonicBaseEntity, SwitchEntity):
    """ Panasonic AC turbo switch """

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00") or 0))
        return _is_on_status

    @property
    def label(self):
        return f"{self.nickname} {LABEL_TURBO}"

    @property
    def icon(self) -> str:
        return ICON_TURBO

    @property
    def device_class(self) -> str:
        return "switch"

    @property
    def is_on(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _nanoe_status = status.get("0x1a")
        if _nanoe_status == None:
            return STATE_UNAVAILABLE
        _is_on = bool(int(_nanoe_status))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")
        return _is_on

    async def async_turn_on(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning on buzzer")
        await self.client.set_command(self.auth, 154, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        _LOGGER.debug(f"[{self.label}] Turning off buzzer")
        await self.client.set_command(self.auth, 154, 0)
        await self.coordinator.async_request_refresh()
