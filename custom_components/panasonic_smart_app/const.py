"""Contants for Panasonic Smart App integration"""

from homeassistant.components.climate.const import (
    HVAC_MODE_OFF,
    HVAC_MODE_COOL,
    HVAC_MODE_DRY,
    HVAC_MODE_HEAT,
    HVAC_MODE_AUTO,
    HVAC_MODE_FAN_ONLY,
)

DOMAIN = "panasonic_smart_app"
PLATFORMS = ["humidifier", "sensor", "number", "binary_sensor", "climate"]
MANUFACTURER = "Panasonic"
DEFAULT_NAME = "Panasonic Smart Application"

DEVICE_TYPE_AC = 1
DEVICE_TYPE_DEHUMIDIFIER = 4

DATA_CLIENT = "client"
DATA_COORDINATOR = "coordinator"

UPDATE_INTERVAL = 60

DEHUMIDIFIER_MAX_HUMD = 70
DEHUMIDIFIER_MIN_HUMD = 40
DEHUMIDIFIER_AVAILABLE_HUMIDITY = {0: 40, 1: 45, 2: 50, 3: 55, 4: 60, 5: 65, 6: 70}
CLIMATE_AVAILABLE_MODE = [
    {"key": HVAC_MODE_OFF, "mappingCode": -1},
    {"key": HVAC_MODE_COOL, "mappingCode": 0},
    {"key": HVAC_MODE_DRY, "mappingCode": 1},
    {"key": HVAC_MODE_FAN_ONLY, "mappingCode": 2},
    {"key": HVAC_MODE_AUTO, "mappingCode": 3},
    {"key": HVAC_MODE_HEAT, "mappingCode": 4},
]
CLIMATE_AVAILABLE_PRESET = {0: "冷氣", 1: "除濕", 2: "清淨", 3: "自動", 4: "暖氣"}
CLIMATE_AVAILABLE_SWING_MODE = {
    0: "自動",
    1: "0°",
    2: "20°",
    3: "45°",
    4: "70°",
    5: "90°",
}
CLIMATE_AVAILABLE_FAN_MODE = {
    0: "自動",
    1: "20%",
    2: "40%",
    3: "60%",
    4: "80%",
    5: "100%",
}
CLIMATE_MINIMUM_TEMPERATURE = 16
CLIMATE_MAXIMUM_TEMPERATURE = 30
CLIMATE_TEMPERATURE_STEP = 1.0

ON_TIMER_MIN = 0
ON_TIMER_MAX = 12
OFF_TIMER_MIN = 0
OFF_TIMER_MAX = 12

ICON_TANK = "mdi:cup-water"
ICON_HUMIDITY = "mdi:water-percent"
ICON_TIMER = "mdi:alarm"
ICON_THERMOMETER = "mdi:thermometer"

LABEL_DEHUMIDIFIER = ""
LABEL_CLIMATE = ""
LABEL_TANK = "水箱滿水"
LABEL_HUMIDITY = "環境溼度"
LABEL_ON_TIMER = "定時開機"
LABEL_OFF_TIMER = "定時關機"
LABEL_OUTDOOR_TEMPERATURE = "室外溫度"
