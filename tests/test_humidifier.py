"""Regression coverage for dehumidifier modes using Home Assistant entities.

Run with Home Assistant installed: python -m unittest discover -s tests -v
"""

import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, Mock

from custom_components.panasonic_smart_app.humidifier import PanasonicDehumidifier


class DehumidifierModeTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        command_path = (
            Path(__file__).resolve().parents[1]
            / "custom_components/panasonic_smart_app/commands/command_list.json"
        )
        commands = json.loads(command_path.read_text())["CommandList"]
        self.device = {
            "ModelType": "NNW",
            "NickName": "Dehumidifier",
            "Auth": "test-device",
            "status": {"0x00": "1", "0x01": "9", "0x04": "2"},
        }
        self.client = Mock()
        self.client.get_commands.return_value = commands
        self.client.set_command = AsyncMock()
        self.coordinator = SimpleNamespace(
            data=[self.device], async_request_refresh=AsyncMock()
        )
        self.entity = PanasonicDehumidifier(
            self.coordinator, 0, self.client, self.device
        )

    async def test_smart_eco_can_be_reported_and_selected(self):
        self.assertEqual(self.entity.mode, "智慧節能")
        self.assertIn("智慧節能", self.entity.available_modes)
        self.assertTrue(self.entity.available)
        await self.entity.async_set_mode("智慧節能")
        self.client.set_command.assert_awaited_once_with("test-device", 129, 9)
        self.coordinator.async_request_refresh.assert_awaited_once()

    async def test_unknown_mode_preserves_power_controls(self):
        self.device["status"]["0x01"] = "99"
        self.assertIsNone(self.entity.mode)
        self.assertTrue(self.entity.available)
        self.assertTrue(self.entity.is_on)
        await self.entity.async_turn_off()
        self.client.set_command.assert_awaited_with("test-device", 128, 0)
        self.device["status"]["0x00"] = "0"
        self.assertFalse(self.entity.is_on)
        await self.entity.async_turn_on()
        self.client.set_command.assert_awaited_with("test-device", 128, 1)
        self.assertEqual(self.coordinator.async_request_refresh.await_count, 2)

    def test_existing_modes_and_empty_status_keep_their_mapping(self):
        for value, label in (
            ("0", "連續除濕"),
            ("1", "自動除濕"),
            ("4", "衣物乾燥"),
            ("5", "保持乾燥"),
            ("6", "濕度設定"),
            (9, "智慧節能"),
            (None, "連續除濕"),
            ("", "連續除濕"),
        ):
            with self.subTest(value=value):
                self.device["status"]["0x01"] = value
                self.assertEqual(self.entity.mode, label)
        del self.device["status"]["0x01"]
        self.assertEqual(self.entity.mode, "連續除濕")

    def test_unconfirmed_nnw_l_mode_is_not_advertised(self):
        self.device["ModelType"] = "NNW-L"
        self.assertNotIn("智慧節能", self.entity.available_modes)
        self.assertIsNone(self.entity.mode)
        self.assertTrue(self.entity.available)
