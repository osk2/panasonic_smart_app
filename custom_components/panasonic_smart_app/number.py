import logging
from datetime import timedelta
from homeassistant.components.number import NumberEntity

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    DEVICE_TYPE_AC,
    DEVICE_TYPE_DEHUMIDIFIER,
    DATA_CLIENT,
    DATA_COORDINATOR,
    LABEL_DEHUMIDIFIER_ON_TIMER,
    LABEL_DEHUMIDIFIER_OFF_TIMER,
    LABEL_CLIMATE_ON_TIMER,
    LABEL_CLIMATE_OFF_TIMER,
    UNIT_HOUR,
    UNIT_MINUTE,
    ICON_ON_TIMER,
    ICON_OFF_TIMER,
    CLIMATE_ON_TIMER_MIN,
    CLIMATE_ON_TIMER_MAX,
    CLIMATE_OFF_TIMER_MIN,
    CLIMATE_OFF_TIMER_MAX,
    DEHUMIDIFIER_ON_TIMER_MIN,
    DEHUMIDIFIER_ON_TIMER_MAX,
    DEHUMIDIFIER_OFF_TIMER_MIN,
    DEHUMIDIFIER_OFF_TIMER_MAX,
)

_LOGGER = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    commands = client.get_commands()
    numbers = []

    for index, device in enumerate(devices):

        current_device_commands = [
            command
            for command in commands
            if command["ModelType"] == device.get("ModelType")
        ]

        if int(device.get("DeviceType")) == DEVICE_TYPE_DEHUMIDIFIER:
            numbers.append(
                PanasonicDehumidifierOffTimer(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )

            if len(current_device_commands) > 0:
                is_on_timer_supported = (
                    len(
                        [
                            command
                            for command in current_device_commands[0]["JSON"][0]["list"]
                            if command["CommandType"] == "0x55"
                        ]
                    )
                    > 0
                )

                if is_on_timer_supported:
                    numbers.append(
                        PanasonicDehumidifierOnTimer(
                            coordinator,
                            index,
                            client,
                            device,
                        )
                    )

        if int(device.get("DeviceType")) == DEVICE_TYPE_AC:

            numbers.append(
                PanasonicACOffTimer(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )

            if len(current_device_commands) > 0:
                is_on_timer_supported = (
                    len(
                        [
                            command
                            for command in current_device_commands[0]["JSON"][0]["list"]
                            if command["CommandType"] == "0x0b"
                        ]
                    )
                    > 0
                )

                if is_on_timer_supported:
                    numbers.append(
                        PanasonicACOnTimer(
                            coordinator,
                            index,
                            client,
                            device,
                        )
                    )

    async_add_entities(numbers, True)

    return True


class PanasonicDehumidifierOnTimer(PanasonicBaseEntity, NumberEntity):
    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = int(status.get("0x00", -1)) == 0
        return _is_on_status

    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_DEHUMIDIFIER_ON_TIMER}"

    @property
    def icon(self) -> str:
        return ICON_ON_TIMER

    @property
    def native_value(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _on_timer = float(status.get("0x55") or 0)
        _timer_value = 0 if _on_timer <= 0 else _on_timer
        _LOGGER.debug(f"[{self.label}] value: {_timer_value}")
        return int(_timer_value)

    @property
    def native_min_value(self) -> int:
        return DEHUMIDIFIER_ON_TIMER_MIN

    @property
    def native_max_value(self) -> int:
        return DEHUMIDIFIER_ON_TIMER_MAX

    @property
    def native_unit_of_measurement(self) -> str:
        return UNIT_HOUR

    async def async_set_native_value(self, value: float) -> None:
        await self.client.set_command(self.auth, 213, int(value))
        await self.coordinator.async_request_refresh()


class PanasonicDehumidifierOffTimer(PanasonicBaseEntity, NumberEntity):
    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_DEHUMIDIFIER_OFF_TIMER}"

    @property
    def icon(self) -> str:
        return ICON_OFF_TIMER

    @property
    def native_value(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _off_timer = float(status.get("0x02") or 0)
        _timer_value = 0 if _off_timer <= 0 else _off_timer
        _LOGGER.debug(f"[{self.label}] value: {_timer_value}")
        return int(_timer_value)

    @property
    def native_min_value(self) -> int:
        return DEHUMIDIFIER_OFF_TIMER_MIN

    @property
    def native_max_value(self) -> int:
        return DEHUMIDIFIER_OFF_TIMER_MAX

    @property
    def native_unit_of_measurement(self) -> str:
        return UNIT_HOUR

    async def async_set_native_value(self, value: float) -> None:
        await self.client.set_command(self.auth, 130, int(value))
        await self.coordinator.async_request_refresh()


class PanasonicACOnTimer(PanasonicBaseEntity, NumberEntity):
    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        if status.get("0x00") == None:
            return False

        _is_on_status = int(status.get("0x00")) == 0
        return _is_on_status

    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_CLIMATE_ON_TIMER}"

    @property
    def icon(self) -> str:
        return ICON_ON_TIMER

    @property
    def native_value(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _on_timer = float(status.get("0x0B") or 0)
        _timer_value = 0 if _on_timer <= 0 else _on_timer
        _LOGGER.debug(f"[{self.label}] value: {_timer_value}")
        return int(_timer_value)

    @property
    def native_min_value(self) -> int:
        return CLIMATE_ON_TIMER_MIN

    @property
    def native_max_value(self) -> int:
        return CLIMATE_ON_TIMER_MAX

    @property
    def native_unit_of_measurement(self) -> str:
        return UNIT_MINUTE

    async def async_set_native_value(self, value: float) -> None:
        await self.client.set_command(self.auth, 139, int(value))
        await self.coordinator.async_request_refresh()


class PanasonicACOffTimer(PanasonicBaseEntity, NumberEntity):
    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_CLIMATE_OFF_TIMER}"

    @property
    def icon(self) -> str:
        return ICON_OFF_TIMER

    @property
    def native_value(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _off_timer = float(status.get("0x0C") or 0)
        _timer_value = 0 if _off_timer <= 0 else _off_timer
        _LOGGER.debug(f"[{self.label}] value: {_timer_value}")
        return int(_timer_value)

    @property
    def native_min_value(self) -> int:
        return CLIMATE_OFF_TIMER_MIN

    @property
    def native_max_value(self) -> int:
        return CLIMATE_OFF_TIMER_MAX

    @property
    def native_unit_of_measurement(self) -> str:
        return UNIT_MINUTE

    async def async_set_native_value(self, value: float) -> None:
        await self.client.set_command(self.auth, 140, int(value))
        await self.coordinator.async_request_refresh()
