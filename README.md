[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/osk2/panasonic_smart_app?style=for-the-badge)
[![GitHub license](https://img.shields.io/github/license/osk2/panasonic_smart_app?style=for-the-badge)](https://github.com/osk2/panasonic_smart_app/blob/master/LICENSE)

[繁體中文](README-zh.md) | [English](README.md)

# Panasonic Smart App

Home Assistant integration for [Panasonic Smart App](https://play.google.com/store/apps/details?id=com.panasonic.smart&hl=zh_TW&gl=US).

This integration allows you to control your Panasonic appliances.

## Note

Only Panasonic Smart App is supported. If you are using Panasonic Comfort Cloud. Use [sockless-coding/panasonic_cc](https://github.com/sockless-coding/panasonic_cc) instead.

| ![smart-app-icon](https://raw.githubusercontent.com/osk2/panasonic_smart_app/master/assets/smart-app-icon.png) | ![comfort-cloud-icon](https://raw.githubusercontent.com/osk2/panasonic_smart_app/master/assets/comfort-cloud-icon.png) |
| :------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------: |
|                                                  ✅ Supported                                                  |                                                     ❌ Unsupported                                                     |

This project is forked from [PhantasWeng's](https://github.com/PhantasWeng/) [panasonic_smart_app](https://github.com/PhantasWeng/panasonic_smart_app). Main differences are:

1. Implement more platforms
2. Add config flow to make setup much more easier
3. Support device info

_For all supported entities, check out [Available Entities](#available-entities)._

# Installation

### Via HACS (recommended)

Search and install `Panasonic Smart App` in HACS

### Manually

Copy `custom_components/panasonic_smart_app` into your `custom_components/`.

# Configuration

1. Search `Panasonic Smart App` in integration list
2. Follow steps on UI to finish configuration

# Note

### Supported Devices

See [支援的裝置 / Supported devices](https://github.com/osk2/panasonic_smart_app/discussions/42) for detail of supported devices.

### Available Entities

| Device Type     | Entity Type   | Note                           |
| --------------- | ------------- | ------------------------------ |
| AC              | climate       |                                |
|                 | number        | On timer\*                     |
|                 | number        | Off timer                      |
|                 | sensor        | Outdoor temperature sensor     |
|                 | sensor        | PM2.5 sensor                   |
|                 | switch        | nanoe switch\*                 |
|                 | switch        | ECONAVI swtich\*               |
|                 | switch        | Buzzer switch\*                |
|                 | switch        | Turbo mode switch\*            |
|                 | switch        | Self-clean mode switch\*       |
|                 | switch        | Mold prevention switch\*       |
|                 | switch        | Sleep mode switch\*            |
|                 | select        | Motion detection mode select\* |
|                 | select        | Indicator light select\*       |
| Dehumidifier    | humidifier    |                                |
|                 | number        | On timer\*                     |
|                 | number        | Off timer                      |
|                 | select        | Fan mode\*                     |
|                 | sensor        | Environment humidity sensor    |
|                 | sensor        | PM2.5 sensor                   |
|                 | binary_sensor | Water tank status sensor       |
| Washing Machine | sensor        | Countdown sensor               |
|                 | sensor        | Device status sensor           |
|                 | sensor        | Washing mode sensor            |
|                 | sensor        | Washing cycle sensor           |

\*Only available if feature is supported.

Note: Make sure latest Home Assistant is installed or some entities might not available.

For missing entities, open an issue or submit a PR 💪

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
