import logging, requests, json
from pprint import pprint
import time

HOST = "https://ota-stage.owlting.com"

def api_call_login(func):
  print('api_call_login')
  def wrapper_call(*args, **kwargs):
      try:
          func(*args, **kwargs)
      except:
          print('error')
  return wrapper_call

@api_call_login
def test():
  print(time.time())
  r = requests.get("https://in.hotjar.com/api/v2/client/sites/2107935/visit-data?sv=7")
  r.raise_for_status()


# for i in range(10):
#   test()
#   time.sleep(1)
test()