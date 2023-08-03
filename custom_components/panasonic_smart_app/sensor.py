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
    TIME_MINUTES,
)

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    DEVICE_TYPE_DEHUMIDIFIER,
    DEVICE_TYPE_AC,
    DEVICE_TYPE_WASHING_MACHINE,
    DATA_CLIENT,
    DATA_COORDINATOR,
    LABEL_PM25,
    LABEL_HUMIDITY,
    LABEL_OUTDOOR_TEMPERATURE,
    LABEL_ENERGY,
    LABEL_WASHING_MACHINE_COUNTDOWN,
    LABEL_WASHING_MACHINE_STATUS,
    LABEL_WASHING_MACHINE_CYCLE,
    LABEL_WASHING_MACHINE_MODE,
    ICON_PM25,
    ICON_THERMOMETER,
    ICON_HUMIDITY,
    ICON_ENERGY,
    ICON_CLOCK,
    ICON_INFO,
    ICON_WASHING_MACHINE,
    ICON_LIST,
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

        if device_type == DEVICE_TYPE_WASHING_MACHINE:
            sensors.append(
                PanasonicWashingCountdownSensor(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )
            sensors.append(
              PanasonicWashingStatusSensor(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )
            sensors.append(
                PanasonicWashingModeSensor(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )
            sensors.append(
                PanasonicWashingCycleSensor(
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
        _is_on = bool(int(status.get("0x00", 0)))
        if not _is_on:
            return STATE_UNAVAILABLE
        _pm25 = float(status.get(self.command_type, -1))
        _LOGGER.debug(f"[{self.label}] state: {_pm25}")
        return _pm25

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
        return energy if energy is not None and energy >= 0 else STATE_UNAVAILABLE

    @property
    def state_class(self) -> str:
        return STATE_TOTAL_INCREASING

    @property
    def unit_of_measurement(self) -> str:
        return ENERGY_KILO_WATT_HOUR


class PanasonicWashingCountdownSensor(PanasonicBaseEntity, SensorEntity):
    """ Panasonic washing machine washing cycle countdown sensor """

    @property
    def label(self):
        return f"{self.nickname} {LABEL_WASHING_MACHINE_COUNTDOWN}"

    @property
    def icon(self) -> str:
        return ICON_CLOCK

    @property
    def state(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        _current_countdown = status.get("0x13", None)
        if _current_countdown is None or float(_current_countdown) < 0:
            _current_countdown = status.get("0x41", None)
        _LOGGER.debug(f"[{self.label}] state: {_current_countdown}")
        return _current_countdown if _current_countdown else STATE_UNAVAILABLE

    @property
    def state_class(self) -> str:
        return STATE_MEASUREMENT

    @property
    def unit_of_measurement(self) -> str:
        return TIME_MINUTES


class PanasonicWashingStatusSensor(PanasonicBaseEntity, SensorEntity):
    """ Panasonic washing machine status sensor """

    @property
    def label(self):
        return f"{self.nickname} {LABEL_WASHING_MACHINE_STATUS}"

    @property
    def icon(self) -> str:
        return ICON_INFO

    @property
    def state(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        washing_status = status.get("0x50")

        if not washing_status:
            return STATE_UNAVAILABLE

        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x50", self.commands)
        )[0]["Parameters"]
        _current_status = list(
            filter(lambda m: m[1] == int(washing_status), raw_mode_list)
        )[0][0]
        _LOGGER.debug(f"[{self.label}] state: {_current_status}")
        return _current_status

    @property
    def state_class(self) -> str:
        return STATE_MEASUREMENT


class PanasonicWashingModeSensor(PanasonicBaseEntity, SensorEntity):
    """ Panasonic washing machine mode sensor """

    @property
    def label(self):
        return f"{self.nickname} {LABEL_WASHING_MACHINE_MODE}"

    @property
    def icon(self) -> str:
        return ICON_WASHING_MACHINE

    @property
    def state(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        mode = status.get("0x54")

        if not mode:
            return STATE_UNAVAILABLE

        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x54", self.commands)
        )[0]["Parameters"]
        _current_mode = list(
            filter(lambda m: m[1] == int(mode), raw_mode_list)
        )[0][0]
        _LOGGER.debug(f"[{self.label}] state: {_current_mode}")
        return _current_mode

    @property
    def state_class(self) -> str:
        return STATE_MEASUREMENT


class PanasonicWashingCycleSensor(PanasonicBaseEntity, SensorEntity):
    """ Panasonic washing machine washing cycle sensor """

    @property
    def label(self):
        return f"{self.nickname} {LABEL_WASHING_MACHINE_CYCLE}"

    @property
    def icon(self) -> str:
        return ICON_LIST

    @property
    def state(self) -> int:
        status = self.coordinator.data[self.index]["status"]
        cycle = status.get("0x55")

        if not cycle:
            return STATE_UNAVAILABLE

        raw_mode_list = list(
            filter(lambda c: c["CommandType"] == "0x55", self.commands)
        )[0]["Parameters"]
        _current_cycle = list(
            filter(lambda m: m[1] == int(cycle), raw_mode_list)
        )[0][0]
        _LOGGER.debug(f"[{self.label}] state: {_current_cycle}")
        return _current_cycle

    @property
    def state_class(self) -> str:
        return STATE_MEASUREMENT
