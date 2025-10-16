import subprocess
from dataclasses import dataclass
from typing import Literal


@dataclass
class Device:
    id: int
    is_on: bool = False

    def turn_on(self):
        self.is_on = True
        _exec_cmd('on', id=self.id)

    def turn_off(self):
        self.is_on = False
        _exec_cmd('off', id=self.id)

    def toggle(self):
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()


_devices = {
    'lamp': Device(id=65537),
}


def get_device(name: Literal['lamp']) -> Device:
    return _devices[name]


def _exec_cmd(command: Literal['on', 'off'], id: int):
    cmd = f'tradfri {command} {id}'
    subprocess.run(['zsh', '-i', '-c', cmd])


if __name__ == '__main__':
    _devices['lamp'].turn_off()
