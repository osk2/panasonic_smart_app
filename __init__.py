"""
panasonic_smart_app
climate:
  - platform: panasonic_smart_app
    username: test_username
    password: test_password
    access_token: test_access_token
"""
import logging
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
  _LOGGER.debug('The panasonic_smart_app is setup.')
  return True
