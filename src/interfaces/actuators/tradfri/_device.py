from dataclasses import dataclass
import json
import subprocess
from typing import Literal
import os
from pathlib import Path

from log import log


@dataclass
class Group:
    ids: list[str]

    # getters -------------------------------------------------------------------- #

    def amt_on(self) -> int:
        count = 0
        for id in self.ids:
            if _is_on(id):
                count += 1

        return count

    def is_some_on(self) -> bool:
        for id in self.ids:
            if _is_on(id):
                return True

        return False

    # actions -------------------------------------------------------------------- #

    def turn_on(self):
        log(f"Turning on group with ids: {self.ids}")
        for id in self.ids:
            _exec_cmd(id, 'on')

    def turn_off(self):
        log(f"Turning off group with ids: {self.ids}")
        for id in self.ids:
            _exec_cmd(id, 'off')

    def toggle(self):
        is_on = self.is_some_on()

        if is_on:
            self.turn_off()
        else:
            self.turn_on()

    def toggle_individually(self):
        log(f"Toggling group individually with ids: {self.ids}")
        for id in self.ids:
            if _is_on(id):
                _exec_cmd(id, 'off')
            else:
                _exec_cmd(id, 'on')

    def level(self, level: int):
        log(f"Setting level {level} for group with ids: {self.ids}")
        for id in self.ids:
            _exec_cmd(id, 'level', str(level))


# ================================== HELPERS ================================= #


def _exec_cmd(name: str, command: Literal['on', 'off', 'level', 'raw'], argument: str | None = None) -> str | None:
    id = _get_id(name)

    cmd = f'tradfri {command} {id}'
    if argument:
        cmd += f' {argument}'

    venv_bin = str(Path.home() / "Developer/local-app/.venv/bin")
    env = os.environ.copy()
    env["PATH"] = f"{venv_bin}:{env.get('PATH','')}"

    try:
        result = subprocess.run(
            ['zsh', '-i', '-c', f'{cmd} >&2'],
            stdin=subprocess.DEVNULL,
            timeout=5,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        return result.stderr.strip()
    except Exception as e:
        print(f"Error executing command '{cmd}': {e}")


def _is_on(id: str) -> bool:
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


def _get_id(name: str) -> int:
    from interfaces.api.config import get_cashed

    config = get_cashed()
    if not config:
        raise ValueError("No config found")

    devices: dict[str, int] = config.devices

    if name not in devices:
        raise ValueError(f"Device '{name}' not found in config")

    return devices[name]
