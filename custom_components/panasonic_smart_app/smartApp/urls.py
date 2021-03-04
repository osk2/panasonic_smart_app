""" Panasonic Smart App API """

from .const import BASE_URL


def login():
    url = f"{BASE_URL}/Userlogin1"
    return url


def getDevices():
    url = f"{BASE_URL}/UserGetRegisteredGWList1"
    return url


def getDeviceInfo():
    url = f"{BASE_URL}/DeviceGetInfo"
    return url


def setCommand():
    url = f"{BASE_URL}/DeviceSetCommand"
    return url
