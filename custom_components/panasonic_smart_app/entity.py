import logging
from datetime import timedelta
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List

from homeassistant.const import (
    STATE_UNAVAILABLE,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_TEMPERATURE,
    TEMP_CELSIUS,
    ATTR_TEMPERATURE,
    PERCENTAGE,
)
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.humidifier import HumidifierEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.humidifier.const import (
    DEVICE_CLASS_DEHUMIDIFIER,
    SUPPORT_MODES,
)
from homeassistant.components.climate.const import (
    HVAC_MODE_COOL,
    HVAC_MODE_DRY,
    HVAC_MODE_HEAT,
    HVAC_MODE_AUTO,
    HVAC_MODE_FAN_ONLY,
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_FAN_MODE,
    SUPPORT_SWING_MODE,
    SUPPORT_PRESET_MODE,
)

from .const import (
    DOMAIN,
    LABEL_DEHUMIDIFIER,
    LABEL_CLIMATE,
    LABEL_HUMIDITY,
    LABEL_TANK,
    LABEL_ON_TIMER,
    LABEL_OFF_TIMER,
    LABEL_OUTDOOR_TEMPERATURE,
    ICON_HUMIDITY,
    ICON_TANK,
    ICON_TIMER,
    ICON_THERMOMETER,
    MANUFACTURER,
    UPDATE_INTERVAL,
    DEHUMIDIFIER_MIN_HUMD,
    DEHUMIDIFIER_MAX_HUMD,
    DEHUMIDIFIER_AVAILABLE_HUMIDITY,
    CLIMATE_AVAILABLE_MODE,
    CLIMATE_AVAILABLE_PRESET,
    CLIMATE_AVAILABLE_SWING_MODE,
    CLIMATE_AVAILABLE_FAN_MODE,
    CLIMATE_MINIMUM_TEMPERATURE,
    CLIMATE_MAXIMUM_TEMPERATURE,
    CLIMATE_TEMPERATURE_STEP,
    ON_TIMER_MIN,
    ON_TIMER_MAX,
    OFF_TIMER_MIN,
    OFF_TIMER_MAX,
)

_LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(seconds=UPDATE_INTERVAL)


def getKeyFromDict(targetDict, mode_name):
    for key, value in targetDict.items():
        if mode_name == value:
            return key

    return None


class PanasonicBaseEntity(ABC):
    def __init__(
        self,
        client,
        device,
    ):
        self.client = client
        self.device = device

    @property
    @abstractmethod
    def label(self) -> str:
        """Label to use for name and unique id."""
        ...

    @property
    def current_device_info(self) -> dict:
        return self.device["Devices"][0]

    @property
    def nickname(self) -> str:
        return self.current_device_info["NickName"]

    @property
    def model(self) -> str:
        return self.current_device_info["Model"]

    @property
    def commands(self) -> list:
        command_list = self.client.get_commands()
        current_model_type = self.current_device_info["ModelType"]
        commands = list(
            filter(lambda c: c["ModelType"] == current_model_type, command_list)
        )

        return commands[0]["JSON"][0]["list"]

    @property
    def name(self) -> str:
        return f"{self.nickname} {self.label}"

    @property
    def auth(self) -> str:
        return self.device["auth"]

    @property
    def unique_id(self) -> str:
        return self.auth + self.label

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.auth)},
            "name": self.nickname,
            "manufacturer": MANUFACTURER,
            "model": self.model,
        }


