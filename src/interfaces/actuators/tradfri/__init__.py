from dataclasses import dataclass
import json
from interfaces.actuators.tradfri._device import Device, Group
from interfaces.actuators.tradfri._preset import Preset
from interfaces.api.config import get_cashed
from log import log

_devices = {
    'all': Group(ids=[Device.EVE.value, Device.READ.value, Device.PLANT.value, Device.DESK.value, Device.ROOF.value]),
    # Specifics:
    'day': Group(ids=[Device.READ.value, Device.PLANT.value, Device.DESK.value, Device.ROOF.value]),
    'out': Group(ids=[Device.EVE.value, Device.READ.value, Device.DESK.value, Device.ROOF.value]),
    'chill': Group(ids=[Device.EVE.value, Device.PLANT.value, Device.DESK.value, Device.ROOF.value]),
    # Singles:
    'eve': Group(ids=[Device.EVE.value]),
    'read': Group(ids=[Device.READ.value]),
    'plant': Group(ids=[Device.PLANT.value]),
    'roof': Group(ids=[Device.ROOF.value]),
}


def exec_preset_by_name(name: str):
    config = get_cashed()
    if not config:
        raise ValueError("No config found")

    presets: dict[str, Preset] = config.presets
    preset = presets.get(name)
    if not preset:
        raise ValueError(f"Preset '{name}' not found in config")

    log(f"Executing preset: {name}")
    _exec_preset(preset)


def _exec_preset(preset: Preset):

    for device_name, config in preset['values'].items():
        if device_name not in _devices:
            log(f"Device '{device_name}' not found in preset")
            continue

        device = _devices[device_name]

        if 'state' in config:
            state = config['state']
            if state == 'on':
                device.turn_on()
            elif state == 'off':
                device.turn_off()

        if 'level' in config:
            level = config['level']
            if level:
                device.level(level)


# get device(s) ----------------------------------------------------------------- #


def get_device(name: str) -> Group:
    if name not in _devices:
        raise ValueError(f"Device '{name}' not found")

    return _devices[name]


def get_devices_string() -> str:
    return json.dumps([name for name, _ in _devices.items()])


# =================================== START ================================== #

if __name__ == '__main__':
    _devices['lamp'].turn_off()
