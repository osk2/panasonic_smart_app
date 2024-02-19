import logging
from homeassistant.components.humidifier import (
    HumidifierEntity,
    HumidiferDeviceClass,
    HumidifierEntityFeature,
)
from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    DEVICE_TYPE_DEHUMIDIFIER,
    DEVICE_CLASS_DEHUMIDIFIER,
    DATA_CLIENT,
    DATA_COORDINATOR,
    LABEL_DEHUMIDIFIER,
    DEHUMIDIFIER_MIN_HUMD,
    DEHUMIDIFIER_MAX_HUMD,
    DEHUMIDIFIER_AVAILABLE_HUMIDITY,
)

_LOGGER = logging.getLogger(__package__)


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

    for index, device in enumerate(devices):
        if int(device.get("DeviceType")) == DEVICE_TYPE_DEHUMIDIFIER:
            humidifiers.append(
                PanasonicDehumidifier(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )

    async_add_entities(humidifiers, True)

    return True


class PanasonicDehumidifier(PanasonicBaseEntity, HumidifierEntity):
    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        return status.get("0x00") != None

    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_DEHUMIDIFIER}"

    @property
    def target_humidity(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _target_humidity = DEHUMIDIFIER_AVAILABLE_HUMIDITY[int(status.get("0x04", 0))]
        _LOGGER.debug(f"[{self.label}] target_humidity: {_target_humidity}")
        return _target_humidity

    @property
    def max_humidity(self) -> int:
        return DEHUMIDIFIER_MAX_HUMD

    @property
    def min_humidity(self) -> int:
        return DEHUMIDIFIER_MIN_HUMD

    @property
    def mode(self) -> str:
        status = self.coordinator.data[self.index]["status"]
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x01", self.commands)
        )[0]["Parameters"]
        target_mode = list(
            filter(lambda m: m[1] == int(status.get("0x01") or 0), raw_mode_list)
        )[0]
        _mode = target_mode[0] if len(target_mode) > 0 else ""
        _LOGGER.debug(f"[{self.label}] _mode: {_mode}")
        return _mode

    @property
    def available_modes(self) -> list:
        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x01", self.commands)
        )[0]["Parameters"]

        def mode_extractor(mode):
            return mode[0]

        mode_list = list(map(mode_extractor, raw_mode_list))
        return mode_list

    @property
    def supported_features(self) -> int:
        return HumidifierEntityFeature.MODES

    @property
    def is_on(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00") or 0))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_on_status}")
        return _is_on_status

    @property
    def device_class(self) -> str:
        #return HumidiferDeviceClass.DEHUMIDIFIER
        return DEVICE_CLASS_DEHUMIDIFIER

    async def async_set_mode(self, mode) -> None:
        """ Set operation mode """
        if mode is None:
            return

        _LOGGER.debug(f" [{self.label}] Set mode to {mode}")

        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x01", self.commands)
        )[0]
        mode_info = list(filter(lambda m: m[0] == mode, raw_mode_list["Parameters"]))[0]

        await self.client.set_command(self.auth, 129, int(mode_info[1]))
        await self.coordinator.async_request_refresh()

    async def async_set_humidity(self, humidity) -> None:
        """ Set target humidity """
        if humidity is None:
            return

        """ Find closest humidity value """
        targetValue = min(
            list(DEHUMIDIFIER_AVAILABLE_HUMIDITY.values()),
            key=lambda x: abs(x - humidity),
        )
        targetKey = getKeyFromDict(DEHUMIDIFIER_AVAILABLE_HUMIDITY, targetValue)

        _LOGGER.debug(f"[{self.label}] Set humidity to {targetValue}")
        await self.client.set_command(self.auth, 132, int(targetKey))
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self) -> None:
        """ Turn on dehumidifier """
        _LOGGER.debug(f"[{self.label}] Turning on")
        await self.client.set_command(self.auth, 128, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        """ Turn off dehumidifier """
        _LOGGER.debug(f"[{self.label}] Turning off")
        await self.client.set_command(self.auth, 128, 0)
        await self.coordinator.async_request_refresh()
