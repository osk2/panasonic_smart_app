from .entity import PanasonicOnTimer, PanasonicOffTimer
from .const import DOMAIN, DEVICE_TYPE_DEHUMIDIFIER, DATA_CLIENT, DATA_COORDINATOR


async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    commands = client.get_commands()
    numbers = []

    for device in devices:

        current_device_commands = [
            command
            for command in commands
            if command["ModelType"] == device["Devices"][0]["ModelType"]
        ]

        if int(device["Devices"][0]["DeviceType"]) == DEVICE_TYPE_DEHUMIDIFIER:
            numbers.append(
                PanasonicOffTimer(
                    client,
                    device,
                )
            )

            if len(current_device_commands) > 0:
                is_on_timer_supported = (
                    len(
                        [
                            command
                            for command in current_device_commands[0]["JSON"][0]["list"]
                            if command["CommandType"] == "0x55"
                        ]
                    )
                    > 0
                )

                if is_on_timer_supported:
                    numbers.append(
                        PanasonicOnTimer(
                            client,
                            device,
                        )
                    )

    async_add_entities(numbers, True)

    return True
