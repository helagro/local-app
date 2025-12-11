from dataclasses import dataclass
from enum import Enum
import json
import subprocess
from typing import Literal

from log import log


@dataclass
class Group:
    ids: list[str]

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


# ================================== HELPERS ================================= #


def _exec_cmd(name: str, command: Literal['on', 'off', 'level', 'raw'], argument: str | None = None) -> str | None:
    id = _get_id(name)

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


def _get_id(name: str) -> int:
    from interfaces.api.config import get_cashed

    config = get_cashed()
    if not config:
        raise ValueError("No config found")

    devices: dict[str, int] = config.devices

    if name not in devices:
        raise ValueError(f"Device '{name}' not found in config")

    return devices[name]
