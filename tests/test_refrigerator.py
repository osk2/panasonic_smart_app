"""Tests for Panasonic refrigerator status decoding."""

import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = (
    Path(__file__).parents[1]
    / "custom_components"
    / "panasonic_smart_app"
    / "refrigerator.py"
)
SPEC = importlib.util.spec_from_file_location("panasonic_refrigerator", MODULE_PATH)
refrigerator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(refrigerator)


class RefrigeratorStatusTest(unittest.TestCase):
    def test_parse_status_byte_accepts_protocol_values(self) -> None:
        self.assertEqual(refrigerator.parse_status_byte("0"), 0)
        self.assertEqual(refrigerator.parse_status_byte("255"), 255)
        self.assertEqual(refrigerator.parse_status_byte(12), 12)

    def test_parse_status_byte_rejects_unsupported_values(self) -> None:
        for value in (None, True, "", "unavailable", "-1683.3", "1.0", -1, 256):
            with self.subTest(value=value):
                self.assertIsNone(refrigerator.parse_status_byte(value))

    def test_decode_temperature_preserves_signed_byte_protocol(self) -> None:
        self.assertEqual(refrigerator.decode_temperature("0"), 0)
        self.assertEqual(refrigerator.decode_temperature("127"), 127)
        self.assertEqual(refrigerator.decode_temperature("128"), -128)
        self.assertEqual(refrigerator.decode_temperature("238"), -18)
        self.assertEqual(refrigerator.decode_temperature("255"), -1)
        self.assertIsNone(refrigerator.decode_temperature("-1683.3"))

    def test_decode_binary_status_accepts_only_zero_or_one(self) -> None:
        self.assertFalse(refrigerator.decode_binary_status("0"))
        self.assertTrue(refrigerator.decode_binary_status("1"))
        self.assertIsNone(refrigerator.decode_binary_status("2"))
        self.assertIsNone(refrigerator.decode_binary_status("-1683.3"))


if __name__ == "__main__":
    unittest.main()
