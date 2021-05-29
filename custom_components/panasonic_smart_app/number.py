import logging
from datetime import timedelta
from homeassistant.components.number import NumberEntity

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    UPDATE_INTERVAL,
    DEVICE_TYPE_AC,
    DEVICE_TYPE_DEHUMIDIFIER,
    DATA_CLIENT,
    DATA_COORDINATOR,
    LABEL_DEHUMIDIFIER_ON_TIMER,
    LABEL_DEHUMIDIFIER_OFF_TIMER,
    LABEL_CLIMATE_ON_TIMER,
    LABEL_CLIMATE_OFF_TIMER,
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
SCAN_INTERVAL = timedelta(seconds=UPDATE_INTERVAL)


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    commands = client.get_commands()
    numbers = []

    for device in devices:

        current_device_commands = [
            command
            for command in commands
            if command["ModelType"] == device["Devices"][0]["ModelType"]
        ]

        if int(device["Devices"][0]["DeviceType"]) == DEVICE_TYPE_DEHUMIDIFIER:
            numbers.append(
                PanasonicDehumidifierOffTimer(
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
                            client,
                            device,
                        )
                    )

        if int(device["Devices"][0]["DeviceType"]) == DEVICE_TYPE_AC:

            numbers.append(
                PanasonicACOffTimer(
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
                            client,
                            device,
                        )
                    )

    async_add_entities(numbers, True)

    return True


class PanasonicDehumidifierOnTimer(PanasonicBaseEntity, NumberEntity):
    async def async_update(self):
        _LOGGER.debug(f"------- UPDATING {self.nickname} {self.label} -------")
        try:
            self._status = await self.client.get_device_info(
                self.auth,
                options=["0x00", "0x55"],
            )

            self._on_timer = float(self._status.get("0x55"))
            _LOGGER.debug(f"[{self.nickname}] _on_timer: {self._on_timer}")

            self._is_on_status = bool(int(self._status.get("0x00")))
            _LOGGER.debug(f"[{self.nickname}] _is_on_status: {self._is_on_status}")

        except:
            _LOGGER.error(f"[{self.nickname}] Error occured while updating status")
        else:
            self._timer_value = 0 if self._on_timer <= 0 else self._on_timer
            _LOGGER.debug(f"[{self.nickname}] _timer_value: {self._timer_value}")

    @property
    def available(self) -> bool:
        return not self._is_on_status

    @property
    def label(self) -> str:
        return LABEL_DEHUMIDIFIER_ON_TIMER

    @property
    def icon(self) -> str:
        return ICON_ON_TIMER

    @property
    def value(self) -> int:
        return int(self._timer_value)

    @property
    def min_value(self) -> int:
        return DEHUMIDIFIER_ON_TIMER_MIN

    @property
    def max_value(self) -> int:
        return DEHUMIDIFIER_ON_TIMER_MAX

    async def async_set_value(self, value: float) -> None:
        return await self.client.set_command(self.auth, 213, int(value))


class PanasonicDehumidifierOffTimer(PanasonicBaseEntity, NumberEntity):
    async def async_update(self):
        _LOGGER.debug(f"------- UPDATING {self.nickname} {self.label} -------")
        try:
            self._status = await self.client.get_device_info(
                self.auth,
                options=["0x00", "0x02"],
            )

            self._off_timer = float(self._status.get("0x02"))
            _LOGGER.debug(f"[{self.nickname}] _off_timer: {self._off_timer}")

            self._is_on_status = bool(int(self._status.get("0x00")))
            _LOGGER.debug(f"[{self.nickname}] _is_on_status: {self._is_on_status}")

        except:
            _LOGGER.error(f"[{self.nickname}] Error occured while updating status")
        else:
            self._timer_value = 0 if self._off_timer <= 0 else self._off_timer
            _LOGGER.debug(f"[{self.nickname}] _timer_value: {self._timer_value}")

    @property
    def available(self) -> bool:
        return self._is_on_status

    @property
    def label(self) -> str:
        return LABEL_DEHUMIDIFIER_OFF_TIMER

    @property
    def icon(self) -> str:
        return ICON_OFF_TIMER

    @property
    def value(self) -> int:
        return int(self._timer_value)

    @property
    def min_value(self) -> int:
        return DEHUMIDIFIER_OFF_TIMER_MIN

    @property
    def max_value(self) -> int:
        return DEHUMIDIFIER_OFF_TIMER_MAX

    async def async_set_value(self, value: float) -> None:
        return await self.client.set_command(self.auth, 130, int(value))


class PanasonicACOnTimer(PanasonicBaseEntity, NumberEntity):
    async def async_update(self):
        _LOGGER.debug(f"------- UPDATING {self.nickname} {self.label} -------")
        try:
            self._status = await self.client.get_device_info(
                self.auth,
                options=["0x00", "0x0b"],
            )

            self._on_timer = float(self._status.get("0x0b"))
            _LOGGER.debug(f"[{self.nickname}] _on_timer: {self._on_timer}")

            self._is_on_status = bool(int(self._status.get("0x00")))
            _LOGGER.debug(f"[{self.nickname}] _is_on_status: {self._is_on_status}")

        except:
            _LOGGER.error(f"[{self.nickname}] Error occured while updating status")
        else:
            self._timer_value = 0 if self._on_timer <= 0 else self._on_timer
            _LOGGER.debug(f"[{self.nickname}] _timer_value: {self._timer_value}")

    @property
    def available(self) -> bool:
        return not self._is_on_status

    @property
    def label(self) -> str:
        return LABEL_CLIMATE_ON_TIMER

    @property
    def icon(self) -> str:
        return ICON_ON_TIMER

    @property
    def value(self) -> int:
        return int(self._timer_value)

    @property
    def min_value(self) -> int:
        return CLIMATE_ON_TIMER_MIN

    @property
    def max_value(self) -> int:
        return CLIMATE_ON_TIMER_MAX

    async def async_set_value(self, value: float) -> None:
        return await self.client.set_command(self.auth, 139, int(value))


class PanasonicACOffTimer(PanasonicBaseEntity, NumberEntity):
    async def async_update(self):
        _LOGGER.debug(f"------- UPDATING {self.nickname} {self.label} -------")
        try:
            self._status = await self.client.get_device_info(
                self.auth,
                options=["0x00", "0x0c"],
            )

            self._off_timer = float(self._status.get("0x0c"))
            _LOGGER.debug(f"[{self.nickname}] _off_timer: {self._off_timer}")

            self._is_on_status = bool(int(self._status.get("0x00")))
            _LOGGER.debug(f"[{self.nickname}] _is_on_status: {self._is_on_status}")

        except:
            _LOGGER.error(f"[{self.nickname}] Error occured while updating status")
        else:
            self._timer_value = 0 if self._off_timer <= 0 else self._off_timer
            _LOGGER.debug(f"[{self.nickname}] _timer_value: {self._timer_value}")

    @property
    def available(self) -> bool:
        return self._is_on_status

    @property
    def label(self) -> str:
        return LABEL_CLIMATE_OFF_TIMER

    @property
    def icon(self) -> str:
        return ICON_OFF_TIMER

    @property
    def value(self) -> int:
        return int(self._timer_value)

    @property
    def min_value(self) -> int:
        return CLIMATE_OFF_TIMER_MIN

    @property
    def max_value(self) -> int:
        return CLIMATE_OFF_TIMER_MAX

    async def async_set_value(self, value: float) -> None:
        return await self.client.set_command(self.auth, 140, int(value))
