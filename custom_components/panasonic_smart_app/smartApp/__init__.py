""" Panasonic Smart App API """
import json
from typing import Literal
import logging

from homeassistant.const import HTTP_OK
from .exceptions import (
    PanasonicRefreshTokenNotFound,
    PanasonicTokenExpired,
    PanasonicInvalidRefreshToken,
    PanasonicLoginFailed,
)
from .const import APP_TOKEN, HTTP_EXPECTATION_FAILED, EXCEPTION_INVALID_REFRESH_TOKEN
from . import urls

_LOGGER = logging.getLogger(__name__)


def tryApiStatus(func):
    async def wrapper_call(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except PanasonicTokenExpired:
            await args[0].refresh_token()
            return await func(*args, **kwargs)
        except (PanasonicInvalidRefreshToken, PanasonicLoginFailed, Exception):
            await args[0].login()
            return await func(*args, **kwargs)

    return wrapper_call


class SmartApp(object):
    def __init__(self, session, account, password):
        self.account = account
        self.password = password
        self._session = session
        self._devices = []
        self._commands = []

    async def login(self):
        _LOGGER.info("Attemping to login...")
        data = {"MemId": self.account, "PW": self.password, "AppToken": APP_TOKEN}
        response = await self.request(
            method="POST", headers={}, endpoint=urls.login(), data=data
        )

        self._refresh_token = response["RefreshToken"]
        self._cp_token = response["CPToken"]

    async def refresh_token(self):
        _LOGGER.info("Attemping to refresh token...")
        if self._refresh_token is None:
            raise PanasonicRefreshTokenNotFound

        data = {"RefreshToken": self._refresh_token}
        response = await self.request(
            method="POST", headers={}, endpoint=urls.refresh_token(), data=data
        )
        self._refresh_token = response["RefreshToken"]
        self._cp_token = response["CPToken"]

    @tryApiStatus
    async def get_devices(self):
        headers = {"cptoken": self._cp_token}
        response = await self.request(
            method="GET", headers=headers, endpoint=urls.get_devices()
        )

        self._devices = response["GWList"]
        self._commands = response["CommandList"]

        return self._devices

    def get_commands(self):
        return self._commands

    @tryApiStatus
    async def get_device_info(
        self, deviceId=None, options=["0x00", "0x01", "0x03", "0x04"]
    ):
        headers = {"cptoken": self._cp_token, "auth": deviceId}
        commands = {"CommandTypes": [], "DeviceID": 1}
        for option in options:
            commands["CommandTypes"].append({"CommandType": option})

        response = await self.request(
            method="POST",
            headers=headers,
            endpoint=urls.get_device_info(),
            data=[commands],
        )
        result = {}
        for device in response["devices"]:
            for info in device.get("Info"):
                command = info.get("CommandType")
                status = info.get("status")
                result[command] = status
        return result

    @tryApiStatus
    async def set_command(self, deviceId=None, command=0, value=0):
        headers = {"cptoken": self._cp_token, "auth": deviceId}
        payload = {"DeviceID": 1, "CommandType": command, "Value": value}

        await self.request(
            method="GET", headers=headers, endpoint=urls.set_command(), params=payload
        )
        return True

    async def request(
        self,
        method: Literal["GET", "POST"],
        headers,
        endpoint: str,
        params=None,
        data=None,
    ):
        """Shared request method"""

        resp = None

        _LOGGER.debug(f"Making request to {endpoint} with headers {headers}")
        async with self._session.request(
            method, url=endpoint, json=data, params=params, headers=headers
        ) as response:
            if response.status == HTTP_OK:
                try:
                    resp = await response.json()
                except:
                    resp = {}
            elif response.status == HTTP_EXPECTATION_FAILED:
                returned_raw_data = await response.text()
                _LOGGER.error(
                    "Failed to access API. Returned" " %d: %s",
                    response.status,
                    returned_raw_data,
                )
                try:
                    resp = await response.json()
                    if resp["StateMsg"] == EXCEPTION_INVALID_REFRESH_TOKEN:
                        raise PanasonicTokenExpired
                    else:
                        raise PanasonicLoginFailed
                except:
                    raise PanasonicInvalidRefreshToken

            else:
                _LOGGER.error(
                    "Failed to access API. Returned" " %d: %s",
                    response.status,
                    await response.text(),
                )

        return resp
