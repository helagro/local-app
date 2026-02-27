import json
from interfaces.home._device import Group
from interfaces.home._preset import Preset
from log import log
import interfaces.home._api as api


def exec_preset_by_name(name: str, state_mode: str | None = None):
    from interfaces.api.config import get_cashed
    config = get_cashed()
    if not config:
        raise ValueError("No config found")

    presets: dict[str, Preset] = config.presets
    preset = presets.get(name)
    if not preset:
        raise ValueError(f"Preset '{name}' not found in config")

    log(f"Executing preset: {name} with mode: {state_mode}")
    _exec_preset(preset, state_mode)


def _exec_preset(preset: Preset, state_mode: str | None):
    for device_name, config in preset['values'].items():
        device = get_device(device_name)
        was_on = device.is_some_on()

        level = config.get('level')
        state = config.get('state')
        color = config.get('color')

        if state_mode == 'keep':
            should_be_on = was_on
        else:
            should_be_on: bool = (state == 'on' or level is not None)

        state_string = 'on' if should_be_on else 'off'
        payload: api.Payload = {}

        if level is not None:
            payload['brightness'] = level
        if color is not None:
            payload.update(api.get_color_dict(color))

        device.switch_custom(state_string, payload)


# get device(s) ----------------------------------------------------------------- #


def get_device(name: str) -> Group:
    groups = _get_groups()

    if name not in groups:
        raise ValueError(f"Device '{name}' not found")

    return Group(groups[name])


def _get_groups() -> dict[str, list[str]]:
    from interfaces.api.config import get_cashed
    config = get_cashed()
    if not config:
        raise ValueError("No config found")

    groups: dict[str, list[str]] = config.groups
    devices = config.devices

    for device_name, _ in devices.items():
        groups[device_name] = [device_name]

    return groups


def get_devices_string() -> str:
    return json.dumps([name for name, _ in _get_groups().items()])


# =================================== START ================================== #

if __name__ == '__main__':
    pass
    # _get_groups()['lamp'].turn_off()
