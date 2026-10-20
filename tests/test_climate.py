"""Horizontal airflow support against Home Assistant's native climate interface."""

from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

from homeassistant.components.climate import ClimateEntityFeature
from homeassistant.exceptions import HomeAssistantError
import pytest

from custom_components.panasonic_smart_app.climate import PanasonicClimate
from custom_components.panasonic_smart_app.smartApp import SmartApp


COMMANDS = json.loads(
    (
        Path(__file__).parents[1]
        / "custom_components/panasonic_smart_app/commands/command_list.json"
    ).read_text()
)["CommandList"]
AC_MODELS = [
    item["ModelType"] for item in COMMANDS if item["JSON"][0]["DeviceType"] == 1
]


def make_climate(model="PX", status=None, api_commands=None):
    """Use the real command-source selection and entity classes, without network IO."""
    client = SmartApp(None, "", "")
    if api_commands is not None:
        client._commands = [{"ModelType": model, "JSON": [{"list": api_commands}]}]
    client.set_command = AsyncMock()
    device = {
        "ModelType": model,
        "Model": model,
        "Auth": "test-auth",
        "NickName": "AC",
        "status": {"0x00": "1", "0x0F": "1", "0x02": "0", **(status or {})},
    }
    coordinator = SimpleNamespace(data=[device], async_request_refresh=AsyncMock())
    return PanasonicClimate(coordinator, 0, client, device)


@pytest.mark.parametrize("model", AC_MODELS)
def test_static_model_capabilities(model):
    entity = make_climate(model)
    supports_horizontal = model not in {"PU", "GX", "J", "SX-DUCT"}
    assert (
        bool(entity.supported_features & ClimateEntityFeature.SWING_HORIZONTAL_MODE)
        == supports_horizontal
    )
    assert entity.swing_horizontal_modes == (
        ["自動", *[f"位置 {position}" for position in range(1, 8)]]
        if supports_horizontal
        else []
    )


@pytest.mark.parametrize(
    "value, expected", [("0", "自動"), ("1", "位置 1"), ("4", "位置 4"), (7, "位置 7")]
)
def test_horizontal_status(value, expected):
    entity = make_climate(status={"0x11": value})
    assert entity.swing_horizontal_mode == expected
    assert entity.swing_mode == "0°"


@pytest.mark.parametrize("value", [None, "", "invalid", "8", "-1"])
def test_unknown_status_does_not_become_auto(value):
    entity = make_climate(status={"0x11": value})
    assert entity.swing_horizontal_mode is None
    assert entity.supported_features & ClimateEntityFeature.SWING_HORIZONTAL_MODE


def test_missing_status_keeps_capability():
    entity = make_climate()
    assert entity.swing_horizontal_mode is None
    assert entity.supported_features & ClimateEntityFeature.SWING_HORIZONTAL_MODE


def test_home_assistant_exposes_horizontal_capabilities_and_state():
    entity = make_climate(status={"0x11": "4", "0x01": "0", "0x03": "26", "0x04": "27"})
    entity.hass = SimpleNamespace(
        config=SimpleNamespace(units=SimpleNamespace(temperature_unit="°C"))
    )
    assert (
        entity.capability_attributes["swing_horizontal_modes"]
        == entity.swing_horizontal_modes
    )
    assert entity.state_attributes["swing_horizontal_mode"] == "位置 4"


@pytest.mark.parametrize("command_type", ["0x11", "0X11"])
def test_api_enum_takes_precedence_over_static_definition(command_type):
    entity = make_climate(
        status={"0x11": "4"},
        api_commands=[
            {
                "CommandType": command_type,
                "ParameterType": "enum",
                "Parameters": [["自動", "0"], ["中央", "4"]],
            }
        ],
    )
    assert entity.swing_horizontal_modes == ["自動", "中央"]
    assert entity.swing_horizontal_mode == "中央"


def test_api_range_controls_option_bounds():
    entity = make_climate(
        api_commands=[
            {
                "CommandType": "0x11",
                "ParameterType": "rangeA",
                "Parameters": [["Auto", "0"], ["Min", "2"], ["Max", "4"]],
            }
        ]
    )
    assert entity.swing_horizontal_modes == ["自動", "位置 2", "位置 3", "位置 4"]


def test_incomplete_api_model_does_not_inherit_static_horizontal_command():
    entity = make_climate(api_commands=[])
    assert entity.swing_horizontal_modes == []
    assert not entity.supported_features & ClimateEntityFeature.SWING_HORIZONTAL_MODE


@pytest.mark.parametrize(
    "parameters",
    [
        [],
        [["Min", 1], ["Max", 7]],
        [["Auto", 0], ["Min", 7], ["Max", 1]],
        [["Auto", 0], ["Min", "invalid"], ["Max", 7]],
    ],
)
def test_invalid_range_is_not_advertised(parameters):
    entity = make_climate(
        api_commands=[
            {
                "CommandType": "0x11",
                "ParameterType": "rangeA",
                "Parameters": parameters,
            }
        ]
    )
    assert entity.swing_horizontal_modes == []
    assert not entity.supported_features & ClimateEntityFeature.SWING_HORIZONTAL_MODE


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mode, value", [("自動", 0), ("位置 1", 1), ("位置 4", 4), ("位置 7", 7)]
)
async def test_native_horizontal_action(mode, value):
    entity = make_climate(status={"0x11": "0"})
    original_status = deepcopy(entity.coordinator.data[0]["status"])
    await entity.async_handle_set_swing_horizontal_mode_service(mode)
    entity.client.set_command.assert_awaited_once_with("test-auth", 145, value)
    entity.coordinator.async_request_refresh.assert_awaited_once()
    assert entity.coordinator.data[0]["status"] == original_status


@pytest.mark.asyncio
async def test_invalid_action_sends_no_command():
    entity = make_climate()
    with pytest.raises(HomeAssistantError):
        await entity.async_handle_set_swing_horizontal_mode_service("位置 8")
    with pytest.raises(HomeAssistantError):
        await entity.async_set_swing_horizontal_mode("位置 8")
    entity.client.set_command.assert_not_awaited()
    entity.coordinator.async_request_refresh.assert_not_awaited()


@pytest.mark.asyncio
async def test_api_enum_action_uses_device_value():
    entity = make_climate(
        api_commands=[
            {
                "CommandType": "0x11",
                "ParameterType": "enum",
                "Parameters": [["自動", 0], ["中央", 4]],
            }
        ]
    )
    await entity.async_handle_set_swing_horizontal_mode_service("中央")
    entity.client.set_command.assert_awaited_once_with("test-auth", 145, 4)
    entity.coordinator.async_request_refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_vertical_action_is_unchanged():
    entity = make_climate()
    assert entity.swing_modes == ["自動", "0°", "20°", "45°", "70°", "90°"]
    await entity.async_handle_set_swing_mode_service("45°")
    entity.client.set_command.assert_awaited_once_with("test-auth", 143, 3)
    entity.coordinator.async_request_refresh.assert_awaited_once()
