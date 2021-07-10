from datetime import timedelta
from abc import ABC, abstractmethod

from .const import (
    DOMAIN,
    MANUFACTURER,
    UPDATE_INTERVAL,
)

SCAN_INTERVAL = timedelta(seconds=UPDATE_INTERVAL)


class PanasonicBaseEntity(ABC):
    def __init__(
        self,
        client,
        device,
    ):
        self.client = client
        self.device = device
        self.status = device["status"]

    @property
    @abstractmethod
    def label(self) -> str:
        """Label to use for name and unique id."""
        ...

    @property
    def current_device_info(self) -> dict:
        return self.device["Devices"][0]

    @property
    def nickname(self) -> str:
        return self.current_device_info["NickName"]

    @property
    def model(self) -> str:
        return self.current_device_info["Model"]

    @property
    def commands(self) -> list:
        command_list = self.client.get_commands()
        current_model_type = self.current_device_info["ModelType"]
        commands = list(
            filter(lambda c: c["ModelType"] == current_model_type, command_list)
        )

        return commands[0]["JSON"][0]["list"]

    @property
    def name(self) -> str:
        return f"{self.nickname} {self.label}"

    @property
    def auth(self) -> str:
        return self.device["auth"]

    @property
    def unique_id(self) -> str:
        return self.auth + self.label

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.auth)},
            "name": self.nickname,
            "manufacturer": MANUFACTURER,
            "model": self.model,
        }
