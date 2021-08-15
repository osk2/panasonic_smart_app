"""Adds config flow for Panasonic Smart App"""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from .smartApp import SmartApp
from .smartApp.exceptions import PanasonicExceedRateLimit
from .const import (
    DOMAIN,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
)


class SmartAppFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self) -> None:
        self._errors: dict[str, str] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        self._errors = {}

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]
            session = async_get_clientsession(self.hass)
            client = SmartApp(
                session=session,
                account=username,
                password=password,
            )

            try:
                await self._test_credentials(client)
                return self.async_create_entry(title=username, data=user_input)
            except PanasonicExceedRateLimit:
                self._errors["base"] = "rate_limit"
            except:
                self._errors["base"] = "auth"

        return await self._show_config_form(user_input)

    async def _show_config_form(
        self, _user_input: dict[str, Any] | None
    ) -> dict[str, Any]:
        """ Show the configuration form. """
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): int,
                }
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, client) -> True:
        await client.login()
        return True
