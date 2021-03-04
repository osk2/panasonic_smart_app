[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

# Panasonic Smart App
Home Assistant integration for Panasonic Smart App.

# Installation

### Via HACS
Install this component via HACS is highly recommended

### Manually
Copy `custom_components/panasonic_smart_app` into `custom_components/` folder.

# Configuration
Add following configuration in `configuration.yaml`:

```
panasonic_smart_app:
    username: !secret smart_app_account
    password: !secret smart_app_password
```

# Note

## Slow Startup
As you may already know, the API is so slow at processing our request.

It may takes up to 30 seconds to boot up Home Assistant (depend on device count), so just be patient.

## Available Entities
Following devices are tested and supported by this component:

- **climate**: AC with `CZ-T007` wifi module.
- **humidifier**: Dehumidifier with `CZ-T006` wifi module.

## Enable Logs
Add following configs to `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.panasonic_smart_app: debug
```
