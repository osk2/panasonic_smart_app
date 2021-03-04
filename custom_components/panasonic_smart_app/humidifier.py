import logging
from datetime import timedelta

from .const import DOMAIN, DEVICE_TYPE_DEHUMIDIFIER

from homeassistant.components.humidifier import HumidifierEntity
from homeassistant.components.humidifier.const import (
    DEVICE_CLASS_DEHUMIDIFIER,
    SUPPORT_MODES,
)

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=60)

AVAILABLE_MODE = {
    0: "連續除溼",
    1: "自動除濕",
    2: "防霉抑菌",
    3: "送風模式",
    4: "衣物乾燥",
    5: "保持乾燥",
    6: "自訂濕度",
}

AVAILABLE_HUMD = {0: 40, 1: 45, 2: 50, 3: 55, 4: 60, 5: 65, 6: 70}


def getKeyFromDict(targetDict, mode_name):
    for key, value in targetDict.items():
        if mode_name == value:
            return key

    return None


def tryApiStatus(func):
    def wrapper_call(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            args[0]._api.login()
            func(*args, **kwargs)

    return wrapper_call


def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.info("The panasonic_smart_app is setting up humidifier Platform.")
    api = hass.data[DOMAIN]["api"]

    try:
        api.login()
    except Exception as ex:
        _LOGGER.error("Please Check Your Username and Password.")
    else:
        devices = []
        for device in api.getDevices().get("GWList"):
            if device["Devices"][0]["DeviceType"] == DEVICE_TYPE_DEHUMIDIFIER:
                try:
                    entity = PanasonicDehumidifier(device, api)
                except:
                    _LOGGER.error(f"Error occured while setting up {self._name}")
                else:
                    devices.append(entity)

        add_entities(devices, True)
        _LOGGER.info("Dehumidifier setup is done.")


class PanasonicDehumidifier(HumidifierEntity):
    def __init__(self, device, api):
        self._api = api
        self._commandList = api._devices["CommandList"][0]["JSON"][0]["list"]
        self._device = device
        self._name = device["Devices"][0]["NickName"]
        self._auth = device["auth"]
        self._mode = ""
        self._current_humd = 0
        self._is_on_status = False

    @tryApiStatus
    def update(self):
        _LOGGER.debug(f"------- UPDATING {self._name} -------")
        try:
            self._status = self._api.getDeviceInfo(
                self._device["auth"], options=["0x50", "0x00", "0x01", "0x07", "0x0a"]
            )
        except:
            _LOGGER.error(f"Error occured while updating status for {self._name}")
        else:
            _LOGGER.debug(f"Status: {self._status}")
            # _is_on
            self._is_on_status = bool(int(self._status.get("0x00")))
            _LOGGER.debug(f"_is_on: {self._is_on_status}")

            # _mode
            _LOGGER.debug(int(self._status.get("0x01")))
            self._mode = AVAILABLE_MODE[int(self._status.get("0x01"))]
            _LOGGER.debug(f"_mode: {self._mode}")

            # _current_humd
            self._current_humd = self._status.get("0x07")
            _LOGGER.debug(f"_current_humd: {self._current_humd}")

            _LOGGER.debug(f"[{self._name}] is UPDATED.")

    @property
    def name(self):
        """Return the display name of this dehumidifier."""
        return self._name

    @property
    def target_humidity(self):
        return self._current_humd

    @property
    def max_humidity(self):
        return 70

    @property
    def min_humidity(self):
        return 40

    @property
    def mode(self):
        """ Return current mode. """
        return self._mode

    @property
    def available_modes(self):
        return list(AVAILABLE_MODE.values())

    @property
    def supported_features(self):
        return SUPPORT_MODES

    @property
    def is_on(self):
        return self._is_on_status

    @property
    def device_class(self):
        return DEVICE_CLASS_DEHUMIDIFIER

    @tryApiStatus
    def set_mode(self, mode):
        """Set new target mode."""
        if mode is None:
            return
        _LOGGER.debug("Set %s mode %s", self.name, mode)
        self._api.setCommand(self._auth, 129, getKeyFromDict(AVAILABLE_MODE, mode))

    @tryApiStatus
    def set_humidity(self, humidity):
        """Set new target humidity."""
        if humidity is None:
            return

        """ Find closest humidity value """
        targetValue = min(
            list(AVAILABLE_HUMD.values()), key=lambda x: abs(x - humidity)
        )
        targetKey = getKeyFromDict(AVAILABLE_HUMD, targetValue)

        _LOGGER.debug("Set %s humidity to %s", self.name, targetValue)
        self._api.setCommand(self._auth, 132, int(targetKey))

    @tryApiStatus
    def turn_on(self, **kwargs):
        """Turn on dehumidifier."""
        _LOGGER.debug("Turn %s on", self.name)
        self._api.setCommand(self._auth, 128, 1)

    @tryApiStatus
    def turn_off(self, **kwargs):
        """Turn off dehumidifier."""
        _LOGGER.debug("Turn %s off", self.name)
        self._api.setCommand(self._auth, 128, 0)
