from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    STATE_UNAVAILABLE,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_PM25,
    TEMP_CELSIUS,
    ENERGY_KILO_WATT_HOUR,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    PERCENTAGE,
)

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    DEVICE_TYPE_DEHUMIDIFIER,
    DEVICE_TYPE_AC,
    DATA_CLIENT,
    DATA_COORDINATOR,
    LABEL_PM25,
    LABEL_HUMIDITY,
    LABEL_OUTDOOR_TEMPERATURE,
    LABEL_ENERGY,
    ICON_PM25,
    ICON_THERMOMETER,
    ICON_HUMIDITY,
    ICON_ENERGY,
    STATE_MEASUREMENT,
    STATE_TOTAL_INCREASING,
)

_LOGGER = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    sensors = []

    for index, device in enumerate(devices):
        device_type = int(device.get("DeviceType"))

        sensors.append(
            PanasonicEnergySensor(
                coordinator,
                index,
                client,
                device,
            )
        )

        if device_type == DEVICE_TYPE_DEHUMIDIFIER:
            sensors.append(
                PanasonicHumiditySensor(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )
            sensors.append(
                PanasonicDehumidifierPM25Sensor(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )

        if device_type == DEVICE_TYPE_AC:
            sensors.append(
                PanasonicOutdoorTemperatureSensor(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )
            sensors.append(
                PanasonicACPM25Sensor(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )

    async_add_entities(sensors, True)

    return True


class PanasonicHumiditySensor(PanasonicBaseEntity, SensorEntity):
    """ Panasonic dehumidifier current humidity sensor """

    @property
    def label(self):
        return f"{self.nickname} {LABEL_HUMIDITY}"

    @property
    def icon(self) -> str:
        return ICON_HUMIDITY

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_HUMIDITY

    @property
    def state(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _current_humd = status.get("0x07", None)
        _LOGGER.debug(f"[{self.label}] state: {_current_humd}")
        return _current_humd if _current_humd else STATE_UNAVAILABLE

    @property
    def state_class(self) -> str:
        return STATE_MEASUREMENT

    @property
    def unit_of_measurement(self) -> str:
        return PERCENTAGE


class PanasonicPM25Sensor(PanasonicBaseEntity, SensorEntity, ABC):

    @property
    @abstractmethod
    def command_type(self) -> str:
        """Command type for PM2.5 sensor."""
        ...

    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_PM25}"

    @property
    def icon(self) -> str:
        return ICON_PM25

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_PM25

    @property
    def state(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _pm25 = float(status.get(self.command_type, -1))
        _LOGGER.debug(f"[{self.label}] state: {_pm25}")
        return _pm25 if _pm25 >= 0 else STATE_UNAVAILABLE

    @property
    def state_class(self) -> str:
        return STATE_MEASUREMENT

    @property
    def unit_of_measurement(self) -> str:
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

class PanasonicDehumidifierPM25Sensor(PanasonicPM25Sensor):
    """ Panasonic Dehumidifier PM2.5 sensor """

    @property
    def command_type(self) -> str:
        return "0x53"

class PanasonicACPM25Sensor(PanasonicPM25Sensor):
    """ Panasonic AC PM2.5 sensor """

    @property
    def command_type(self) -> str:
        return "0x37"

class PanasonicOutdoorTemperatureSensor(PanasonicBaseEntity, SensorEntity):
    """ Panasonic AC outdoor temperature sensor """

    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_OUTDOOR_TEMPERATURE}"

    @property
    def icon(self) -> str:
        return ICON_THERMOMETER

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_TEMPERATURE

    @property
    def state(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _outdoor_temperature = float(status.get("0x21", -1))
        _LOGGER.debug(f"[{self.label}] state: {_outdoor_temperature}")
        return _outdoor_temperature if _outdoor_temperature >= 0 else STATE_UNAVAILABLE

    @property
    def state_class(self) -> str:
        return STATE_MEASUREMENT

    @property
    def unit_of_measurement(self) -> str:
        return TEMP_CELSIUS


class PanasonicEnergySensor(PanasonicBaseEntity, SensorEntity):
    """ Panasonic energy sensor """

    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_ENERGY}"

    @property
    def icon(self) -> str:
        return ICON_ENERGY

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_ENERGY

    @property
    def last_reset(self):
        return datetime.today().replace(day=1)

    @property
    def state(self) -> int:
        energy = self.coordinator.data[self.index]["energy"]
        _LOGGER.debug(f"[{self.label}] state: {energy}")
        return energy if energy >= 0 else STATE_UNAVAILABLE

    @property
    def state_class(self) -> str:
        return STATE_TOTAL_INCREASING

    @property
    def unit_of_measurement(self) -> str:
        return ENERGY_KILO_WATT_HOUR
