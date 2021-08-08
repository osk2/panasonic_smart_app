{% if prerelease %}
Please note that this is a beta version which is still undergoing final testing before its official release.

Following documentation may be out-dated or not for beta release

---

請注意，目前版本為 Beta 版，此版本仍在開發或測試中，可能會發生某些未預期的情況或錯誤，且下列文件可能不適用於此版本，請斟酌使用
{% endif %}

# Panasonic Smart App

Home Assistant integration for [Panasonic Smart App](https://play.google.com/store/apps/details?id=com.panasonic.smart&hl=zh_TW&gl=US).

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

| Device Type  | Entity Type   | Note                         |
| ------------ | ------------- | ---------------------------- |
| AC           | climate       |                              |
|              | number        | On timer (Only if supported) |
|              | number        | Off timer                    |
|              | sensor        | Outdoor temperature sensor   |
| Dehumidifier | humidifier    |                              |
|              | number        | On timer (Only if supported) |
|              | number        | Off timer                    |
|              | select        | Fan mode                     |
|              | sensor        | Environment humidity sensor  |
|              | sensor        | PM2.5 sensor                 |
|              | binary_sensor | Water tank status sensor     |

For missing entities, open an [issue](https://github.com/osk2/panasonic_smart_app/issues) or submit a PR 💪

### Enable Logs

Add following configs to `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.panasonic_smart_app: debug
```
