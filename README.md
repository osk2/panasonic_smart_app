[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

[繁體中文](README-zh.md) | [English](README.md)

# Panasonic Smart App

Home Assistant integration for [Panasonic Smart App](https://play.google.com/store/apps/details?id=com.panasonic.smart&hl=zh_TW&gl=US).

# Installation

### Via HACS (highly recommended)

You will need to add this repository into HACS first

1. Click HACS 3-dots button at top right corner
2. Click "Custom repositories"
3. Paste `https://github.com/osk2/panasonic_smart_app` into URL field
4. Change `Category` to "Integration"

### Manually

Copy `custom_components/panasonic_smart_app` into your `custom_components/`

# Configuration

1. Search `Panasonic Smart App` in integration list
2. Follow steps on UI to finish configuration

# Note

### Available Entities

| Device Type  | Entity Type   | Note                         |
| ------------ | ------------- | ---------------------------- |
| AC           | climate       |                              |
|              | sensor        | Outdoor temperature sensor   |
| Dehumidifier | humidifier    |                              |
|              | number        | On timer (Only if supported) |
|              | number        | Off timer                    |
|              | sensor        | Environment humidity sensor  |
|              | binary_sensor | Water tank status sensor     |

### Enable Logs

Add following configs to `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.panasonic_smart_app: debug
```

# License

This project is licensed under MIT license. See [LICENSE](LICENSE) file for details.
