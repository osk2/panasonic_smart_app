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
PLATFORMS = [
    "humidifier",
    "sensor",
    "number",
    "binary_sensor",
    "climate",
    "switch",
    "select",
]
MANUFACTURER = "Panasonic"
DEFAULT_NAME = "Panasonic Smart Application"

DEVICE_TYPE_AC = 1
DEVICE_TYPE_WASHING_MACHINE = 3
DEVICE_TYPE_DEHUMIDIFIER = 4

DATA_CLIENT = "client"
DATA_COORDINATOR = "coordinator"

CONF_PROXY = "proxy"
CONF_UPDATE_INTERVAL = "update_interval"

DEVICE_CLASS_SWITCH = "switch"

DEFAULT_UPDATE_INTERVAL = 180

DEVICE_STATUS_CODES = {
    DEVICE_TYPE_AC: [
        "0x00",  # AC power status
        "0x01",  # AC operation mode
        "0x04",  # AC current termperature
        "0x03",  # AC target temperature
        "0x02",  # AC fan level
        "0x0F",  # AC fan position (horizontal)
        "0x21",  # AC outdoor temperature
        "0x0B",  # AC on timer
        "0x0C",  # AC off timer
        "0x08",  # AC nanoeX
        "0x1B",  # AC ECONAVI
        "0x1E",  # AC buzzer
        "0x1A",  # AC turbo mode
        "0x18",  # AC self clean
        "0x05",  # AC sleep mode
        "0x17",  # AC mold prevention
        "0x11",  # AC fan position (vertical)
        "0x19",  # AC motion detection
        "0x1F",  # AC indicator light
        "0x37",  # AC PM2.5
    ],
    DEVICE_TYPE_DEHUMIDIFIER: [
        "0x00",  # Dehumidifier power status
        "0x01",  # Dehumidifier operation mode
        "0x02",  # Dehumidifier off timer
        "0x07",  # Dehumidifier humidity sensor
        "0x09",  # Dehumidifier fan direction
        "0x0D",  # Dehumidifier nanoe
        "0x50",
        "0x18",  # Dehumidifier buzzer
        "0x53",  # Dehumidifier PM2.5
        "0x55",  # Dehumidifier on timer
        "0x0A",  # Dehumidifier tank status
        "0x04",  # Dehumidifier target humidity
        "0x0E",  # Dehumidifier fan mode
    ],
    DEVICE_TYPE_WASHING_MACHINE: [
        "0x13", # Washing machine remaining washing time
        "0x14", # Washing machine timer
        "0x15", # Washing machine remaining time to trigger timer
        "0x41", # Washing machine timer for japan model
        "0x50", # Washing machine status
        "0x54", # Washing machine current mode
        "0x55", # Washing machine current cycle
        "0x61", # Washing machine dryer delay
        "0x64", # Washing machine cycle
    ],
}

DEHUMIDIFIER_MAX_HUMD = 70
DEHUMIDIFIER_MIN_HUMD = 40
DEHUMIDIFIER_AVAILABLE_HUMIDITY = {0: 40, 1: 45, 2: 50, 3: 55, 4: 60, 5: 65, 6: 70}
DEHUMIDIFIER_ON_TIMER_MIN = 0
DEHUMIDIFIER_ON_TIMER_MAX = 12
DEHUMIDIFIER_OFF_TIMER_MIN = 0
DEHUMIDIFIER_OFF_TIMER_MAX = 12

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
CLIMATE_ON_TIMER_MIN = 0
CLIMATE_ON_TIMER_MAX = 1440
CLIMATE_OFF_TIMER_MIN = 0
CLIMATE_OFF_TIMER_MAX = 1440

ICON_TANK = "mdi:cup-water"
ICON_HUMIDITY = "mdi:water-percent"
ICON_ON_TIMER = "mdi:alarm"
ICON_OFF_TIMER = "mdi:alarm-snooze"
ICON_THERMOMETER = "mdi:thermometer"
ICON_PM25 = "mdi:dots-hexagon"
ICON_NANOE = "mdi:atom"
ICON_ECONAVI = "mdi:leaf"
ICON_BUZZER = "mdi:volume-high"
ICON_TURBO = "mdi:clock-fast"
ICON_FAN = "mdi:fan"
ICON_ENERGY = "mdi:flash"
ICON_MOLD_PREVENTION = "mdi:weather-windy"
ICON_SLEEP = "mdi:sleep"
ICON_CLEAN = "mdi:broom"
ICON_LIGHT = "mdi:lightbulb-on-outline"
ICON_MOTION_SENSOR = "mdi:motion-sensor"
ICON_ARROW_LEFT_RIGHT = "mdi:arrow-left-right-bold"
ICON_CLOCK = "mdi:clock"
ICON_INFO = "mdi:information"
ICON_WASHING_MACHINE = "mdi:washing-machine"
ICON_LIST = "mdi:order-bool-descending-variant"

LABEL_DEHUMIDIFIER = ""
LABEL_CLIMATE = ""
LABEL_TANK = "水箱滿水"
LABEL_HUMIDITY = "環境溼度"
LABEL_DEHUMIDIFIER_ON_TIMER = "定時開機"
LABEL_DEHUMIDIFIER_OFF_TIMER = "定時關機"
LABEL_DEHUMIDIFIER_FAN_MODE = "風量設定"
LABEL_CLIMATE_ON_TIMER = "定時開機(分)"
LABEL_CLIMATE_ON_TIMER = "定時開機"
LABEL_CLIMATE_OFF_TIMER = "定時關機"
LABEL_CLIMATE_MOLD_PREVENTION = "乾燥防霉"
LABEL_CLIMATE_SLEEP = "舒眠"
LABEL_CLIMATE_CLEAN = "自體淨"
LABEL_CLIMATE_FAN_POSITION = "左右風向設定"
LABEL_CLIMATE_MOTION_DETECTION = "動向感應"
LABEL_CLIMATE_INDICATOR = "機體燈光"
LABEL_WASHING_MACHINE_COUNTDOWN = "剩餘洗衣時間"
LABEL_WASHING_MACHINE_STATUS = "運轉狀態"
LABEL_WASHING_MACHINE_CYCLE = "目前行程"
LABEL_WASHING_MACHINE_MODE = "目前模式"
LABEL_OUTDOOR_TEMPERATURE = "室外溫度"
LABEL_PM25 = "PM2.5"
LABEL_NANOE = "nanoe"
LABEL_ECONAVI = "ECONAVI"
LABEL_BUZZER = "操作提示音"
LABEL_TURBO = "急速"
LABEL_ENERGY = "本月耗電量"

UNIT_HOUR = "小時"
UNIT_MINUTE = "分鐘"

STATE_MEASUREMENT = "measurement"
STATE_TOTAL_INCREASING = "total_increasing"
