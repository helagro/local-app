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
            _exec_cmd(id, 'on')

    def turn_off(self):
        self.is_on = False
        for id in self.ids:
            _exec_cmd(id, 'off')

    def toggle(self):
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    def level(self, level: int):
        for id in self.ids:
            _exec_cmd(id, 'level', str(level))


_devices = {'eve': Device(ids=[65537]), 'day': Device(ids=[65541, 65542, 65543]), 'read': Device(ids=[65541])}


def get_device(name: Literal['eve', 'day', 'read'] | str) -> Device:
    if name not in _devices:
        raise ValueError(f"Device '{name}' not found")

    return _devices[name]


def get_devices() -> dict[str, Device]:
    return _devices


def _exec_cmd(id: int, command: Literal['on', 'off', 'level'], argument: str | None = None):
    cmd = f'tradfri {command} {id}'
    if argument:
        cmd += f' {argument}'

    subprocess.run(['zsh', '-i', '-c', cmd], stdin=subprocess.DEVNULL, timeout=5)


if __name__ == '__main__':
    _devices['lamp'].turn_off()
