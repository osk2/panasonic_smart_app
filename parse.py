import json
from pprint import pprint
RESPONSE = [{'GWID': 'B8B7F120F1BF', 'NickName': '', 'auth': 'B8B7F120F1BF9E60E913DA5D78AAAB9E79706C1457B3', 'HSType': 'S', 'ModelID': 'CZ-T006', 'City': '新北市', 'Area': '中和區', 'Devices': [{'DeviceID': 1, 'NickName': '客臥冷氣', 'DeviceType': 1, 'AreaID': 0, 'ModelType': 'PXGD', 'Model': 'CS-PX28FA2'}]}, {'GWID': 'B8B7F120F1D1', 'NickName': '', 'auth': 'B8B7F120F1D19E60E913DA5D78AAAB9E79706C1457B3', 'HSType': 'S', 'ModelID': 'CZ-T006', 'City': '新北市', 'Area': '中和區', 'Devices': [{'DeviceID': 1, 'NickName': '客廳冷氣', 'DeviceType': 1, 'AreaID': 0, 'ModelType': 'PXGD', 'Model': 'CS-PX50FA2'}]}, {'GWID': 'B8B7F120F1DF', 'NickName': '', 'auth': 'B8B7F120F1DF9E60E913DA5D78AAAB9E79706C1457B3', 'HSType': 'S', 'ModelID': 'CZ-T006', 'City': '新北市', 'Area': '中和區', 'Devices': [{'DeviceID': 1, 'NickName': '主臥冷氣', 'DeviceType': 1, 'AreaID': 0, 'ModelType': 'PXGD', 'Model': 'CS-PX28FA2'}]}]

LIST = []

class SmartAppDevice(object):
  def __init__(self, auth, device):
    self.name = device['NickName']
    self.auth = auth
    self.model = device['Model']
    pprint(vars(self))
    LIST.append(self)

for group in RESPONSE:
  AUTH = group['auth']
  # pprint(f"GWID: {group['GWID']}")
  # pprint(f"auth: {group['auth']}")
  for device in group['Devices']:
    # pprint(device, indent = 2)
    SmartAppDevice(AUTH, device)
  pprint('---------------------------------------')

# for device in LIST:
#   pprint(vars(device), indent = 2)