class PanasonicDehumidifier(PanasonicBaseEntity, HumidifierEntity):
    def __init__(self, client, device):

        super().__init__(client, device)

        self._is_on_status = False
        self._mode = ""
        self._current_humd = 0
        self._target_humd = 0

    async def async_update(self):
        _LOGGER.debug(f"------- UPDATING {self.nickname} {self.label} -------")
        try:
            self._status = await self.client.get_device_info(
                self.auth,
                options=["0x50", "0x00", "0x01", "0x0a", "0x04"],
            )

        except:
            _LOGGER.error(f"[{self.nickname}] Error occured while updating status")
        else:
            _LOGGER.debug(f"[{self.nickname}] status: {self._status}")
            # _is_on
            self._is_on_status = bool(int(self._status.get("0x00")))
            _LOGGER.debug(f"[{self.nickname}] _is_on: {self._is_on_status}")

            # _mode
            raw_mode_list = list(
                filter(lambda c: c["CommandType"] == "0x01", self.commands)
            )[0]["Parameters"]
            self._mode = list(
                filter(lambda m: m[1] == int(self._status.get("0x01")), raw_mode_list)
            )[0][0]
            _LOGGER.debug(f"[{self.nickname}] _mode: {self._mode}")

            # _target_humd
            self._target_humd = DEHUMIDIFIER_AVAILABLE_HUMIDITY[
                int(self._status.get("0x04"))
            ]
            _LOGGER.debug(f"[{self.nickname}] _target_humd: {self._target_humd}")

            _LOGGER.debug(f"[{self.nickname}] update completed.")

    @property
    def label(self):
        return LABEL_DEHUMIDIFIER

    @property
    def target_humidity(self):
        return self._target_humd

    @property
    def max_humidity(self):
        return DEHUMIDIFIER_MAX_HUMD

    @property
    def min_humidity(self):
        return DEHUMIDIFIER_MIN_HUMD

    @property
    def mode(self):
        return self._mode

    @property
    def available_modes(self):
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x01", self.commands)
        )[0]["Parameters"]

        def mode_extractor(mode):
            return mode[0]

        mode_list = list(map(mode_extractor, raw_mode_list))
        return mode_list

    @property
    def supported_features(self):
        return SUPPORT_MODES

    @property
    def is_on(self):
        return self._is_on_status

    @property
    def device_class(self):
        return DEVICE_CLASS_DEHUMIDIFIER

    async def async_set_mode(self, mode):
        """ Set operation mode """
        if mode is None:
            return

        _LOGGER.debug("Set %s mode %s", self.name, mode)

        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x01", self.commands)
        )[0]
        mode_info = list(filter(lambda m: m[0] == mode, raw_mode_list["Parameters"]))[0]

        await self.client.set_command(self.auth, 129, int(mode_info[1]))

    async def async_set_humidity(self, humidity):
        """ Set target humidity """
        if humidity is None:
            return

        """ Find closest humidity value """
        targetValue = min(
            list(DEHUMIDIFIER_AVAILABLE_HUMIDITY.values()),
            key=lambda x: abs(x - humidity),
        )
        targetKey = getKeyFromDict(DEHUMIDIFIER_AVAILABLE_HUMIDITY, targetValue)

        _LOGGER.debug("Set %s humidity to %s", self.name, targetValue)
        await self.client.set_command(self.auth, 132, int(targetKey))

    async def async_turn_on(self):
        """ Turn on dehumidifier """
        _LOGGER.debug("Turn %s on", self.name)
        await self.client.set_command(self.auth, 128, 1)

    async def async_turn_off(self):
        """ Turn off dehumidifier """
        _LOGGER.debug("Turn %s off", self.name)
        await self.client.set_command(self.auth, 128, 0)


class PanasonicHumiditySensor(PanasonicBaseEntity, SensorEntity):
    """ Panasonic dehumidifier current humidity sensor """

    async def async_update(self):
        _LOGGER.debug(f"------- UPDATING {self.nickname} {self.label} -------")

        try:
            self._status = await self.client.get_device_info(
                self.auth,
                options=["0x07", "0x0a"],
            )

            self._current_humd = self._status.get("0x07")
            _LOGGER.debug(f"[{self.nickname}] _current_humd: {self._current_humd}")

            self._is_tank_full = self._status.get("0x0a")
            _LOGGER.debug(f"[{self.nickname}] _is_tank_full: {self._is_tank_full}")
        except:
            _LOGGER.error(f"[{self.nickname}] Error occured while updating status")
        else:
            _LOGGER.debug(f"[{self.nickname}] status: {self._status}")

    @property
    def label(self) -> str:
        return LABEL_HUMIDITY

    @property
    def icon(self) -> str:
        return ICON_HUMIDITY

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_HUMIDITY

    @property
    def state(self) -> int:
        return self._current_humd if self._current_humd else STATE_UNAVAILABLE

    @property
    def unit_of_measurement(self) -> str:
        return PERCENTAGE


class PanasonicOnTimer(PanasonicBaseEntity, NumberEntity):
    """ Currently not used as not all model support this timer """

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
        return LABEL_ON_TIMER

    @property
    def icon(self) -> str:
        return ICON_TIMER

    @property
    def value(self) -> int:
        return int(self._timer_value)

    @property
    def min_value(self) -> int:
        return ON_TIMER_MIN

    @property
    def max_value(self) -> int:
        return ON_TIMER_MAX

    async def async_set_value(self, value: float) -> None:
        return await self.client.set_command(self.auth, 213, int(value))


