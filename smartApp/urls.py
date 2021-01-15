""" Panasonic Smart App API """
BASE_URL = 'https://ems2.panasonic.com.tw/api'

def login():
  url = f'{BASE_URL}/userlogin1'
  return url

def getDevices():
  url = f'{BASE_URL}/UserGetRegisteredGWList1'
  return url

def getDeviceInfo():
  url = f'{BASE_URL}/DeviceGetInfo'
  return url

def setCommand():
  url = f'{BASE_URL}/DeviceSetCommand'
  return url