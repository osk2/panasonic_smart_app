""" TaiSEIA 101 """
from homeassistant.components.climate.const import (
    HVAC_MODE_COOL, HVAC_MODE_HEAT, HVAC_MODE_HEAT_COOL, HVAC_MODE_DRY, HVAC_MODE_FAN_ONLY, HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE, SUPPORT_FAN_MODE, SUPPORT_SWING_MODE, SUPPORT_PRESET_MODE,
    PRESET_ECO, PRESET_NONE, PRESET_BOOST,
    ATTR_CURRENT_TEMPERATURE, ATTR_FAN_MODE,
    ATTR_HVAC_MODE, ATTR_SWING_MODE, ATTR_PRESET_MODE
)

COMMANDS_NAME = {
    "0x00": "power",
    "0x01": "mode",
    "0x02": "fan_speed",
    "0x03": "target_temperature",
    "0x04": "current_temperature",
    "0x08": "nanoeX",
    "0x0F": "上下風向",
    "0x11": "左右風向",
    "0x1A": "急速",
    "0x0B": "定時開機",
    "0x0C": "定時關機",
    "0x19": "動態感應",
    "0x1B": "econavi",
    "0x1F": "亮度",
    "0x1E": "音量"
}

COMMANDS_OPTIONS = {
    "0x00": {
        "0": "Off",
        "1": "On"
    },
    "0x01": {
        "0": HVAC_MODE_COOL,
        "1": HVAC_MODE_DRY,
        "2": HVAC_MODE_FAN_ONLY,
        "3": HVAC_MODE_HEAT_COOL,
        "4": HVAC_MODE_HEAT
    }
}