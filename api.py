""" Panasonic Smart App API """
import logging, requests, json, pprint
import voluptuous as vol

def test(hass, config):
  username = config.get(CONF_USERNAME)
  password = config.get(CONF_PASSWORD)
  print(username, password)

# test()

# logging.basicConfig(level=logging.DEBUG)

# BASE_URL = 'https://ems2.panasonic.com.tw/api'

# def login():
#   global ACCESS_TOKEN
#   url = f'{BASE_URL}/userlogin1'
#   res = requests.post(url, json = {
#     'MemId': ACCOUNT,
#     'PW': PASSWORD,
#     'AppToken': APP_TOKEN
#   })
#   logging.debug(res.json())
#   ACCESS_TOKEN = res.json()['CPToken']

# def getDevices():
#   HEADERS = {
#     'cptoken': ACCESS_TOKEN
#   }
#   url = f'{BASE_URL}/UserGetRegisteredGWList1'
#   res = requests.get(url, headers = HEADERS)
#   pprint.pprint(res.json())

# def getDevice():
#   HEADERS = {
#     'Content-Type': 'application/json',
#     'cptoken': ACCESS_TOKEN,
#     'auth': deviceAuth
#   }
#   return f'{BASE_URL}/DeviceGetInfo'

# def setCommand():
#   HEADERS = {
#     'cptoken': ACCESS_TOKEN
#   }
#   QUERY = {
#     'DeviceId': DeviceID,
#     'CommandType': CommandType,
#     'Value': Value
#   }
#   return f'{BASE_URL}/DeviceSetCommand'

# login()
# print('ACCESS_TOKEN', ACCESS_TOKEN)
# getDevices()
