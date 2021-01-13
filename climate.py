import logging
import voluptuous as vol
from typing import Any, Dict, Optional, List
from datetime import timedelta
import homeassistant.helpers.config_validation as cv

from homeassistant.components.climate import PLATFORM_SCHEMA, ClimateEntity

from homeassistant.const import (
    TEMP_CELSIUS, ATTR_TEMPERATURE,
    CONF_ACCESS_TOKEN, CONF_USERNAME, CONF_PASSWORD
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
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_ACCESS_TOKEN): cv.string
})

OPERATION_LIST = {
    HVAC_MODE_OFF: 'Off',
    HVAC_MODE_HEAT: 'Heat',
    HVAC_MODE_COOL: 'Cool',
    HVAC_MODE_HEAT_COOL: 'Auto',
    HVAC_MODE_DRY: 'Dry',
    HVAC_MODE_FAN_ONLY: 'Fan'
}

PRESET_LIST = {
    PRESET_NONE: 'Auto',
    PRESET_BOOST: 'Powerful',
    PRESET_ECO: 'Quiet'
}

SUPPORT_FLAGS = (
    SUPPORT_TARGET_TEMPERATURE |
    SUPPORT_FAN_MODE |
    SUPPORT_PRESET_MODE |
    SUPPORT_SWING_MODE
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the panasonic cloud components."""
    _LOGGER.debug('The panasonic_smart_app is setting up Platform.')
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    devices = []
    devices.append(PanasonicDevice())
    add_entities(devices, True)


class PanasonicDevice(ClimateEntity):
    def __init__(self):
        # self._api = api
        # self._device = device
        # self._constants = constants
        # self._current_temp = None
        self._name = 'panasonic_test'
        self._is_on = False
        self._hvac_mode = 'Off'
        self._current_fan = 'Auto'
        self._airswing_hor = 'Auto'
        self._airswing_vert = 'Auto'
        self._eco = 'Auto'

        self._unit = TEMP_CELSIUS
        self._target_temp = None
        self._cur_temp = None
        self._outside_temp = None
        self._mode = None
        self._eco = 'Auto'
        self._preset_mode = 'off'

    @property
    def name(self):
        """Return the display name of this climate."""
        return 'panasonic_test'

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def hvac_mode(self):
        """Return the current operation."""
        return HVAC_MODE_OFF

    @property
    def hvac_modes(self):
        """Return the list of available operation modes."""
        return list(OPERATION_LIST.keys())

    @property
    def preset_mode(self) -> Optional[str]:
        """Return the current preset mode, e.g., home, away, temp.
        Requires SUPPORT_PRESET_MODE.
        """
        for key, value in PRESET_LIST.items():
            if value == self._eco:
                _LOGGER.debug("Preset mode is {0}".format(key))
                return key


    @property
    def preset_modes(self) -> Optional[List[str]]:
        """Return a list of available preset modes.
        Requires SUPPORT_PRESET_MODE.
        """
        _LOGGER.debug("Preset modes are {0}".format(",".join(PRESET_LIST.keys())))
        return list(PRESET_LIST.keys())

    @property
    def fan_mode(self):
        """Return the fan setting."""
        return 'Auto'

    @property
    def fan_modes(self):
        """Return the list of available fan modes."""
        return SUPPORT_FAN_MODE

    @property
    def swing_mode(self):
        """Return the fan setting."""
        return None

    @property
    def swing_modes(self):
        """Return the list of available swing modes."""
        return SUPPORT_SWING_MODE

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS