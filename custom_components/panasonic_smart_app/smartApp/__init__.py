""" Panasonic Smart App API """
import logging, requests, json
from pprint import pprint
from . import urls
# from .secrets import *
from . import _taiseia as taiSEIA

_LOGGER = logging.getLogger(__name__)

APP_TOKEN = 'D8CBFF4C-2824-4342-B22D-189166FEF503'

class SmartApp(object):
  def __init__(self, account, password):
    self.host = 'https://ems2.panasonic.com.tw/api'
    self.account = account
    self.password = password
    self.app_token = APP_TOKEN
    self.taiSEIA = taiSEIA

  def login(self):
    data = {
      'MemId': self.account,
      'PW': self.password,
      'AppToken': self.app_token
    }
    response = requests.post(urls.login(), json = data)
    response.raise_for_status()
    # print(response.json().get('CPToken'))
    self.CPToken = response.json().get('CPToken')
    self.header = {
      'Content-Type': 'application/json',
      'CPToken': self.CPToken
    }

  def getDevices(self):
    response = requests.get(urls.getDevices(), headers = self.header)
    response.raise_for_status()
    _LOGGER.debug(f"[getDevices {response.status_code}] - {response.json()}")
    self._devices = response.json()
    return self._devices

  def getDeviceInfo(self, deviceId=None, options=['0x00', '0x01', '0x03', '0x04']):
    self.header.update({
      'auth': deviceId
    })
    commands = {
      "CommandTypes": [],
      "DeviceID": 1
    }
    for option in options:
      commands['CommandTypes'].append({ "CommandType": option })

    response = requests.post(urls.getDeviceInfo(), headers = self.header, json = [commands])
    response.raise_for_status()
    result = {}
    if (response.status_code == 200):
      for device in response.json().get('devices', []):
        for info in device.get('Info'):
          command = info.get('CommandType')
          status = info.get('status')
          result[command] = status
    return result

  def setCommand(self, deviceId=None, command=0, value=0):
    self.header.update({
      'auth': deviceId
    })
    payload = {
      "DeviceID": 1,
      "CommandType": command,
      "Value": value
    }
    response = requests.get(urls.setCommand(), headers = self.header, params = payload)
    response.raise_for_status()
    # pprint(vars(response))
    return True
