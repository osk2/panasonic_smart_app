"""Helpers for decoding Panasonic refrigerator status values."""


def parse_status_byte(value: object) -> int | None:
    """Return a protocol byte, or None for missing/unsupported values."""
    if isinstance(value, bool):
        return None

    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None

    if isinstance(value, float) and not value.is_integer():
        return None
    if isinstance(value, str) and str(parsed) != value.strip():
        return None
    if not 0 <= parsed <= 255:
        return None

    return parsed


def decode_temperature(value: object) -> int | None:
    """Decode an unsigned protocol byte into a signed Celsius value."""
    parsed = parse_status_byte(value)
    if parsed is None:
        return None

    return parsed if parsed < 128 else parsed - 256


def decode_binary_status(value: object) -> bool | None:
    """Decode a refrigerator 0/1 status value."""
    parsed = parse_status_byte(value)
    if parsed not in (0, 1):
        return None

    return parsed == 1
