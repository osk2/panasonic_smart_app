from pprint import pprint
import logging
import voluptuous as vol
from typing import Any, Dict, Optional, List
from datetime import timedelta
import homeassistant.helpers.config_validation as cv

from .smartApp import SmartApp

from homeassistant.components.climate import PLATFORM_SCHEMA, ClimateEntity

from homeassistant.const import (
    TEMP_CELSIUS, ATTR_TEMPERATURE,
    CONF_USERNAME, CONF_PASSWORD
)

from homeassistant.components.climate.const import (
    HVAC_MODE_COOL, HVAC_MODE_HEAT, HVAC_MODE_HEAT_COOL, HVAC_MODE_DRY, HVAC_MODE_FAN_ONLY, HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE, SUPPORT_FAN_MODE, SUPPORT_SWING_MODE, SUPPORT_PRESET_MODE,
    PRESET_ECO, PRESET_NONE, PRESET_BOOST,
    ATTR_CURRENT_TEMPERATURE, ATTR_FAN_MODE,
    ATTR_HVAC_MODE, ATTR_SWING_MODE, ATTR_PRESET_MODE
)

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'panasonic_smart_app'

SCAN_INTERVAL = timedelta(seconds=300)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

PRESET_LIST = {
    # PRESET_NONE: 'Auto',
    # PRESET_BOOST: 'Powerful',
    # PRESET_ECO: 'Quiet'
}

SUPPORT_FLAGS = (
    SUPPORT_TARGET_TEMPERATURE
    # SUPPORT_FAN_MODE |
    # SUPPORT_PRESET_MODE |
    # SUPPORT_SWING_MODE
)

