from datetime import timedelta
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    STATE_UNAVAILABLE,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_TEMPERATURE,
    TEMP_CELSIUS,
    PERCENTAGE,
)

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    UPDATE_INTERVAL,
    DEVICE_TYPE_DEHUMIDIFIER,
    DEVICE_TYPE_AC,
    DATA_CLIENT,
    DATA_COORDINATOR,
    LABEL_HUMIDITY,
    LABEL_OUTDOOR_TEMPERATURE,
    ICON_THERMOMETER,
    ICON_HUMIDITY,
)

_LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(seconds=UPDATE_INTERVAL)


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    sensors = []

    for device in devices:
        device_type = int(device["Devices"][0]["DeviceType"])

        if device_type == DEVICE_TYPE_DEHUMIDIFIER:
            sensors.append(
                PanasonicHumiditySensor(
                    client,
                    device,
                )
            )

        if device_type == DEVICE_TYPE_AC:
            sensors.append(
                PanasonicOutdoorTemperatureSensor(
                    client,
                    device,
                )
            )

    async_add_entities(sensors, True)

    return True


class PanasonicHumiditySensor(PanasonicBaseEntity, SensorEntity):
    """ Panasonic dehumidifier current humidity sensor """

    async def async_update(self):
        _LOGGER.debug(f"------- UPDATING {self.nickname} {self.label} -------")

        try:
            self._status = await self.client.get_device_info(
                self.auth,
                options=["0x07"],
            )

            self._current_humd = self._status.get("0x07")
            _LOGGER.debug(f"[{self.nickname}] _current_humd: {self._current_humd}")
        except:
            _LOGGER.error(f"[{self.nickname}] Error occured while updating status")
        else:
            _LOGGER.debug(f"[{self.nickname}] status: {self._status}")

    @property
    def label(self) -> str:
        return LABEL_HUMIDITY

    @property
    def icon(self) -> str:
        return ICON_HUMIDITY

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_HUMIDITY

    @property
    def state(self) -> int:
        return self._current_humd if self._current_humd else STATE_UNAVAILABLE

    @property
    def unit_of_measurement(self) -> str:
        return PERCENTAGE


class PanasonicOutdoorTemperatureSensor(PanasonicBaseEntity, SensorEntity):
    """ Panasonic AC outdoor temperature sensor """

    async def async_update(self):
        _LOGGER.debug(f"------- UPDATING {self.nickname} {self.label} -------")

        try:
            self._status = await self.client.get_device_info(
                self.auth,
                options=["0x21"],
            )

            self._outside_temperature = float(self._status.get("0x21"))
            _LOGGER.debug(
                f"[{self.nickname}] _outside_temperature: {self._outside_temperature}"
            )
        except:
            _LOGGER.error(f"[{self.nickname}] Error occured while updating status")
        else:
            _LOGGER.debug(f"[{self.nickname}] status: {self._status}")

    @property
    def label(self) -> str:
        return LABEL_OUTDOOR_TEMPERATURE

    @property
    def icon(self) -> str:
        return ICON_THERMOMETER

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_TEMPERATURE

    @property
    def state(self) -> int:
        return (
            self._outside_temperature
            if self._outside_temperature
            else STATE_UNAVAILABLE
        )

    @property
    def unit_of_measurement(self) -> str:
        return TEMP_CELSIUS
