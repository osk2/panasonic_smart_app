""" Panasonic Smart App API """

from .const import BASE_URL


def login():
    url = f"{BASE_URL}/userlogin1"
    return url


def get_devices():
    url = f"{BASE_URL}/UserGetRegisteredGwList2"
    return url


def get_device_info():
    url = f"{BASE_URL}/DeviceGetInfo"
    return url


def get_energy_report():
    url = f"{BASE_URL}/UserGetInfo"
    return url


def get_device_overview():
    url = f"{BASE_URL}/UserGetDeviceStatus"
    return url


def set_command():
    url = f"{BASE_URL}/DeviceSetCommand"
    return url


def refresh_token():
    url = f"{BASE_URL}/RefreshToken1"
    return url
