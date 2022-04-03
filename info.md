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

For missing entities, open an [issue](https://github.com/osk2/panasonic_smart_app/issues) or submit a PR 💪

### Enable Logs

Add following configs to `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.panasonic_smart_app: debug
```
