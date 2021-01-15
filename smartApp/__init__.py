""" Panasonic Smart App API """
import logging, requests, json
from pprint import pprint
from . import urls
from .secrets import *

class SmartApp(object):
  def __init__(self, account=None, password=None, app_token=None):
    self.host = 'https://ems2.panasonic.com.tw/api'
    self.account = ACCOUNT
    self.password = PASSWORD
    self.app_token = APP_TOKEN

  def login(self):
    data = {
      'MemId': self.account,
      'PW': self.password,
      'AppToken': self.app_token
    }
    response = requests.post(urls.login(), json = data)
    response.raise_for_status()
    self.headers = {
      'cptoken': response.json()['CPToken']
    }
    pprint('[Login]')
    pprint(self.headers)

  def getDevices(self):
    response = requests.get(urls.getDevices(), headers = self.headers)
    response.raise_for_status()
    self.devices = response
    pprint('[getDevices]')
    pprint(vars(response))
    return self

  def getDeviceInfo():
    # urls.getDeviceInfo()
    pprint('[getDeviceInfo]')

  def setCommand():
    # urls.setCommand()
    pprint('[setCommand]')
