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
    DEHUMIDIFIER_COMMANDTYPES_PARAMETERS_XLATE_LOOKUP,
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
            method="POST", headers={}, endpoint=urls.login(), data=data, log=False
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

        try:
            # walk through 'CommandList' as an actual list so we can change the contents in-place
            for ci in range(0, len(self._commands)):
                if self._commands[ci]["JSON"][0]["DeviceType"] == 4: #DEVICE_TYPE_DEHUMIDIFIER:
                    # walk through ...['list'] as an actual list so we can change the contents in-place
                    for li in range(0, len(self._commands[ci]["JSON"][0]["list"])):
                        ctype = self._commands[ci]["JSON"][0]["list"][li]["CommandType"]
                        cname = self._commands[ci]["JSON"][0]["list"][li]["CommandName"] # pre-translation name

                        # find the entry in the translation lookup table that matches the 'CommandType'
                        xlate_lookup = next(filter(lambda x: x["type"] == ctype.lower(), DEHUMIDIFIER_COMMANDTYPES_PARAMETERS_XLATE_LOOKUP), None)

                        if (xlate_lookup is not None):
                            # overwrite 'CommandName' with the translation we were able to find
                            self._commands[ci]["JSON"][0]["list"][li]["CommandName"] = xlate_lookup["name"]
                            _LOGGER.debug(f"Translating: type:'{ctype}' name:'{cname}' => '{xlate_lookup['name']}'")

                            # walk through ...['Parameters'] as an actual list so we can change the contents in-place
                            for pi in range(0, len(self._commands[ci]["JSON"][0]["list"][li]["Parameters"])):
                                pvalue = self._commands[ci]["JSON"][0]["list"][li]["Parameters"][pi][0] # pre-translation name for the parameter value
                                penum = self._commands[ci]["JSON"][0]["list"][li]["Parameters"][pi][1]

                                # find the entry in the translation lookup table entry that matched with the 'CommandType' and  'Parameter' enum
                                param_xlate_lookup = next(filter(lambda x: x[1] == penum, xlate_lookup["parameters"]), None)

                                if (param_xlate_lookup is None):
                                    param_xlate_lookup = next(filter(lambda x: x[1] == pvalue, xlate_lookup["parameters"]), None)

                                if (param_xlate_lookup is not None):
                                    # overwrite the name of the parameter value with the translation we were able to find
                                    self._commands[ci]["JSON"][0]["list"][li]["Parameters"][pi][0] = param_xlate_lookup[0]
                                    _LOGGER.debug(f"Translating: parameter:['{pvalue}', '{penum}'] => ['{self._commands[ci]["JSON"][0]["list"][li]["Parameters"][pi][0]}', '{self._commands[ci]["JSON"][0]["list"][li]["Parameters"][pi][1]}']")

            _LOGGER.debug(f"After translating: self._commands={self._commands}")
        except Exception as e:
            _LOGGER.error(f"While trying to translate command and parameter values: {e}")

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
        # Call APIs concurrently
        get_device_task = asyncio.create_task(self.get_devices())
        get_energy_report_task = asyncio.create_task(self.get_energy_report())
        get_co2_report_task = asyncio.create_task(self.get_co2_report())
        get_ref_open_door_report_task = asyncio.create_task(self.get_ref_open_door_report())

        devices = await get_device_task or []
        energy_report = await get_energy_report_task
        co2_report = await get_co2_report_task
        ref_open_door_report = await get_ref_open_door_report_task

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
            device["co2"] = co2_report.get(gwid)
            device["ref_open_door"] = ref_open_door_report.get(gwid)

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

    async def get_energy_report(self) -> dict[str, float]:
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
            endpoint=urls.get_info(),
            data=payload,
        )
        result = {}
        for device in response.get("GwList"):
            result[device.get("GwID")] = float(device.get("Total_kwh"))
        return result

    async def get_co2_report(self) -> dict[str, float]:
        """Get CO2 report for current month"""
        headers = {"cptoken": self._cp_token}
        payload = {
            "name": "CO2",
            "from": datetime.today().replace(day=1).strftime("%Y/%m/%d"),
            "unit": "day",
            "max_num": 31,
        }
        response = await self.request(
            method="POST",
            headers=headers,
            endpoint=urls.get_info(),
            data=payload,
        )

        try:
            gw_list = response["GwList"]
        except KeyError:
            _LOGGER.info("No CO2 data available")
            return {}

        result = {}
        for index, device in enumerate(gw_list):
            try:
                gw_id = device["GwID"]
            except KeyError:
                _LOGGER.info(f"No CO2 data available for device {index}")
                continue

            try:
                co2 = float(device["Total_kg"])
            except KeyError:
                _LOGGER.info(f"No CO2 data available for device {index}")
                continue
            except ValueError:
                _LOGGER.warning(
                    f"Invalid CO2 data {device['Total_kg']} for device {index}"
                )
                continue

            result[gw_id] = co2

        return result

    async def get_ref_open_door_report(self) -> dict[str, int]:
        """Get refrigerator open door report for current month"""

        # TODO: Response from "Other" may contain reports other than
        #       Ref_OpenDoor_Total. Make it more generic to handle
        #       other reports when we know what they are.

        headers = {"cptoken": self._cp_token}
        payload = {
            "name": "Other",
            "from": datetime.today().replace(day=1).strftime("%Y/%m/%d"),
            "unit": "day",
            "max_num": 31,
        }
        response = await self.request(
            method="POST",
            headers=headers,
            endpoint=urls.get_info(),
            data=payload,
        )

        try:
            gw_list = response["GwList"]
        except KeyError:
            _LOGGER.info("No refrigerator open door data available")
            return {}

        report = {}
        for index, device in enumerate(gw_list):
            try:
                gw_id = device["GwID"]
            except KeyError:
                _LOGGER.info(
                    f"No refrigerator open door data available for device {index}"
                )
                continue

            try:
                open_door = int(device["Ref_OpenDoor_Total"])
            except KeyError:
                _LOGGER.info(
                    f"No refrigerator open door data available for device {index}"
                )
                continue
            except ValueError:
                _LOGGER.warning(
                    "Invalid refrigerator open door data "
                    f"{device['Ref_OpenDoor_Total']} for device {index}"
                )
                continue

            report[gw_id] = open_door

        return report

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
        log=True,
    ):
        """Shared request method"""

        resp = None
        request_id = self.last_request_id + 1
        self.last_request_id = request_id
        headers["user-agent"] = USER_AGENT
        if log:
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
                if log:
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
