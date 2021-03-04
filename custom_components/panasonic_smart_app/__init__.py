import logging
from .smartApp import SmartApp
from .const import DOMAIN, PLATFORMS
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
)

"""
panasonic_smart_app:
  username: !secret smart_app_username
  password: !secret smart_app_password
"""

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    username = config[DOMAIN][CONF_USERNAME]
    password = config[DOMAIN][CONF_PASSWORD]
    api = SmartApp(username, password)

    hass.data[DOMAIN] = {"api": api}

    for p in PLATFORMS:
        hass.helpers.discovery.load_platform(p, DOMAIN, {}, config)

    return True
