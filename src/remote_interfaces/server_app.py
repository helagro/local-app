import os
import subprocess
import requests
from log import log

# ============================== TRACKING VALUES ============================= #

PRESSURE = 'weather_air_pressure'
HUM = 'hum_indoor'

LIGHT_EVE = 'light_eve'
LIGHT_NIGHT = 'light_night'
LIGHT_BEFORE_WAKE = 'light_before_wake'
LIGHT_DAWN = 'light_dawn'

TEMP_NIGHT = 'temp_night_indoor'
TEMP_EARLY = 'temp_early_indoor'

# ================================ ENVIRONMENT =============================== #

_TOOLS_URL = os.getenv("TOOLS_URL")
if not _TOOLS_URL:
    raise ValueError("TOOLS_URL environment variable is not set")
_ROUTINE_ENDPOINT = f"{_TOOLS_URL}/routines"

_AUTH_TOKEN = os.getenv("A75H")
if not _AUTH_TOKEN:
    raise ValueError("AUTH_TOKEN environment variable is not set")

# ================================== GETTING ================================= #


def get_routine(name: str) -> str | None:
    headers = {"Authorization": f"Bearer {_AUTH_TOKEN}"}
    params = {"sep": ":", "sec": "false"}

    try:
        response = requests.get(
            f"{_ROUTINE_ENDPOINT}/{name}/start",
            params=params,
            headers=headers,
        )
        response.raise_for_status()

        return response.text
    except requests.exceptions.RequestException as e:
        log_to_server(f"Failed to fetch routine: {e}")
        return None


# ================================== POSTING ================================= #


def log_to_server(content: str):
    """ prepend (location context) and space """
    log(content)
    a(f"local-app{content}")


def a(content: str, do_exec=True) -> None:
    content = content.strip()

    if not content:
        log("Empty content")
        return

    if not do_exec:
        log(f"Would have added: {content}")
        return

    script_path = os.path.expanduser('~/.dotfiles/scripts/path/task/a.sh')
    result = subprocess.run([script_path, content], capture_output=True, text=True)

    if result.returncode != 0:
        log(f"Failed to send command, error: {result.stderr}")
    else:
        log(f"A: {content}")
