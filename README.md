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
    username: !secret username
    password: !secret password
    appToken: !secret appToken
```

## Entities Aviables
- **climate**: Air Condition with `CZ-T007` wifi model.

# Attention
This project only test with `Panasonic air conditioner - PX series` which use `CZ-T007` wifi adapater. `CZ-T005`, `CZ-T006` or `PXGD` series might occurs some error.


[python-panasonic-comfort-cloud]: https://github.com/lostfields/python-panasonic-comfort-cloud

[panasonic_ac]: https://github.com/djbulsink/panasonic_ac

[python-panasonic-smart-app]: https://github.com/PhantasWeng/python-panasonic-smart-app

[panasonic_smart_app]: https://github.com/PhantasWeng/panasonic_smart_app
