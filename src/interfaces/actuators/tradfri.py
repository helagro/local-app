import subprocess
from dataclasses import dataclass
from typing import Literal
import json
from log import log
from enum import Enum


class Device(Enum):
    ROOF = 65545
    PLANT = 65542
    READ = 65541
    EVE = 65537
    DESK = 65543


@dataclass
class Group:
    ids: list[int]

    def is_some_on(self):
        for id in self.ids:
            res = _exec_cmd(id, 'raw')
            if res:
                try:
                    json_res = json.loads(res)
                    control = '3312' if '3312' in json_res else '3311'

                    if json_res.get(control)[0].get('5850') == 1:
                        return True
                except Exception as e:
                    log(f"Error parsing response for device {id}: {e}, response: {res}")
        return False

    def turn_on(self):
        for id in self.ids:
            _exec_cmd(id, 'on')

    def turn_off(self):
        for id in self.ids:
            _exec_cmd(id, 'off')

    def toggle(self):
        is_on = self.is_some_on()

        if is_on:
            self.turn_off()
        else:
            self.turn_on()

    def level(self, level: int):
        for id in self.ids:
            _exec_cmd(id, 'level', str(level))


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


def get_device(name: str) -> Group:
    if name not in _devices:
        raise ValueError(f"Device '{name}' not found")

    return _devices[name]


def get_devices_string() -> str:
    return json.dumps([name for name, _ in _devices.items()])


def _exec_cmd(id: int, command: Literal['on', 'off', 'level', 'raw'], argument: str | None = None) -> str | None:
    cmd = f'tradfri {command} {id}'
    if argument:
        cmd += f' {argument}'

    try:
        result = subprocess.run(
            ['zsh', '-i', '-c', f'{cmd} >&2'],
            stdin=subprocess.DEVNULL,
            timeout=5,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stderr.strip()
    except Exception as e:
        print(f"Error executing command '{cmd}': {e}")


if __name__ == '__main__':
    _devices['lamp'].turn_off()
