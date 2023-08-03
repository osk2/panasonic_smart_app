""" Panasonic Smart App API """
from typing import Literal
from datetime import datetime
from collections import defaultdict
from http import HTTPStatus
import asyncio
import logging

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
    EXCEPTION_DEVICE_OFFLINE,
    EXCEPTION_DEVICE_NOT_RESPONDING,
    EXCEPTION_INVALID_REFRESH_TOKEN,
    EXCEPTION_DEVICE_JP_INFO,
    EXCEPTION_DEVICE_JP_FAILED,
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
        except PanasonicExceedRateLimit:
            """ Fallback to use overview API """
            raise PanasonicExceedRateLimit
        except (
            PanasonicDeviceOffline,
            Exception,
        ) as exception:
            _LOGGER.warning(exception)
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
    def __init__(self, session, account, password, proxy=None):
        self.account = account
        self.password = password
        self._proxy = proxy
        self._session = session
        self._devices = []
        self._commands = []
        self.last_request_id = 0

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
        self, deviceId=None, gwid=None, options=["0x00", "0x01", "0x03", "0x04"]
    ):
        headers = {
          "cptoken": self._cp_token,
          "auth": deviceId,
          "gwid": gwid
        }
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

    async def get_overview(self):
        headers = {"cptoken": self._cp_token}
        response = await self.request(
            method="GET",
            headers=headers,
            endpoint=urls.get_device_overview(),
        )

        result = defaultdict(dict)
        for device in response.get("GwList"):
            for info in device.get("List"):
                command = info.get("CommandType")
                status = info.get("Status")
                result[device.get("GWID")][command] = status
        return result

    async def get_device_with_info(self, status_code_mapping: dict):

        devices = await self.get_devices() or []
        energy_report = await self.get_energy_report()

        async def get_device_overview(gwid: str):
            all_device_overview = await self.get_overview() or {}
            device_overview = all_device_overview.get(gwid, {})
            if device_overview and "" in list(dict(device_overview).values()):
                """ Retry if API return empty status for current device """
                return await get_device_overview(gwid)
            else:
                return device_overview

        for device in devices:
            device_type = int(device.get("DeviceType"))
            gwid = device.get("GWID")
            device["energy"] = energy_report.get(gwid)
            if device_type in status_code_mapping.keys():
                status_codes = status_code_mapping[device_type]
                device["status"] = {}
                try:
                    info = await self.get_device_info(device.get("Auth"), gwid, status_codes)
                    device["status"].update(info)
                except PanasonicExceedRateLimit:
                    _LOGGER.warning(
                        "超量使用 API，功能將受限制，詳見 https://github.com/osk2/panasonic_smart_app/discussions/31"
                    )
                    overview = await get_device_overview(gwid)
                    target_device = list(
                        filter(lambda d: d["GWID"] == gwid, self._devices)
                    )
                    _LOGGER.debug(
                        f"[{target_device[0]['NickName']}] overview: {overview}"
                    )
                    device["status"].update(overview)
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
        request_id = self.last_request_id + 1
        self.last_request_id = request_id
        headers["user-agent"] = USER_AGENT
        _LOGGER.debug(
            f"Making #{request_id} request to {endpoint} with headers {headers} and data {data}, proxy: {self._proxy}"
        )
        try:
            response = await self._session.request(
                method,
                url=endpoint,
                json=data,
                params=params,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
                proxy=self._proxy,
            )
        except:
            auth = headers.get("auth", None)
            if auth:
                device = list(
                    filter(lambda device: device["Auth"] == auth, self._devices)
                )
                raise PanasonicDeviceOffline(
                    f"無法連線至\"{device[0]['NickName']}\"，將於下輪更新時重試"
                )
            else:
                raise PanasonicDeviceOffline(f"無法連線至裝置，將於下輪更新時重試")

        if response.status == HTTPStatus.OK:
            try:
                resp = await response.json()
                _LOGGER.debug(
                    "Succeed to access #%d API. Returned" " %d: %s",
                    request_id,
                    response.status,
                    await response.text(),
                )
            except:
                resp = {}
        elif response.status == HTTPStatus.EXPECTATION_FAILED:
            resp = {}
            try:
                resp = await response.json()
            except:
                """ Invalid CPToken or something else """
                raise PanasonicLoginFailed

            offline_exceptions = [
              EXCEPTION_DEVICE_OFFLINE,
              EXCEPTION_DEVICE_NOT_RESPONDING,
              EXCEPTION_DEVICE_JP_INFO,
              EXCEPTION_DEVICE_JP_FAILED,
            ]
            if resp.get("StateMsg") in offline_exceptions:
                auth = headers.get("auth", None)
                if auth:
                    device = list(
                        filter(lambda device: device["Auth"] == auth, self._devices)
                    )
                    raise PanasonicDeviceOffline(
                        f"無法連線至\"{device[0]['NickName']}\"，將於下輪更新時重試"
                    )
                else:
                    raise PanasonicDeviceOffline(f"無法連線至裝置，將於下輪更新時重試")

            elif resp.get("StateMsg") == EXCEPTION_INVALID_REFRESH_TOKEN:
                raise PanasonicTokenExpired
            else:
                _LOGGER.error(
                    "Failed to access #%d API. Returned" " %d: %s",
                    request_id,
                    response.status,
                    await response.text(),
                )
                raise PanasonicLoginFailed

        elif response.status == HTTPStatus.TOO_MANY_REQUESTS:
            raise PanasonicExceedRateLimit
        else:
            _LOGGER.error(
                "Failed to access #%d API. Returned" " %d: %s",
                request_id,
                response.status,
                await response.text(),
            )

        return resp
