import subprocess
from dataclasses import dataclass
from typing import Literal
import json
from log import log


@dataclass
class Device:
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


_devices = {'eve': Device(ids=[65537]), 'day': Device(ids=[65541, 65542, 65543]), 'read': Device(ids=[65541])}


def get_device(name: Literal['eve', 'day', 'read'] | str) -> Device:
    if name not in _devices:
        raise ValueError(f"Device '{name}' not found")

    return _devices[name]


def get_devices() -> dict[str, Device]:
    return _devices


def _exec_cmd(id: int, command: Literal['on', 'off', 'level', 'raw'], argument: str | None = None) -> str | None:
    cmd = f'tradfri {command} {id}'
    if argument:
        cmd += f' {argument}'

    try:
        result = subprocess.run(
            ['zsh', '-i', '-c', cmd],
            stdin=subprocess.DEVNULL,
            timeout=5,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error executing command '{cmd}': {e}")


if __name__ == '__main__':
    _devices['lamp'].turn_off()
