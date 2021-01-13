""" Panasonic Smart App API """
import logging, requests, json, pprint
from . import urls
from .secrets import *

class SmartApp(object):
  def __init__(self, username_or_access_token=None, password=None):
    self.host = 'https://ems2.panasonic.com.tw/api'
    self.account = ACCOUNT
    self.password = PASSWORD
    self.app_token = APP_TOKEN

  def login(self):
    response = requests.post(urls.login(), json = {
      'MemId': self.account,
      'PW': self.password,
      'AppToken': self.app_token
    })
    response.raise_for_status()
    self.token = response.json()['CPToken']
    # print('[Login]', self.token)

  def getDevices(self):
    self.headers = {
      'cptoken': self.token
    }
    response = requests.get(urls.getDevices(), headers = self.headers)
    response.raise_for_status()
    self.devices = response.json()['GWList']
    # print('[getDevices]', self.devices)
    return self.devices
