from datetime import timedelta
import logging
from homeassistant.components.binary_sensor import BinarySensorEntity

from .entity import PanasonicBaseEntity
from .const import (
    DOMAIN,
    DEVICE_TYPE_DEHUMIDIFIER,
    DATA_CLIENT,
    DATA_COORDINATOR,
    LABEL_TANK,
    ICON_TANK,
)

_LOGGER = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    sensors = []

    for index, device in enumerate(devices):
        if int(device.get("DeviceType")) == DEVICE_TYPE_DEHUMIDIFIER:
            sensors.append(
                PanasonoicTankSensor(
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
        _is_on_status = bool(int(status.get("0x00") or 0))
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
        _is_tank_full = bool(int(status.get("0x0a") or 0))
        _LOGGER.debug(f"[{self.label}] is_on: {_is_tank_full}")
        return _is_tank_full
