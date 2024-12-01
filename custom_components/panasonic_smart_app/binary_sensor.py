import logging
from abc import ABC, abstractmethod

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)

from .const import (
    DATA_CLIENT,
    DATA_COORDINATOR,
    DEVICE_TYPE_DEHUMIDIFIER,
    DEVICE_TYPE_REFRIGERATOR,
    DOMAIN,
    ICON_DEFROSTING,
    ICON_TANK,
    ICON_ECONAVI,
    ICON_NANOE,
    LABEL_REFRIGERATOR_DEFROSTING_STATUS,
    LABEL_TANK,
    LABEL_ECONAVI,
    LABEL_NANOE,
)
from .entity import PanasonicBaseEntity

_LOGGER = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    sensors = []

    for index, device in enumerate(devices):
        device_type = int(device.get("DeviceType"))

        if device_type == DEVICE_TYPE_DEHUMIDIFIER:
            sensors.append(
                PanasonoicTankSensor(
                    coordinator,
                    index,
                    client,
                    device,
                )
            )
        elif device_type == DEVICE_TYPE_REFRIGERATOR:
            for sensor_type in (
                PanasonicRefrigeratorDefrostSensor,
                PanasonicRefrigeratorEcoSensor,
                PanasonicRefrigeratorNanoeSensor,
            ):
                if sensor_type.command_type in device["status"]:
                    sensors.append(
                        sensor_type(
                            coordinator,
                            index,
                            client,
                            device,
                        )
                    )

    async_add_entities(sensors, True)

    return True


class PanasonoicTankSensor(PanasonicBaseEntity, BinarySensorEntity):

    @property
    def available(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_on_status = bool(int(status.get("0x00", 0)))
        return _is_on_status

    @property
    def label(self) -> str:
        return f"{self.nickname} {LABEL_TANK}"

    @property
    def icon(self) -> str:
        return ICON_TANK

    @property
    def is_on(self) -> bool:
        status = self.coordinator.data[self.index]["status"]
        _is_tank_full = bool(int(status.get("0x0A", 0)))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_tank_full}")
        return _is_tank_full


class PanasonicRefrigeratorBinarySensorABC(
    PanasonicBaseEntity, BinarySensorEntity, ABC
):
    """Abstract class for binary sensor of Panasonic refrigerator."""

    @property
    @abstractmethod
    def icon(self) -> str:
        """Icon of binary sensor."""

    @property
    @abstractmethod
    def command_name(self) -> str:
        """Command name from the Panasonic API."""

    @property
    @abstractmethod
    def command_type(self) -> str:
        """Command type from the Panasonic API."""

    @property
    def label(self) -> str:
        return f"{self.nickname} {self.command_name}"

    @property
    def is_on(self) -> bool | None:
        status = self.coordinator.data[self.index]["status"]

        try:
            _is_on = int(status[self.command_type]) == 1
        except (KeyError, ValueError):
            _LOGGER.exception(f"Error while getting status for {self.label}")
            return None

        _LOGGER.debug(f"[{self.label}] is_on: {_is_on}")

        return _is_on


class PanasonicRefrigeratorDefrostSensor(PanasonicRefrigeratorBinarySensorABC):
    """Defrosting status of Panasonic refrigerator."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING
    command_name = LABEL_REFRIGERATOR_DEFROSTING_STATUS
    command_type = "0x50"
    icon = ICON_DEFROSTING


class PanasonicRefrigeratorEcoSensor(PanasonicRefrigeratorBinarySensorABC):
    """ECO status of Panasonic refrigerator."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING
    command_name = LABEL_ECONAVI
    command_type = "0x0C"
    icon = ICON_ECONAVI


class PanasonicRefrigeratorNanoeSensor(PanasonicRefrigeratorBinarySensorABC):
    """nanoe status of Panasonic refrigerator."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING
    command_name = LABEL_NANOE
    command_type = "0x61"
    icon = ICON_NANOE
