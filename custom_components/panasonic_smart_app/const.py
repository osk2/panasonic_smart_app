"""Contants for Panasonic Smart App integration"""

from homeassistant.components.climate import HVACMode

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
DEVICE_TYPE_REFRIGERATOR = 2
DEVICE_TYPE_WASHING_MACHINE = 3
DEVICE_TYPE_DEHUMIDIFIER = 4
DEVICE_TYPE_PURIFIER = 8
DEVICE_TYPE_ERV = 14
DEVICE_TYPE_SWITCH = 17

DATA_CLIENT = "client"
DATA_COORDINATOR = "coordinator"

CONF_PROXY = "proxy"
CONF_UPDATE_INTERVAL = "update_interval"

DEVICE_CLASS_SWITCH = "switch"
DEVICE_CLASS_DEHUMIDIFIER = "dehumidifier"

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
    DEVICE_TYPE_REFRIGERATOR: [
        "0x00",  # Refrigerator freezer temperature setting
        "0x01",  # Refrigerator refrigerator temperature setting
        "0x57",  # Refrigerator partial freezing temperature setting
        "0x03",  # Refrigerator freezer temperature display
        "0x05",  # Refrigerator refrigerator temperature display
        "0x58",  # Refrigerator partial freezing temperature display
        "0x50",  # Refrigerator defrosting status
        "0x0C",  # Refrigerator ECO status
        "0x61",  # Refrigerator nanoe status
        "0x52",  # Refrigerator stop ice making status
        "0x53",  # Refrigerator quick ice making status
        "0x56",  # Refrigerator rapid freezing status
        "0x5A",  # Refrigerator winter mode
        "0x5B",  # Refrigerator shopping mode
        "0x5C",  # Refrigerator vacation mode
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
        "0x56",  # Dehumidifier PM1.0
    ],
    DEVICE_TYPE_WASHING_MACHINE: [
        "0x13",  # Washing machine remaining washing time
        "0x14",  # Washing machine timer
        "0x15",  # Washing machine remaining time to trigger timer
        "0x41",  # Washing machine timer for japan model
        "0x50",  # Washing machine status
        "0x54",  # Washing machine current mode
        "0x55",  # Washing machine current cycle
        "0x61",  # Washing machine dryer delay
        "0x64",  # Washing machine cycle
    ],
    DEVICE_TYPE_PURIFIER: [
        "0x00",  # Purifier power status
        "0x01",  # Purifier fan level
        "0x07",  # Purifier nanoeX
        "0x50",  # Purifier PM 2.5
    ],
    DEVICE_TYPE_ERV: [
        "0x00",  # ERV power status
        "0x15",  # ERV operation mode
        "0x56",  # ERV fan level
    ],
    DEVICE_TYPE_SWITCH: [
        "0x70",  # Switch power status
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
    {"key": HVACMode.OFF, "mappingCode": -1},
    {"key": HVACMode.COOL, "mappingCode": 0},
    {"key": HVACMode.DRY, "mappingCode": 1},
    {"key": HVACMode.FAN_ONLY, "mappingCode": 2},
    {"key": HVACMode.AUTO, "mappingCode": 3},
    {"key": HVACMode.HEAT, "mappingCode": 4},
]
CLIMATE_AVAILABLE_PRESET = {
    0: "Cool",
    1: "Dry",
    2: "Purify",
    3: "Auto",
    4: "Heat"
}
CLIMATE_AVAILABLE_SWING_MODE = {
    0: "Auto",
    1: "0°",
    2: "20°",
    3: "45°",
    4: "70°",
    5: "90°",
}
CLIMATE_AVAILABLE_FAN_MODE = {
    0: "Auto",
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
ICON_NANOEX = "mdi:atom"
ICON_ECONAVI = "mdi:leaf"
ICON_BUZZER = "mdi:volume-high"
ICON_TURBO = "mdi:clock-fast"
ICON_FAN = "mdi:fan"
ICON_FAN_POSITION = "mdi:arrow-oscillating"
ICON_ENERGY = "mdi:flash"
ICON_REFRIGERATOR = "mdi:fridge"
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
ICON_PURIFIER = "mdi:air-purifier"
ICON_BUZZER = "mdi:volume-high"
ICON_DEFROSTING = "mdi:car-defrost-rear"
ICON_STOP_ICE_MAKING = "mdi:snowflake-off"
ICON_QUICK_ICE_MAKING = "mdi:snowflake-variant"
ICON_REFRIGERATOR_FREEZER = "mdi:snowflake"
ICON_REFRIGERATOR_REFRIGERATOR = "mdi:fridge"
ICON_REFRIGERATOR_PARTIAL_FREEZING = "mdi:food-steak"
ICON_REFRIGERATOR_RAPID_FREEZING = "mdi:snowflake-alert"
ICON_REFRIGERATOR_WINTER_MODE = "mdi:snowflake"
ICON_REFRIGERATOR_SHOPPING_MODE = "mdi:cart"
ICON_REFRIGERATOR_VACATION_MODE = "mdi:beach"

ICON_CO2_FOOTPRINT = "mdi:molecule-co2"

LABEL_DEHUMIDIFIER = ""
LABEL_CLIMATE = ""
LABEL_SMART_SWITCH = "Smart switch"
LABEL_TANK = "Tank full"
LABEL_HUMIDITY = "Humidity"
LABEL_DEHUMIDIFIER_BUZZER = "Buzzer"
LABEL_DEHUMIDIFIER_ON_TIMER = "On timer"
LABEL_DEHUMIDIFIER_OFF_TIMER = "Off timer"
LABEL_DEHUMIDIFIER_FAN_MODE = "Fan mode"
LABEL_DEHUMIDIFIER_FAN_POSITION = "Fan angle"
LABEL_DEHUMIDIFIER_FAN_LEVEL = "Fan speed"
LABEL_CLIMATE_ON_TIMER = "On timer"
LABEL_CLIMATE_OFF_TIMER = "Off timer"
LABEL_CLIMATE_MOLD_PREVENTION = "Anti-mildew"
LABEL_CLIMATE_SLEEP = "Sleep"
LABEL_CLIMATE_CLEAN = "Purify"
LABEL_CLIMATE_FAN_POSITION = "Fan angle"
LABEL_CLIMATE_MOTION_DETECTION = "Motion detection"
LABEL_CLIMATE_INDICATOR = "Brightness"
LABEL_WASHING_MACHINE_COUNTDOWN = "Countdown"
LABEL_WASHING_MACHINE_STATUS = "Status"
LABEL_WASHING_MACHINE_CYCLE = "Cycle"
LABEL_WASHING_MACHINE_MODE = "Mode"
LABEL_REFRIGERATOR_FREEZER_TEMPERATURE_DISPLAY = "Show temperature"
LABEL_REFRIGERATOR_REFRIGERATOR_TEMPERATURE_DISPLAY = "Show temperature"
LABEL_REFRIGERATOR_PARTIAL_FREEZING_TEMPERATURE_DISPLAY = "Show temperature"
LABEL_REFRIGERATOR_DEFROSTING_STATUS = "Status"
LABEL_REFRIGERATOR_STOP_ICE_MAKING = "Stop icecubes"
LABEL_REFRIGERATOR_QUICK_ICE_MAKING = "Quick icecubes"
LABEL_REFRIGERATOR_RAPID_FREEZING_STATUS = "Rapid freeze"
LABEL_OUTDOOR_TEMPERATURE = "Outdoor temperature"
LABEL_PURIFIER_FAN_LEVEL = "Fan level"
LABEL_PM25 = "PM2.5"
LABEL_NANOE = "nanoe"
LABEL_NANOEX = "nanoeX"
LABEL_ECONAVI = "ECONAVI"
LABEL_BUZZER = "Buzzer"
LABEL_TURBO = "Boost"
LABEL_ENERGY = "Energy consumption"
LABEL_REFRIGERATOR_OPEN_DOOR = "Door openings"
LABEL_CO2_FOOTPRINT = ""
LABEL_POWER = "Power"
LABEL_ERV = ""

UNIT_HOUR = "hours"
UNIT_MINUTE = "minutes"

STATE_MEASUREMENT = "measurement"
STATE_TOTAL_INCREASING = "total_increasing"
