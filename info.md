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
