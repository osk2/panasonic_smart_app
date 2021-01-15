""" Panasonic Smart App API """
# import logging, requests, json
from pprint import pprint
# import voluptuous as vol

from smartApp import SmartApp
api = SmartApp('account', 'password', 'token')
api.login()
api.getDevices()
api.getDeviceInfo()
api.setCommand()