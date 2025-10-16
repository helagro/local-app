import subprocess
from dataclasses import dataclass
from typing import Literal


@dataclass
class Device:
    ids: list[int]
    is_on: bool = False

    def turn_on(self):
        self.is_on = True
        for id in self.ids:
            _exec_cmd('on', id)

    def turn_off(self):
        self.is_on = False
        for id in self.ids:
            _exec_cmd('off', id)

    def toggle(self):
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()


_devices = {'eve': Device(ids=[65537]), 'day': Device(ids=[65541, 65542, 65543])}


def get_device(name: Literal['eve', 'day']) -> Device:
    return _devices[name]


def _exec_cmd(command: Literal['on', 'off'], id: int):
    cmd = f'tradfri {command} {id}'
    subprocess.run(['zsh', '-i', '-c', cmd], stdin=subprocess.DEVNULL, timeout=5)


if __name__ == '__main__':
    _devices['lamp'].turn_off()
