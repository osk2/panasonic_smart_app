[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
![Active Installations](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json&query=%24.panasonic_smart_app.total&style=for-the-badge&label=ACTIVE%20INSTALLATIONS&color=yellow)

![GitHub release (latest version)](https://img.shields.io/github/v/release/osk2/panasonic_smart_app?style=for-the-badge)
[![GitHub license](https://img.shields.io/github/license/osk2/panasonic_smart_app?style=for-the-badge)](https://github.com/osk2/panasonic_smart_app/blob/master/LICENSE)



<a href="https://www.buymeacoffee.com/osk2" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

[繁體中文](README-zh.md) | [English](README.md)

# Panasonic Smart App

Home Assistant integration for [Panasonic Smart App](https://play.google.com/store/apps/details?id=com.panasonic.smart&hl=zh_TW&gl=US).

This integration allows you to control your Panasonic appliances.

## Note

Only Panasonic Smart App is supported. If you are using Panasonic Comfort Cloud. Use [sockless-coding/panasonic_cc](https://github.com/sockless-coding/panasonic_cc) instead.

| ![smart-app-icon](https://raw.githubusercontent.com/osk2/panasonic_smart_app/master/assets/smart-app-icon.png) | ![comfort-cloud-icon](https://raw.githubusercontent.com/osk2/panasonic_smart_app/master/assets/comfort-cloud-icon.png) | ![smart-app-plus-icon](https://raw.githubusercontent.com/osk2/panasonic_smart_app/master/assets/smart-app-plus-icon.jpg) |
| :--: | :--: | :--: |
| ✅ Supported | ❌ Unsupported | ❌ Unsupported |

This project is forked from [PhantasWeng's](https://github.com/PhantasWeng/) [panasonic_smart_app](https://github.com/PhantasWeng/panasonic_smart_app). Main differences are:

1. Implement more platforms
2. Add config flow to make setup much more easier
3. Support device info

_For all supported entities, check out [Available Entities](#available-entities)._

# Installation

### Via HACS (recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=osk2&repository=panasonic_smart_app&category=integration)

Search and install `Panasonic Smart App` in HACS

### Manually

Copy `custom_components/panasonic_smart_app` into your `custom_components/`.

# Configuration

1. Search `Panasonic Smart App` in the integration list
2. Follow the steps on UI to finish the configuration

# Note

### Supported Devices

See [支援的裝置 / Supported devices](https://github.com/osk2/panasonic_smart_app/discussions/42) for details of supported devices.

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
|                  | sensor        | Rapid freezing level sensor              |
|                  | sensor        | Winter mode sensor                       |
|                  | sensor        | Shopping mode sensor                     |
|                  | sensor        | Vacation mode sensor                     |
|                  | sensor        | Door open count sensor                   |
|                  | select        | Freezer temperature level select         |
|                  | select        | Refrigerator temperature level select    |
|                  | select        | Partial freezer temperature level select |
|                  | switch        | Stop ice making switch                   |
|                  | switch        | Quick ice making switch                  |
|                  | binary_sensor | Defrosting status sensor                 |
|                  | binary_sensor | ECONAVI status sensor                    |
|                  | binary_sensor | nanoe status sensor                      |
| ERV              | climate       |                                          |
| Smart Switches   | switch        | Individual circuit switches              |

\*Only available if the feature is supported.

\*\*Only tested with NR-D611XGS

Note: Ensure the latest Home Assistant is installed or some entities might not be available.

For missing entities, open an issue or submit a PR 💪

### How To Enable Debug Logging?

#### Recommended

Click "Enable debug logging" on the integration overview page

#### Manually

Add the following configs to `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.panasonic_smart_app: debug
```

# License

This project is licensed under MIT license. See [LICENSE](LICENSE) file for details.
