[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/osk2/panasonic_smart_app?style=for-the-badge)
[![GitHub license](https://img.shields.io/github/license/osk2/panasonic_smart_app?style=for-the-badge)](https://github.com/osk2/panasonic_smart_app/blob/master/LICENSE)

<a href="https://www.buymeacoffee.com/osk2" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

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

1. Search `Panasonic Smart App` in the integration list
2. Follow the steps on UI to finish the configuration

# Note

### Supported Devices

See [支援的裝置 / Supported devices](https://github.com/osk2/panasonic_smart_app/discussions/42) for detail of supported devices.

### Available Entities

| Device Type      | Entity Type   | Note                                     |
| ---------------- | ------------- | ---------------------------------------- |
| General          | sensor        | Energy consumption sensor\*              |
|                  | sensor        | CO2 footprint sensor\*                   |
| AC               | climate       |                                          |
|                  | number        | On timer\*                               |
|                  | number        | Off timer                                |
|                  | sensor        | Outdoor temperature sensor               |
|                  | sensor        | PM2.5 sensor\*                           |
|                  | switch        | nanoe switch\*                           |
|                  | switch        | ECONAVI swtich\*                         |
|                  | switch        | Buzzer switch\*                          |
|                  | switch        | Turbo mode switch\*                      |
|                  | switch        | Self-clean mode switch\*                 |
|                  | switch        | Mold prevention switch\*                 |
|                  | switch        | Sleep mode switch\*                      |
|                  | select        | Motion detection mode select\*           |
|                  | select        | Indicator light select\*                 |
| Dehumidifier     | humidifier    |                                          |
|                  | number        | On timer\*                               |
|                  | number        | Off timer                                |
|                  | select        | Fan mode\*                               |
|                  | sensor        | Environment humidity sensor              |
|                  | sensor        | PM2.5 sensor\*                           |
|                  | binary_sensor | Water tank status sensor                 |
| Washing Machine  | sensor        | Countdown sensor                         |
|                  | sensor        | Device status sensor                     |
|                  | sensor        | Washing mode sensor                      |
|                  | sensor        | Washing cycle sensor                     |
| Purifier         | switch        | Power switch                             |
|                  | select        | Fan level\*                              |
|                  | switch        | nanoeX switch\*                          |
|                  | sensor        | PM2.5 sensor                             |
| Refrigerator\*\* | sensor        | Freezer temperature sensor               |
|                  | sensor        | Refrigerator temperature sensor          |
|                  | sensor        | Partial freezer temperature sensor       |
|                  | sensor        | Rapid freezing level sensor\*\*\*        |
|                  | sensor        | Winter mode sensor\*\*\*                 |
|                  | sensor        | Shopping mode sensor\*\*\*               |
|                  | sensor        | Vacation mode sensor\*\*\*               |
|                  | sensor        | Door open count sensor                   |
|                  | select        | Freezer temperature level select         |
|                  | select        | Refrigerator temperature level select    |
|                  | select        | Partial freezer temperature level select |
|                  | switch        | Stop ice making switch                   |
|                  | switch        | Quick ice making switch                  |
|                  | binary_sensor | Defrosting status sensor                 |
|                  | binary_sensor | ECONAVI status sensor                    |
|                  | binary_sensor | nanoe status sensor                      |


\*Only available if the feature is supported.

\*\*Only tested with NR-D611XGS

\*\*\*These settings should be configurable in the Panasonic App, but are currently read-only in this integration.

Note: Ensure the latest Home Assistant is installed or some entities might not be available.

For missing entities, open an issue or submit a PR 💪

### Enable Logs

⚠️ Logs may contain some sensitive information. Be very careful before you post logs.

Add the following configs to `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.panasonic_smart_app: debug
```

# License

This project is licensed under MIT license. See [LICENSE](LICENSE) file for details.