class PanasonicOffTimer(PanasonicBaseEntity, NumberEntity):
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
        return LABEL_OFF_TIMER

    @property
    def icon(self) -> str:
        return ICON_TIMER

    @property
    def value(self) -> int:
        return int(self._timer_value)

    @property
    def min_value(self) -> int:
        return OFF_TIMER_MIN

    @property
    def max_value(self) -> int:
        return OFF_TIMER_MAX

    async def async_set_value(self, value: float) -> None:
        return await self.client.set_command(self.auth, 130, int(value))


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
            self._tank_status = bool(int(self._status.get("0x0a")))
            _LOGGER.debug(f"[{self.nickname}] _tank_status: {self._tank_status}")

    @property
    def label(self) -> str:
        return LABEL_TANK

    @property
    def icon(self) -> str:
        return ICON_TANK

    @property
    def is_on(self) -> bool:
        return self._tank_status


class PanasonicClimate(PanasonicBaseEntity, ClimateEntity):
    def __init__(self, client, device):
        super().__init__(client, device)

        self._is_on = False
        self._hvac_mode = HVAC_MODE_COOL

        self._unit = TEMP_CELSIUS
        self._target_temperature = None
        self._current_temperature = None

    async def async_update(self):
        _LOGGER.debug(f"------- UPDATING {self.nickname} {self.label}-------")
        """Update the state of this climate device."""
        self._status = await self.client.get_device_info(
            self.auth,
            options=["0x00", "0x01", "0x04", "0x03", "0x02", "0x0f", "0x21"],
        )
        _LOGGER.debug(f"Status: {self._status}")

        self._is_on = bool(int(self._status.get("0x00")))
        _LOGGER.debug(f"_is_on: {self._is_on}")

        self._target_temperature = float(self._status.get("0x03"))
        _LOGGER.debug(f"_current_temperature: {self._target_temperature}")

        self._current_temperature = float(self._status.get("0x04"))
        _LOGGER.debug(f"_current_temperature: {self._current_temperature}")

        self._fan_mode = int(self._status.get("0x02"))
        _LOGGER.debug(f"_fan_mode: {self._fan_mode}")

        self._swing_mode = int(self._status.get("0x0f"))
        _LOGGER.debug(f"_swing_mode: {self._swing_mode}")

        _LOGGER.debug(f"[{self.nickname}] is UPDATED.")

    @property
    def label(self):
        return LABEL_CLIMATE

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_FAN_MODE | SUPPORT_SWING_MODE

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def hvac_mode(self) -> str:
        """Return the current operation."""
        if not self._is_on:
            return HVAC_MODE_OFF
        else:
            value = int(self._status.get("0x01"))
            mode_mapping = list(
                filter(lambda m: m["mappingCode"] == value, CLIMATE_AVAILABLE_MODE)
            )[0]
            _LOGGER.debug(
                f"{self.nickname} hvac_mode is {value} - {mode_mapping['key']}"
            )
            return mode_mapping["key"]

    @property
    def hvac_modes(self) -> list:
        raw_modes = list(filter(lambda c: c["CommandType"] == "0x01", self.commands))[
            0
        ]["Parameters"]

        def mode_extractor(mode):
            mode_mapping = list(
                filter(lambda m: m["mappingCode"] == mode[1], CLIMATE_AVAILABLE_MODE)
            )[0]
            return mode_mapping["key"]

        modes = list(map(mode_extractor, raw_modes))

        """ Force adding off mode into list """
        modes.append(HVAC_MODE_OFF)

        return modes

    async def async_set_hvac_mode(self, hvac_mode) -> None:
        _LOGGER.debug(f"{self.nickname} set_hvac_mode: {hvac_mode}")
        if hvac_mode == HVAC_MODE_OFF:
            await self.client.set_command(self.auth, 128, 0)
        else:
            mode_mapping = list(
                mode for mode in CLIMATE_AVAILABLE_MODE if mode["key"] == hvac_mode
            )[0]
            mode = mode_mapping["mappingCode"]
            await self.client.set_command(self.auth, 129, mode)
            if not self._is_on:
                await self.client.set_command(self.auth, 128, 1)

    @property
    def preset_mode(self) -> str:
        """ Return the current operation """
        if not self._is_on:
            return HVAC_MODE_OFF
        else:
            value = int(self._status.get("0x01"))
            _LOGGER.debug(
                f"{self.nickname} hvac_mode is {value} - {CLIMATE_AVAILABLE_PRESET[value]}"
            )
            return CLIMATE_AVAILABLE_PRESET[value]

    @property
    def preset_modes(self) -> list:
        return list(CLIMATE_AVAILABLE_PRESET.values())

    async def set_preset_mode(self, preset_mode) -> None:
        _LOGGER.debug(f"{self.nickname} set_preset_mode: {preset_mode}")
        value = getKeyFromDict(CLIMATE_AVAILABLE_PRESET, preset_mode)
        self.client.set_command(self.auth, 1, value)
        if not self._is_on:
            self.client.set_command(self.auth, 0, 1)

    @property
    def fan_mode(self) -> str:
        """ Return the fan setting """
        return CLIMATE_AVAILABLE_FAN_MODE[self._fan_mode]

    @property
    def fan_modes(self) -> list:
        """ Return the list of available fan modes """
        return list(CLIMATE_AVAILABLE_FAN_MODE.values())

    async def async_set_fan_mode(self, fan_mode):
        """Set new fan mode."""
        _LOGGER.debug("Set %s focus mode %s", self.name, fan_mode)
        mode_id = int(getKeyFromDict(CLIMATE_AVAILABLE_FAN_MODE, fan_mode))
        await self.client.set_command(self.auth, 130, mode_id)

    @property
    def swing_mode(self) -> str:
        """ Return the fan setting """
        return CLIMATE_AVAILABLE_SWING_MODE[self._swing_mode]

    @property
    def swing_modes(self) -> list:
        """ Return the list of available swing modes """
        return list(CLIMATE_AVAILABLE_SWING_MODE.values())

    async def async_set_swing_mode(self, swing_mode):
        _LOGGER.debug("Set %s swing mode %s", self.name, swing_mode)
        mode_id = int(getKeyFromDict(CLIMATE_AVAILABLE_SWING_MODE, swing_mode))
        await self.client.set_command(self.auth, 143, mode_id)

    @property
    def target_temperature(self) -> int:
        """ Return the target temperature """
        return self._target_temperature

    async def async_set_temperature(self, **kwargs):
        """ Set new target temperature """
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        _LOGGER.debug("Set %s temperature %s", self.name, target_temp)
        await self.client.set_command(self.auth, 3, int(target_temp))

    @property
    def current_temperature(self) -> int:
        """ Return the current temperature """
        return self._current_temperature

    @property
    def min_temp(self) -> int:
        """ Return the minimum temperature """
        temperature_range = list(
            filter(lambda c: c["CommandType"] == "0x03", self.commands)
        )[0]["Parameters"]
        minimum_temperature = list(filter(lambda t: t[0] == "Min", temperature_range))[
            0
        ][1]

        return minimum_temperature

    @property
    def max_temp(self) -> int:
        """ Return the maximum temperature """
        temperature_range = list(
            filter(lambda c: c["CommandType"] == "0x03", self.commands)
        )[0]["Parameters"]
        maximum_temperature = list(filter(lambda t: t[0] == "Max", temperature_range))[
            0
        ][1]

        return maximum_temperature

    @property
    def target_temperature_step(self) -> float:
        """ Return temperature step """
        return CLIMATE_TEMPERATURE_STEP


class PanasonicOutdoorTemperatureSensor(PanasonicBaseEntity, SensorEntity):
    """ Panasonic AC outdoor temperature sensor """

    async def async_update(self):
        _LOGGER.debug(f"------- UPDATING {self.nickname} {self.label} -------")

        try:
            self._status = await self.client.get_device_info(
                self.auth,
                options=["0x21"],
            )

            self._outside_temperature = float(self._status.get("0x21"))
            _LOGGER.debug(f"_outside_temperature: {self._outside_temperature}")
        except:
            _LOGGER.error(f"[{self.nickname}] Error occured while updating status")
        else:
            _LOGGER.debug(f"[{self.nickname}] status: {self._status}")

    @property
    def label(self) -> str:
        return LABEL_OUTDOOR_TEMPERATURE

    @property
    def icon(self) -> str:
        return ICON_THERMOMETER

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_TEMPERATURE

    @property
    def state(self) -> int:
        return (
            self._outside_temperature
            if self._outside_temperature
            else STATE_UNAVAILABLE
        )

    @property
    def unit_of_measurement(self) -> str:
        return TEMP_CELSIUS
