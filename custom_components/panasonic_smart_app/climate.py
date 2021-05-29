import logging
from datetime import timedelta
from homeassistant.components.climate import ClimateEntity
from homeassistant.const import (
    TEMP_CELSIUS,
    ATTR_TEMPERATURE,
)
from homeassistant.components.climate.const import (
    HVAC_MODE_COOL,
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

    for device in devices:
        if int(device["Devices"][0]["DeviceType"]) == DEVICE_TYPE_AC:
            climate.append(
                PanasonicClimate(
                    client,
                    device,
                )
            )

    async_add_entities(climate, True)

    return True


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
        _LOGGER.debug(f"[{self.nickname}] Status: {self._status}")

        self._is_on = bool(int(self._status.get("0x00")))
        _LOGGER.debug(f"[{self.nickname}] _is_on: {self._is_on}")

        self._target_temperature = float(self._status.get("0x03"))
        _LOGGER.debug(
            f"[{self.nickname}] _current_temperature: {self._target_temperature}"
        )

        self._current_temperature = float(self._status.get("0x04"))
        _LOGGER.debug(
            f"[{self.nickname}] _current_temperature: {self._current_temperature}"
        )

        self._fan_mode = int(self._status.get("0x02"))
        _LOGGER.debug(f"[{self.nickname}] _fan_mode: {self._fan_mode}")

        self._swing_mode = int(self._status.get("0x0f"))
        _LOGGER.debug(f"[{self.nickname}] _swing_mode: {self._swing_mode}")

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
                f"[{self.nickname}] hvac_mode is {value} - {mode_mapping['key']}"
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
        _LOGGER.debug(f"[{self.nickname}] set_hvac_mode: {hvac_mode}")
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
                f"[{self.nickname}] hvac_mode is {value} - {CLIMATE_AVAILABLE_PRESET[value]}"
            )
            return CLIMATE_AVAILABLE_PRESET[value]

    @property
    def preset_modes(self) -> list:
        return list(CLIMATE_AVAILABLE_PRESET.values())

    async def set_preset_mode(self, preset_mode) -> None:
        _LOGGER.debug(f"[{self.nickname}] set_preset_mode: {preset_mode}")
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
        _LOGGER.debug(f"[{self.nickname}] Set fan mode to {fan_mode}")
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
        _LOGGER.debug(f"[{self.nickname}] Set swing mode to {swing_mode}")
        mode_id = int(getKeyFromDict(CLIMATE_AVAILABLE_SWING_MODE, swing_mode))
        await self.client.set_command(self.auth, 143, mode_id)

    @property
    def target_temperature(self) -> int:
        """ Return the target temperature """
        return self._target_temperature

    async def async_set_temperature(self, **kwargs):
        """ Set new target temperature """
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        _LOGGER.debug(f"[{self.nickname}] Set temperature to {target_temp}")
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
