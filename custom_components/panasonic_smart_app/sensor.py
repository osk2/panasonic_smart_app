from abc import ABC, abstractmethod
import logging
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfMass,
    STATE_UNAVAILABLE,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    PERCENTAGE,
)
from homeassistant.exceptions import HomeAssistantError

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    DEVICE_TYPE_DEHUMIDIFIER,
    DEVICE_TYPE_AC,
    DEVICE_TYPE_REFRIGERATOR,
    DEVICE_TYPE_WASHING_MACHINE,
    DEVICE_TYPE_PURIFIER,
    DATA_CLIENT,
    DATA_COORDINATOR,
    LABEL_PM25,
    LABEL_CO2_FOOTPRINT,
    LABEL_HUMIDITY,
    LABEL_OUTDOOR_TEMPERATURE,
    LABEL_ENERGY,
    LABEL_REFRIGERATOR_FREEZER_TEMPERATURE_DISPLAY,
    LABEL_REFRIGERATOR_REFRIGERATOR_TEMPERATURE_DISPLAY,
    LABEL_REFRIGERATOR_PARTIAL_FREEZING_TEMPERATURE_DISPLAY,
    LABEL_REFRIGERATOR_OPEN_DOOR,
    LABEL_WASHING_MACHINE_COUNTDOWN,
    LABEL_WASHING_MACHINE_STATUS,
    LABEL_WASHING_MACHINE_CYCLE,
    LABEL_WASHING_MACHINE_MODE,
    ICON_PM25,
    ICON_THERMOMETER,
    ICON_HUMIDITY,
    ICON_ENERGY,
    ICON_REFRIGERATOR,
    ICON_CLOCK,
    ICON_INFO,
    ICON_WASHING_MACHINE,
    ICON_LIST,
    ICON_CO2_FOOTPRINT,
    ICON_REFRIGERATOR_WINTER_MODE,
    ICON_REFRIGERATOR_SHOPPING_MODE,
    ICON_REFRIGERATOR_VACATION_MODE,
    ICON_REFRIGERATOR_RAPID_FREEZING,
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
        device_status = coordinator.data[index].get("status", {}).keys()
        _LOGGER.debug(f"Device index #{index} status: {device_status}")

        if coordinator.data[index].get("energy"):
            sensors.append(
                PanasonicEnergySensor(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )

        if coordinator.data[index].get("co2"):
            sensors.append(
                PanasonicCO2FootprintSensor(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )

        if coordinator.data[index].get("ref_open_door"):
            sensors.append(
                PanasonicRefOpenDoorSensor(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )

        if device_type == DEVICE_TYPE_DEHUMIDIFIER:
            if "0x07" in device_status:
                sensors.append(
                    PanasonicHumiditySensor(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )
            if "0x53" in device_status:
                sensors.append(
                    PanasonicDehumidifierPM25Sensor(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )

        if device_type == DEVICE_TYPE_AC:
            if "0x21" in device_status:
                sensors.append(
                    PanasonicOutdoorTemperatureSensor(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )
            if "0x37" in device_status:
                sensors.append(
                    PanasonicACPM25Sensor(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )

        if device_type == DEVICE_TYPE_REFRIGERATOR:
            for sensor_type in (
                PananocisRefrigeratorFreezerTemperatureSensor,
                PananocisRefrigeratorRefrigeratorTemperatureSensor,
                PananocisRefrigeratorPartialFreezingTemperatureSensor,
                PananocisRefrigeratorRapidFreezingSensor,
                PananocisRefrigeratorWinterModeSensor,
                PananocisRefrigeratorShoppingModeSensor,
                PananocisRefrigeratorVacationModeSensor,
            ):
                if sensor_type.command_type in device_status:
                    sensors.append(
                        sensor_type(
                            coordinator,
                            index,
                            client,
                            device,
                        )
                    )

        if device_type == DEVICE_TYPE_WASHING_MACHINE:
            if "0x13" in device_status:
                sensors.append(
                    PanasonicWashingCountdownSensor(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )
            if "0x50" in device_status:
                sensors.append(
                    PanasonicWashingStatusSensor(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )
            if "0x54" in device_status:
                sensors.append(
                    PanasonicWashingModeSensor(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )
            if "0x55" in device_status:
                sensors.append(
                    PanasonicWashingCycleSensor(
                        coordinator,
                        index,
                        client,
                        device,
                    )
                )

        if device_type == DEVICE_TYPE_PURIFIER:
            if "0x50" in device_status:
                sensors.append(
                    PanasonicPurifierPM25Sensor(
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
        return SensorDeviceClass.HUMIDITY

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
        return SensorDeviceClass.PM25

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


class PanasonicPurifierPM25Sensor(PanasonicPM25Sensor):
    """ Panasonic Purifier PM2.5 sensor """

    @property
    def command_type(self) -> str:
        return "0x50"


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
        return SensorDeviceClass.TEMPERATURE

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
        return UnitOfTemperature.CELSIUS


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
        return SensorDeviceClass.ENERGY

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
        return UnitOfEnergy.KILO_WATT_HOUR


class PanasonicCO2FootprintSensor(PanasonicBaseEntity, SensorEntity):
    """Panasonic CO2 sensor"""
    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_CO2_FOOTPRINT}"

    @property
    def icon(self) -> str:
        return ICON_CO2_FOOTPRINT

    @property
    def device_class(self) -> str:
        return SensorDeviceClass.WEIGHT

    @property
    def native_value(self) -> float:
        co2 = self.coordinator.data[self.index]["co2"]
        _LOGGER.debug(f"[{self.label}] state: {co2}")
        return co2

    @property
    def state_class(self) -> str:
        return SensorStateClass.TOTAL_INCREASING

    @property
    def native_unit_of_measurement(self) -> str:
        return UnitOfMass.KILOGRAMS


class PanasonicRefOpenDoorSensor(PanasonicBaseEntity, SensorEntity):
    """Panasonic Refrigerator open door sensor"""

    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_REFRIGERATOR_OPEN_DOOR}"

    @property
    def icon(self) -> str:
        return ICON_REFRIGERATOR

    @property
    def last_reset(self) -> None:
        return None

    @property
    def native_value(self) -> int:
        ref_open_door = self.coordinator.data[self.index]["ref_open_door"]
        _LOGGER.debug(f"[{self.label}] state: {ref_open_door}")
        return ref_open_door

    @property
    def state_class(self) -> str:
        return SensorStateClass.TOTAL_INCREASING

    @property
    def native_unit_of_measurement(self) -> None:
        return None


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
        return UnitOfTime.MINUTES


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

        if not raw_mode_list:
            return STATE_UNAVAILABLE

        _raw_current_status = list(filter(lambda m: m[1] == int(washing_status), raw_mode_list))

        if len(_raw_current_status) > 0:
            _current_status = _raw_current_status[0][0]
        else:
            _current_status = STATE_UNAVAILABLE

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


class PananocisRefrigeratorTemperatureSensorABC(PanasonicBaseEntity, SensorEntity, ABC):
    """Abstract class for temperature sensor of Panasonic refrigerator."""

    @property
    @abstractmethod
    def command_type(self) -> str:
        """Command type from the Panasonic API."""

    @property
    @abstractmethod
    def label_name(self) -> str:
        """
        Label name of the sensor. Used to generate the full name.
        See label property.
        """

    @property
    def label(self) -> str:
        """The name of the sensor."""
        return f"{self.nickname} {self.label_name}"

    @property
    def device_class(self) -> str:
        return SensorDeviceClass.TEMPERATURE

    @property
    def native_value(self) -> int:
        status = self.coordinator.data[self.index]["status"]

        try:
            unsigned_temperature = int(status[self.command_type])
        except (KeyError, ValueError):
            _LOGGER.exception(
                f"[{self.label}] Unable to get temperature from status: {status}"
            )
            return STATE_UNAVAILABLE

        signed_temperature = (
            unsigned_temperature
            if unsigned_temperature < 128
            else unsigned_temperature - 256
        )

        _LOGGER.debug(f"[{self.label}] state: {signed_temperature}")

        return signed_temperature

    @property
    def state_class(self) -> str:
        return SensorStateClass.MEASUREMENT

    @property
    def native_unit_of_measurement(self) -> str:
        return UnitOfTemperature.CELSIUS


class PananocisRefrigeratorFreezerTemperatureSensor(PananocisRefrigeratorTemperatureSensorABC):
    """ Panasonic refrigerator freezer temperature sensor """

    command_type = "0x03"
    label_name = LABEL_REFRIGERATOR_FREEZER_TEMPERATURE_DISPLAY


class PananocisRefrigeratorRefrigeratorTemperatureSensor(PananocisRefrigeratorTemperatureSensorABC):
    """ Panasonic refrigerator refrigerator temperature sensor """

    command_type = "0x05"
    label_name = LABEL_REFRIGERATOR_REFRIGERATOR_TEMPERATURE_DISPLAY


class PananocisRefrigeratorPartialFreezingTemperatureSensor(PananocisRefrigeratorTemperatureSensorABC):
    """ Panasonic refrigerator partial freezing temperature sensor """

    command_type = "0x58"
    label_name = LABEL_REFRIGERATOR_PARTIAL_FREEZING_TEMPERATURE_DISPLAY


class PananocisRefrigeratorEnumSensorABC(PanasonicBaseEntity, SensorEntity, ABC):
    """Abstract class for sensor of Panasonic refrigerator with enum values."""

    @property
    @abstractmethod
    def icon(self) -> str:
        """Icon of this entity."""

    @property
    @abstractmethod
    def command_type(self) -> str:
        """Command type from the Panasonic API."""

    def _this_command(self) -> dict:
        """The corresponding command of this entity in Panasonic UserGetRegisteredGwList2 API."""
        for command in self.commands:
            if command["CommandType"] == self.command_type:
                return command

        raise HomeAssistantError(
            f"Command not found in commands: {self.command_type} for {self.label}"
        )

    @property
    def label(self) -> str:
        """The name of the sensor. Generated with the CommandName from Panasonic API."""
        command_name = self._this_command()["CommandName"]
        return f"{self.nickname} {command_name}"

    @property
    def device_class(self) -> str:
        return SensorDeviceClass.ENUM

    @property
    def native_value(self) -> int:
        status = self.coordinator.data[self.index]["status"]

        try:
            value = int(status[self.command_type])
        except (KeyError, ValueError):
            _LOGGER.exception(f"Error while getting status for {self.label}")
            return None

        for parameter in self._this_command()["Parameters"]:
            if parameter[1] == value:
                _LOGGER.debug(f"[{self.label}] current_option: {parameter[0]}")
                return parameter[0]

        _LOGGER.error(f"Unknown value {value} for {self.label}")
        return None

    @property
    def options(self) -> list:
        return [parameter[0] for parameter in self._this_command()["Parameters"]]


class PananocisRefrigeratorRapidFreezingSensor(PananocisRefrigeratorEnumSensorABC):
    """ Panasonic refrigerator rapid freezing sensor """

    # TODO: Rapid freezing can be enabled by the user in the Panasonic app, with the
    #       specified schedule, which can be pre-built or user-defined. This might be
    #       complex to be implemented as a select entity. So, it is implemented as a
    #       sensor entity here, which is read-only and shows the current status.

    icon = ICON_REFRIGERATOR_RAPID_FREEZING
    command_type = "0x56"


class PananocisRefrigeratorWinterModeSensor(PananocisRefrigeratorEnumSensorABC):
    """ Panasonic refrigerator winter mode sensor """

    # TODO: Refrigerator modes can be changed by the user in the Panasonic app. But the
    #       conditions and the behavior of them might be a bit complex. So, they are not
    #       implemented to be select entities for now. Instead, they are implemented as
    #       sensor entities, which are read-only and show the current mode.

    icon = ICON_REFRIGERATOR_WINTER_MODE
    command_type = "0x5A"


class PananocisRefrigeratorShoppingModeSensor(PananocisRefrigeratorEnumSensorABC):
    """ Panasonic refrigerator shopping mode sensor """

    # TODO: See the note in PananocisRefrigeratorWinterModeSensor.

    icon = ICON_REFRIGERATOR_SHOPPING_MODE
    command_type = "0x5B"


class PananocisRefrigeratorVacationModeSensor(PananocisRefrigeratorEnumSensorABC):
    """ Panasonic refrigerator vacation mode sensor """

    # TODO: See the note in PananocisRefrigeratorWinterModeSensor.

    icon = ICON_REFRIGERATOR_VACATION_MODE
    command_type = "0x5C"