def tryApiStatus(func):
    def wrapper_call(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            args[0]._api.login()
            func(*args, **kwargs)
    return wrapper_call

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the panasonic cloud components."""
    _LOGGER.info('The panasonic_smart_app is setting up Platform.')
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    # _LOGGER.debug(f'The panasonic_smart_app info {username} {password}.')
    api = SmartApp(username, password)
    try:
        api.login()
    except:
        _LOGGER.error('Please Check Your UserName and Password.')
    else:
        devices = []
        for device in api.getDevices().get('GWList'):
            _LOGGER.debug(f'The panasonic_smart_app devices {device}.')
            devices.append(PanasonicDevice(device, api))
        add_entities(devices, True)
        _LOGGER.info('The panasonic_smart_app setup is done.')


class PanasonicDevice(ClimateEntity):
    def __init__(self, device, api):
        self._api = api
        self._commandList = api._devices['CommandList'][0]['JSON'][0]['list']
        self._device = device
        self._name = device['Devices'][0]['NickName']
        self._auth = device['auth']

        self._is_on = False
        self._hvac_mode = HVAC_MODE_COOL
        # self._current_fan = 'Auto'
        # self._airswing_hor = 'Auto'
        # self._airswing_vert = 'Auto'
        # self._eco = 'Auto'

        self._unit = TEMP_CELSIUS
        self._target_temperature = None
        self._current_temperature = None
        self._outside_temperature = None
        # self._mode = None
        # self._eco = 'Auto'
        # self._preset_mode = 'off'

    @tryApiStatus
    def update(self):
        _LOGGER.debug(f"------- UPDATING {self._name} -------")
        """Update the state of this climate device."""
        self._status = self._api.getDeviceInfo(self._device['auth'], options=['0x00', '0x01', '0x03', '0x04', '0x21'])
        _LOGGER.debug(f"Status: {self._status}")
        # _is_on
        self._is_on = bool(int(self._status.get('0x00')))
        _LOGGER.debug(f"_is_on: {self._is_on}")
        # _current_temperature
        self._target_temperature = float(self._status.get('0x03'))
        _LOGGER.debug(f"_current_temperature: {self._target_temperature}")

        self._current_temperature = float(self._status.get('0x04'))
        _LOGGER.debug(f"_current_temperature: {self._current_temperature}")

        self._outside_temperature = float(self._status.get('0x21'))
        _LOGGER.debug(f"_outside_temperature: {self._outside_temperature}")
        _LOGGER.debug(f"[{self._name}] is UPDATED.")

    @property
    def name(self):
        """Return the display name of this climate."""
        return self._name

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def hvac_mode(self):
        """Return the current operation."""
        if not self._is_on:
            return HVAC_MODE_OFF
        else:
            value = self._status.get('0x01')
            _LOGGER.debug(f"{self._name} hvac_mode is {value} - {self._api.taiSEIA.COMMANDS_OPTIONS.get('0x01').get(str(value))}")
            return self._api.taiSEIA.COMMANDS_OPTIONS.get('0x01').get(str(value))

    @property
    def hvac_modes(self):
        """Return the list of available operation modes."""
        avaiable_modes = list(filter(lambda x: x.get('CommandType') == '0x01', self._commandList))[0].get('Parameters')
        modes_list = [HVAC_MODE_OFF]
        for mode in avaiable_modes:
            modes_list.append(self._api.taiSEIA.COMMANDS_OPTIONS.get('0x01').get(str(mode[1])))
        return modes_list

    @tryApiStatus
    def set_hvac_mode(self, hvac_mode):
        _LOGGER.debug(f"{self._name} set_hvac_mode: {hvac_mode}")
        if hvac_mode == HVAC_MODE_OFF:
            self._api.setCommand(self._auth, 0, 0)
        else:
            options = self._api.taiSEIA.COMMANDS_OPTIONS.get('0x01')
            value = list(options.keys())[list(options.values()).index(hvac_mode)]
            self._api.setCommand(self._auth, 1, value)
            if not self._is_on:
                self._api.setCommand(self._auth, 0, 1)

    @property
    def preset_mode(self) -> Optional[str]:
        """Return the current preset mode, e.g., home, away, temp.
        Requires SUPPORT_PRESET_MODE.
        """
        # for key, value in PRESET_LIST.items():
            # if value == self._eco:
                # _LOGGER.debug("Preset mode is {0}".format(key))
                # return key


    @property
    def preset_modes(self) -> Optional[List[str]]:
        """Return a list of available preset modes.
        Requires SUPPORT_PRESET_MODE.
        """
        # _LOGGER.debug("Preset modes are {0}".format(",".join(PRESET_LIST.keys())))
        return []

    @property
    def fan_mode(self):
        """Return the fan setting."""
        return 'Auto'

    @property
    def fan_modes(self):
        """Return the list of available fan modes."""
        return []

    # def set_fan_mode(self, fan_mode):
        # """Set new fan mode."""
        # _LOGGER.debug("Set %s focus mode %s", self.name, fan_mode)

    @property
    def swing_mode(self):
        """Return the fan setting."""
        return None

    @property
    def swing_modes(self):
        """Return the list of available swing modes."""
        return ['Auto', 'Up', 'UpMid', 'Mid', 'DownMid', 'Down']

    # def set_swing_mode(self, swing_mode):
    #     """Set swing mode."""
    #     _LOGGER.debug("Set %s swing mode %s", self.name, swing_mode)

    @property
    def supported_features(self):
        """Return the list of supported features."""
        # _LOGGER.debug(f"SUPPORT_FLAGS {SUPPORT_FLAGS}")
        return SUPPORT_FLAGS

    @property
    def target_temperature(self):
        """Return the target temperature."""
        return self._target_temperature
    @property
    def outside_temperature(self):
        """Return the current temperature."""
        return self._outside_temperature

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temperature

    @tryApiStatus
    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        # if target_temp is None:
            # return
        _LOGGER.debug("Set %s temperature %s", self.name, target_temp)
        self._api.setCommand(self._auth, 3, int(target_temp))

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return 16

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return 30

    @property
    def target_temperature_step(self):
        """Return the temperature step."""
        return 1.0