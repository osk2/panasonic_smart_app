import logging
from datetime import timedelta
from homeassistant.components.climate import ClimateEntity
from homeassistant.const import (
    TEMP_CELSIUS,
    ATTR_TEMPERATURE,
)
from homeassistant.components.climate.const import (
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_FAN_MODE,
    SUPPORT_SWING_MODE,
)

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    DEVICE_TYPE_AC,
    UPDATE_INTERVAL,
    DATA_CLIENT,
    DATA_COORDINATOR,
    CLIMATE_AVAILABLE_MODE,
    CLIMATE_AVAILABLE_PRESET,
    CLIMATE_AVAILABLE_SWING_MODE,
    CLIMATE_AVAILABLE_FAN_MODE,
    CLIMATE_TEMPERATURE_STEP,
    LABEL_CLIMATE,
)

_LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(seconds=UPDATE_INTERVAL)


def getKeyFromDict(targetDict, mode_name):
    for key, value in targetDict.items():
        if mode_name == value:
            return key

    return None


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    climate = []

    for index, device in enumerate(devices):
        if int(device["Devices"][0]["DeviceType"]) == DEVICE_TYPE_AC:
            climate.append(
                PanasonicClimate(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )

    async_add_entities(climate, True)

    return True


class PanasonicClimate(PanasonicBaseEntity, ClimateEntity):

    @property
    def label(self):
        return LABEL_CLIMATE

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_FAN_MODE | SUPPORT_SWING_MODE

    @property
    def temperature_unit(self) -> str:
        return TEMP_CELSIUS

    @property
    def hvac_mode(self) -> str:
        status = self.coordinator.data[self.index]["status"]
        _is_on = bool(int(status.get("0x00") or 0))

        if not _is_on:
            return HVAC_MODE_OFF
        else:
            value = int(status.get("0x01"))
            mode_mapping = list(
                filter(lambda m: m["mappingCode"] == value, CLIMATE_AVAILABLE_MODE)
            )[0]
            _LOGGER.debug(
                f"[{self.label}] hvac_mode: {mode_mapping['key']}"
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

        _hvac_modes = list(map(mode_extractor, raw_modes))

        """ Force adding off mode into list """
        _hvac_modes.append(HVAC_MODE_OFF)

        _LOGGER.debug(f"[{self.label}] hvac_modes: {_hvac_modes}")

        return _hvac_modes

    async def async_set_hvac_mode(self, hvac_mode) -> None:
        _LOGGER.debug(f"[{self.label}] set_hvac_mode: {hvac_mode}")
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

        await self.coordinator.async_request_refresh()

    @property
    def preset_mode(self) -> str:
        status = self.coordinator.data[self.index]["status"]
        _is_on = bool(int(status.get("0x00") or 0))
        _hvac_mode = int(status.get("0x01"))
        _preset_mode = HVAC_MODE_OFF if not _is_on else CLIMATE_AVAILABLE_PRESET[_hvac_mode]
        _LOGGER.debug(f"[{self.label}] preset_mode: {_preset_mode}")

        return _preset_mode

    @property
    def preset_modes(self) -> list:
        _preset_modes = list(CLIMATE_AVAILABLE_PRESET.values())
        _LOGGER.debug(f"[{self.label}] preset_modes: {_preset_modes}")
        return _preset_modes

    async def set_preset_mode(self, preset_mode) -> None:
        _LOGGER.debug(f"[{self.label}] set_preset_mode: {preset_mode}")
        value = getKeyFromDict(CLIMATE_AVAILABLE_PRESET, preset_mode)
        self.client.set_command(self.auth, 1, value)
        if not self._is_on:
            self.client.set_command(self.auth, 0, 1)

        await self.coordinator.async_request_refresh()

    @property
    def fan_mode(self) -> str:
        status = self.coordinator.data[self.index]["status"]
        _fan_mode = int(status.get("0x02") or 0)
        _LOGGER.debug(f"[{self.label}] fan_mode: {_fan_mode}")
        return CLIMATE_AVAILABLE_FAN_MODE[_fan_mode]

    @property
    def fan_modes(self) -> list:
        _fan_modes = list(CLIMATE_AVAILABLE_FAN_MODE.values())
        _LOGGER.debug(f"[{self.label}] fan_modes: {_fan_modes}")
        return _fan_modes

    async def async_set_fan_mode(self, fan_mode) -> None:
        """Set new fan mode."""
        _LOGGER.debug(f"[{self.label}] Set fan mode to {fan_mode}")
        mode_id = int(getKeyFromDict(CLIMATE_AVAILABLE_FAN_MODE, fan_mode))
        await self.client.set_command(self.auth, 130, mode_id)
        await self.coordinator.async_request_refresh()

    @property
    def swing_mode(self) -> str:
        status = self.coordinator.data[self.index]["status"]
        _raw_swing_mode = int(status.get("0x0f") or 0)
        _swing_mode = CLIMATE_AVAILABLE_SWING_MODE[_raw_swing_mode]
        _LOGGER.debug(f"[{self.label}] swing_mode: {_swing_mode}")
        return _swing_mode

    @property
    def swing_modes(self) -> list:
        _swing_modes = list(CLIMATE_AVAILABLE_SWING_MODE.values())
        _LOGGER.debug(f"[{self.label}] swing_modes: {_swing_modes}")
        return _swing_modes

    async def async_set_swing_mode(self, swing_mode) -> None:
        _LOGGER.debug(f"[{self.label}] Set swing mode to {swing_mode}")
        mode_id = int(getKeyFromDict(CLIMATE_AVAILABLE_SWING_MODE, swing_mode))
        await self.client.set_command(self.auth, 143, mode_id)
        await self.coordinator.async_request_refresh()

    @property
    def target_temperature(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _target_temperature = float(status.get("0x03") or 0)
        _LOGGER.debug(f"[{self.label}] target_temperature: {_target_temperature}")
        return _target_temperature

    async def async_set_temperature(self, **kwargs):
        """ Set new target temperature """
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        _LOGGER.debug(f"[{self.label}] Set temperature to {target_temp}")
        await self.client.set_command(self.auth, 3, int(target_temp))
        await self.coordinator.async_request_refresh()

    @property
    def current_temperature(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _current_temperature = float(status.get("0x04") or 0)
        return _current_temperature

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
