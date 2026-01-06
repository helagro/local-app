import json
from interfaces.actuators.tradfri._device import Group
from interfaces.actuators.tradfri._preset import Preset
from log import log


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

        if 'level' in config:
            level = config['level']
            if level:
                device.level(level)

        if 'state' in config:
            state = config['state']
            if state == 'on':
                device.turn_on()
            elif state == 'off':
                device.turn_off()
            elif (state == 'keep' or state_mode == 'keep') and not was_on:
                device.turn_off()


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
