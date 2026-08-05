from abc import ABC, abstractmethod

from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_registry import RegistryEntryDisabler
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .smartApp import SmartApp


def set_registry_entity_disabled(hass, domain: str, entity, *, disabled: bool) -> None:
    """Disable unsupported entities without overriding a user's preference."""
    registry = er.async_get(hass)
    entity_id = registry.async_get_entity_id(domain, DOMAIN, entity.unique_id)
    if entity_id is None:
        return

    entry = registry.async_get(entity_id)
    if entry is None:
        return

    if disabled and entry.disabled_by is None:
        registry.async_update_entity(
            entity_id,
            disabled_by=RegistryEntryDisabler.INTEGRATION,
        )
    elif not disabled and entry.disabled_by == RegistryEntryDisabler.INTEGRATION:
        registry.async_update_entity(entity_id, disabled_by=None)


class PanasonicBaseEntity(CoordinatorEntity, ABC):
    def __init__(
        self,
        coordinator,
        index,
        client,
        device,
    ):
        super().__init__(coordinator)
        self.client: SmartApp = client
        self.device = device
        self.index = index

    @property
    @abstractmethod
    def label(self) -> str:
        """Label to use for name and unique id."""
        ...

    @property
    def current_device_info(self) -> dict:
        return self.device

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
        return self.label

    @property
    def auth(self) -> str:
        return self.device["Auth"]

    @property
    def unique_id(self) -> str:
        return self.auth + self.label

    @property
    def device_info(self) -> dict:
        return {
            "identifiers": {(DOMAIN, self.auth)},
            "name": self.nickname,
            "manufacturer": MANUFACTURER,
            "model": self.model,
        }
