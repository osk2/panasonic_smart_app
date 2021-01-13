""" Panasonic Smart App API """
import logging, requests, json, pprint

BASE_URL = 'https://ems2.panasonic.com.tw/api'

def login():
  url = f'{BASE_URL}/userlogin1'
  return url

def getDevices():
  url = f'{BASE_URL}/UserGetRegisteredGWList1'
  return url