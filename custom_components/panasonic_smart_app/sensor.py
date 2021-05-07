from .entity import PanasonicHumiditySensor, PanasonicOutdoorTemperatureSensor
from .const import (
    DOMAIN,
    DEVICE_TYPE_DEHUMIDIFIER,
    DEVICE_TYPE_AC,
    DATA_CLIENT,
    DATA_COORDINATOR,
)


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
