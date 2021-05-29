import logging
from datetime import timedelta
from homeassistant.components.humidifier import HumidifierEntity
from homeassistant.components.humidifier.const import (
    DEVICE_CLASS_DEHUMIDIFIER,
    SUPPORT_MODES,
)

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    UPDATE_INTERVAL,
    DEVICE_TYPE_DEHUMIDIFIER,
    DATA_CLIENT,
    DATA_COORDINATOR,
    LABEL_DEHUMIDIFIER,
    DEHUMIDIFIER_MIN_HUMD,
    DEHUMIDIFIER_MAX_HUMD,
    DEHUMIDIFIER_AVAILABLE_HUMIDITY,
)

_LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(seconds=UPDATE_INTERVAL)


def getKeyFromDict(targetDict, mode_name):
    for key, value in targetDict.items():
        if mode_name == value:
            return key

    return None


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    humidifiers = []

    for device in devices:
        if int(device["Devices"][0]["DeviceType"]) == DEVICE_TYPE_DEHUMIDIFIER:
            humidifiers.append(
                PanasonicDehumidifier(
                    client,
                    device,
                )
            )

    async_add_entities(humidifiers, True)

    return True


class PanasonicDehumidifier(PanasonicBaseEntity, HumidifierEntity):
    def __init__(self, client, device):

        super().__init__(client, device)

        self._is_on_status = False
        self._mode = ""
        self._current_humd = 0
        self._target_humd = 0

    async def async_update(self):
        _LOGGER.debug(f"------- UPDATING {self.nickname} {self.label} -------")
        try:
            self._status = await self.client.get_device_info(
                self.auth,
                options=["0x50", "0x00", "0x01", "0x0a", "0x04"],
            )

        except:
            _LOGGER.error(f"[{self.nickname}] Error occured while updating status")
        else:
            _LOGGER.debug(f"[{self.nickname}] status: {self._status}")
            # _is_on
            self._is_on_status = bool(int(self._status.get("0x00")))
            _LOGGER.debug(f"[{self.nickname}] _is_on: {self._is_on_status}")

            # _mode
            raw_mode_list = list(
                filter(lambda c: c["CommandType"] == "0x01", self.commands)
            )[0]["Parameters"]
            self._mode = list(
                filter(lambda m: m[1] == int(self._status.get("0x01")), raw_mode_list)
            )[0][0]
            _LOGGER.debug(f"[{self.nickname}] _mode: {self._mode}")

            # _target_humd
            self._target_humd = DEHUMIDIFIER_AVAILABLE_HUMIDITY[
                int(self._status.get("0x04"))
            ]
            _LOGGER.debug(f"[{self.nickname}] _target_humd: {self._target_humd}")

            _LOGGER.debug(f"[{self.nickname}] update completed.")

    @property
    def label(self):
        return LABEL_DEHUMIDIFIER

    @property
    def target_humidity(self):
        return self._target_humd

    @property
    def max_humidity(self):
        return DEHUMIDIFIER_MAX_HUMD

    @property
    def min_humidity(self):
        return DEHUMIDIFIER_MIN_HUMD

    @property
    def mode(self):
        return self._mode

    @property
    def available_modes(self):
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x01", self.commands)
        )[0]["Parameters"]

        def mode_extractor(mode):
            return mode[0]

        mode_list = list(map(mode_extractor, raw_mode_list))
        return mode_list

    @property
    def supported_features(self):
        return SUPPORT_MODES

    @property
    def is_on(self):
        return self._is_on_status

    @property
    def device_class(self):
        return DEVICE_CLASS_DEHUMIDIFIER

    async def async_set_mode(self, mode):
        """ Set operation mode """
        if mode is None:
            return

        _LOGGER.debug(f" [{self.nickname}] Set mode to {mode}")

        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x01", self.commands)
        )[0]
        mode_info = list(filter(lambda m: m[0] == mode, raw_mode_list["Parameters"]))[0]

        await self.client.set_command(self.auth, 129, int(mode_info[1]))

    async def async_set_humidity(self, humidity):
        """ Set target humidity """
        if humidity is None:
            return

        """ Find closest humidity value """
        targetValue = min(
            list(DEHUMIDIFIER_AVAILABLE_HUMIDITY.values()),
            key=lambda x: abs(x - humidity),
        )
        targetKey = getKeyFromDict(DEHUMIDIFIER_AVAILABLE_HUMIDITY, targetValue)

        _LOGGER.debug(f"[{self.nickname}] Set humidity to {targetValue}")
        await self.client.set_command(self.auth, 132, int(targetKey))

    async def async_turn_on(self):
        """ Turn on dehumidifier """
        _LOGGER.debug(f"[{self.nickname}] Turning on")
        await self.client.set_command(self.auth, 128, 1)

    async def async_turn_off(self):
        """ Turn off dehumidifier """
        _LOGGER.debug(f"[{self.nickname}] Turning off")
        await self.client.set_command(self.auth, 128, 0)