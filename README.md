[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
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

### Tested Devices

Following devices were tested.

Feel free to report working device by opening an [issue](https://github.com/osk2/panasonic_smart_app/issues)

| Device Model | Module Type  |
| ------------ | ------------ |
| F-Y28EX      | CZ-T006      |
| F-Y24GX      | CZ-T006      |
| F-Y26JH      | _(Built-in)_ |
| CS-PX22FA2   | CZ-T007      |
| CS-PX28FA2   | CZ-T007      |
| CS-PX36FA2   | CZ-T007      |
| CS-PX50FA2   | CZ-T007      |
| CS-PX63FA2   | CZ-T007      |
| CS-QX28FA2   | CZ-T007      |
| CS-QX40FA2   | CZ-T007      |
| CS-QX71FA2   | CZ-T007      |
| CS-RX28GA2   | _(Built-in)_ |
| CS-RX36GA2   | _(Built-in)_ |
| CS-RX50GA2   | _(Built-in)_ |
| CS-RX71GA2   | _(Built-in)_ |

### Available Entities

| Device Type  | Entity Type   | Note                        |
| ------------ | ------------- | --------------------------- |
| AC           | climate       |                             |
|              | number        | On timer\*                  |
|              | number        | Off timer                   |
|              | sensor        | Outdoor temperature sensor  |
|              | switch        | nanoe switch\*              |
|              | switch        | ECONAVI swtich\*            |
|              | switch        | Buzzer switch\*             |
|              | switch        | Turbo mode switch\*         |
| Dehumidifier | humidifier    |                             |
|              | number        | On timer\*                  |
|              | number        | Off timer                   |
|              | select        | Fan mode                    |
|              | sensor        | Environment humidity sensor |
|              | sensor        | PM2.5 sensor                |
|              | binary_sensor | Water tank status sensor    |

\*Only available if feature is supported.

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
