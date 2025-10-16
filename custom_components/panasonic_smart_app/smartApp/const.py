BASE_URL = "https://ems2.panasonic.com.tw/api"
APP_TOKEN = "D8CBFF4C-2824-4342-B22D-189166FEF503"
USER_AGENT = "okhttp/4.9.1"

SECONDS_BETWEEN_REQUEST = 2
REQUEST_TIMEOUT = 20
COMMANDS_PER_REQUEST = 6

EXCEPTION_COMMAND_NOT_FOUND = "無法透過CommandId取得Commmand"
EXCEPTION_DEVICE_OFFLINE = "deviceOffline"
EXCEPTION_DEVICE_NOT_RESPONDING = "deviceNoResponse"
EXCEPTION_DEVICE_JP_INFO = "503:DeviceJPInfo:aStatusCode"
EXCEPTION_DEVICE_JP_FAILED = ":DeviceJPInfo:GetCommandTransResult failed"
EXCEPTION_TOKEN_EXPIRED = "無法依據您的CPToken,auth取得相關資料"
EXCEPTION_INVALID_REFRESH_TOKEN = "無效RefreshToken"
EXCEPTION_CPTOKEN_EXPIRED = "此CPToken已經逾時"
EXCEPTION_REACH_RATE_LIMIT = "系統檢測您當前超量使用"

DEHUMIDIFIER_COMMANDTYPES_PARAMETERS_XLATE_LOOKUP = [
  { "type": "0x00", "name": "Power", "parameters": [
      [ "Off", 0 ],
      [ "On", 1 ],
    ],
  },
  { "type": "0x01", "name": "Mode", "parameters": [
      [ "Continuous dehumidification",  0 ],
      [ "Automatic dehumidification",   1 ],
      [ "Anti-mildew",                  2 ],
      [ "Fan mode",                     3 ],
      [ "ECONAVI",                      4 ],
      [ "Keep dry",                     5 ],
      [ "Target humidity",              6 ],
      [ "Air purification",             7 ],
      [ "AI comfort",                   8 ],
      [ "Energy saving",                9 ],
      [ "Quick dehumidication",         10 ],
      [ "Silent dehumidification",      11 ],
      [ "Shoe drying",                  12 ],
    ],
  },
  { "type": "0x02", "name": "Off timer", "parameters": [], },
  { "type": "0x04", "name": "Target humidity", "parameters": [
      [ "40%", 0 ],
      [ "45%", 1 ],
      [ "50%", 2 ],
      [ "55%", 3 ],
      [ "60%", 4 ],
      [ "65%", 5 ],
      [ "70%", 6 ],
    ],
  },
  { "type": "0x09", "name": "Swing", "parameters": [
      [ "Fixed",    0 ],
      [ "Downward", 1 ],
      [ "Upward",   2 ],
      [ "Swing",    3 ],
    ],
  },
  { "type": "0x0d", "name": "nanoe", "parameters": [
      [ "Off", 0 ],
      [ "On",  1 ],
    ],
  },
  { "type": "0x0e", "name": "Fan speed", "parameters": [
      [ "Auto",   0 ],
      [ "Silent", "靜音" ],
      [ "Normal", "標準" ],
      [ "High",   "急速" ],
    ],
  },
  { "type": "0x18", "name": "Buzzer", "parameters": [
      [ "On",   0 ],
      [ "Off",  1 ],
    ],
  },
  { "type": "0x55", "name": "On timer", "parameters": [], },
  { "type": "0x59", "name": "Mildew prevention", "parameters": [
      [ "Off",  0 ],
      [ "On",   1 ],
    ],
  },
]

