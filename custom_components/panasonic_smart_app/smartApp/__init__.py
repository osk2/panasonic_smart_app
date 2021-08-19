""" Panasonic Smart App API """
from typing import Literal
from datetime import datetime
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
    COMMANDS_PER_REQUEST,
    HTTP_EXPECTATION_FAILED,
    HTTP_TOO_MANY_REQUESTS,
    EXCEPTION_COMMAND_NOT_FOUND,
    EXCEPTION_INVALID_REFRESH_TOKEN,
)
from .utils import chunks
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
        except (
            PanasonicDeviceOffline,
            PanasonicExceedRateLimit,
            Exception,
        ) as exception:
            _LOGGER.info(exception)
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

        self._devices = response["GwList"]
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
        device = response.get("devices")[0]
        for info in device.get("Info"):
            command = info.get("CommandType")
            status = info.get("status")
            result[command] = status
        return result

    async def get_device_overview(self):
        headers = {"cptoken": self._cp_token}
        response = await self.request(
            method="GET",
            headers=headers,
            endpoint=urls.get_device_overview(),
        )
        result = {}
        for device in response.get("GwList"):
            for info in device.get("List"):
                command = info.get("CommandType")
                status = info.get("Status")
                result[command] = status
        return result

    async def get_device_with_info(self, status_code_mapping: dict):

        devices = await self.get_devices()
        energy_report = await self.get_energy_report()
        device_overview = await self.get_device_overview()

        for device in devices:
            device_type = int(device.get("DeviceType"))
            device["energy"] = energy_report.get(device.get("GWID"))
            if device_type in status_code_mapping.keys():
                status_codes = chunks(
                    status_code_mapping[device_type], COMMANDS_PER_REQUEST
                )
                device["status"] = {}
                for codes in status_codes:
                    try:
                        device["status"].update(
                            await self.get_device_info(device.get("Auth"), codes)
                        )
                    except PanasonicExceedRateLimit:
                        _LOGGER.info("超量使用 API，目前功能將受限制")
                        device["status"].update(device_overview.get(device.get("GWID")))
                        break

        return devices

    async def get_energy_report(self):
        headers = {"cptoken": self._cp_token}
        payload = {
            "name": "Power",
            "from": datetime.today().replace(day=1).strftime("%Y/%m/%d"),
            "unit": "day",
            "max_num": 31,
        }
        response = await self.request(
            method="POST",
            headers=headers,
            endpoint=urls.get_energy_report(),
            data=payload,
        )
        result = {}
        for device in response.get("GwList"):
            result[device.get("GwID")] = float(device.get("Total_kwh"))
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
        _LOGGER.debug(
            f"Making request to {endpoint} with headers {headers} and data {data}"
        )
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
            auth = headers.get("auth")
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
            resp = await response.json()

            if resp.get("StateMsg") == EXCEPTION_COMMAND_NOT_FOUND:
                auth = headers.get("auth")
                if auth:
                    device = list(
                        filter(lambda device: device["auth"] == auth, self._devices)
                    )
                    raise PanasonicDeviceOffline(
                        f"{device[0]['Devices'][0]['NickName']} is offline. Retry later..."
                    )
                else:
                    raise PanasonicDeviceOffline
            elif resp.get("StateMsg") == EXCEPTION_INVALID_REFRESH_TOKEN:
                raise PanasonicTokenExpired
            else:
                _LOGGER.error(
                    "Failed to access API. Returned" " %d: %s",
                    response.status,
                    await response.text(),
                )
                raise PanasonicLoginFailed
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
