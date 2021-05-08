from .entity import PanasonicDehumidifier
from .const import DOMAIN, DEVICE_TYPE_DEHUMIDIFIER, DATA_CLIENT, DATA_COORDINATOR


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
