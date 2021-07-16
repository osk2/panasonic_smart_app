""" Panasonic Smart App API """
from typing import Literal
import asyncio
import logging

from homeassistant.const import HTTP_OK
from .exceptions import (
    PanasonicRefreshTokenNotFound,
    PanasonicTokenExpired,
    PanasonicInvalidRefreshToken,
    PanasonicLoginFailed,
    PanasonicDeviceOffline,
    PanasonicExceedRateLimit,
)
from .const import (
    APP_TOKEN,
    USER_AGENT,
    SECONDS_BETWEEN_REQUEST,
    REQUEST_TIMEOUT,
    HTTP_EXPECTATION_FAILED,
    HTTP_TOO_MANY_REQUESTS,
    EXCEPTION_COMMAND_NOT_FOUND,
    EXCEPTION_INVALID_REFRESH_TOKEN,
)
from . import urls

_LOGGER = logging.getLogger(__name__)


def tryApiStatus(func):
    async def wrapper_call(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except PanasonicTokenExpired:
            await args[0].refresh_token()
            return await func(*args, **kwargs)
        except (PanasonicInvalidRefreshToken, PanasonicLoginFailed):
            await args[0].login()
            return await func(*args, **kwargs)
        except (PanasonicDeviceOffline, Exception) as exception:
            _LOGGER.info(exception.message)
            return {}

    return wrapper_call


def delay(func):
    async def wrapper_call(*args, **kwargs):
        results = await asyncio.gather(
            *[func(*args, **kwargs), asyncio.sleep(SECONDS_BETWEEN_REQUEST)]
        )
        return results[0]

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

    @delay
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
        headers["user-agent"] = USER_AGENT
        _LOGGER.debug(f"Making request to {endpoint} with headers {headers}")
        try:
            response = await self._session.request(
                method,
                url=endpoint,
                json=data,
                params=params,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )
        except:
            auth = headers["auth"] or None
            if auth:
                device = list(
                    filter(lambda device: device["auth"] == auth, self._devices)
                )
                raise PanasonicDeviceOffline(
                    f"{device[0]['Devices'][0]['NickName']} is offline. Retry later..."
                )
            else:
                raise PanasonicDeviceOffline

        if response.status == HTTP_OK:
            try:
                resp = await response.json()
            except:
                resp = {}
        elif response.status == HTTP_EXPECTATION_FAILED:
            returned_raw_data = await response.text()

            if returned_raw_data == EXCEPTION_COMMAND_NOT_FOUND:
                auth = headers["auth"]
                if auth:
                    device = list(
                        filter(lambda device: device["auth"] == auth, self._devices)
                    )
                    raise PanasonicDeviceOffline(
                        f"{device[0]['Devices'][0]['NickName']} is offline. Retry later..."
                    )
                else:
                    raise PanasonicDeviceOffline
            else:
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
        elif response.status == HTTP_TOO_MANY_REQUESTS:
            _LOGGER.error(
                "Failed to access API. Returned" " %d: %s",
                response.status,
                await response.text(),
            )
            raise PanasonicExceedRateLimit
        else:
            _LOGGER.error(
                "Failed to access API. Returned" " %d: %s",
                response.status,
                await response.text(),
            )

        return resp
