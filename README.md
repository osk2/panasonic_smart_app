[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
# Panasonic Smart App
This is a home assistant's integration for panasonic smart app.

## Why do I Need this?
Due to Panasonic climates' api in Taiwan are separate to global.
We can't use [python-panasonic-comfort-cloud] and [panasonic_ac] in `Home Assistant`.

So I create [python-panasonic-smart-app] and [panasonic_smart_app] integration.

# How to Install?

### via HACS
You can install the component via the `Home Assistant Community Store (HACS)` directly.

### Manually
Copy `__init__.py`, `climate.py`, and `manifest.json` to the `custom_components/panasonic_smart_app/` folder.


## Configuration
Add the following configuration in configuration.yaml:

```
climate:
  - platform: panasonic_smart_app
    username: !secret smart_app_account
    password: !secret smart_app_password
```

## Entities Available
- **climate**: Air Condition with `CZ-T007` wifi model.

# Attention
This project only test with `Panasonic air conditioner - PX series` which use `CZ-T007` wifi adapater. `CZ-T005`, `CZ-T006` or `PXGD` series might occurs some error.


---
## And..
### You can also...

<a href="https://www.buymeacoffee.com/phantas"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=phantas&button_colour=FFDD00&font_colour=000000&font_family=Poppins&outline_colour=000000&coffee_colour=ffffff"></a>


--

# Logs
How to open the logs record?

Set config in `configuration.yaml` like below:

```yaml
logger:
  default: warning
  logs:
    custom_components.panasonic_smart_app: debug
```