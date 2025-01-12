import subprocess
import os
import requests
import sys

script_dir = os.path.expanduser("~/.dotfiles/scripts/lang/python")
sys.path.append(script_dir)
import exist

# ----------------------- CONFIG VALUES ---------------------- #

REDUCE_HEAT_THRESHOLD = 'reduceHeatThreshold'

# -------------------------- TRACKING VALUES -------------------------- #

PRESSURE = 'weather_air_pressure'
HUM = 'hum_indoor'

LIGHT_EVE = 'light_eve'
LIGHT_NIGHT = 'light_night'
LIGHT_BEFORE_WAKE = 'light_before_wake'
LIGHT_DAWN = 'light_dawn'

TEMP_NIGHT = 'temp_night_indoor'
TEMP_EARLY = 'temp_early_indoor'

# -------------------------- ENVIRONMENT ------------------------- #

_TOOLS_URL = os.getenv("TOOLS_URL")
if not _TOOLS_URL:
    raise ValueError("TOOLS_URL environment variable is not set")
_ROUTINE_ENDPOINT = f"{_TOOLS_URL}/routines"

_CONFIG_URL = os.getenv("MY_CONFIG_URL")
if not _CONFIG_URL:
    raise ValueError("MY_CONFIG_URL environment variable is not set")

_AUTH_TOKEN = os.getenv("A75H")
if not _AUTH_TOKEN:
    raise ValueError("AUTH_TOKEN environment variable is not set")

# -------------------------- UNCATEGORISED FUNCTIONS ------------------------- #


def get_config(name: str) -> str | None:
    try:
        response = requests.get(f"{_CONFIG_URL}/env-tracker/settings.json")
        response.raise_for_status()
        json = response.json()

        return json[name] if name else json
    except requests.exceptions.RequestException as e:
        log(f"Failed to fetch config: {e}")
        return None


def is_away() -> bool:
    if get_config('doTrack') == False: return True

    try:
        away_dict = exist.values('away', 1, None)
        return list(away_dict.values())[0] == 1
    except Exception as e:
        log(f"/is_away - failed to check if away: {e}")
        return False


# ----------------------------- A ---------------------------- #


def log(content: str):
    """ prepend (location context) and space """
    print(content)
    a(f"env-tracker{content}")


def a(content: str, do_exec=True) -> None:
    content = content.strip()

    if not content:
        print("Empty content")
        return

    if not do_exec:
        print(f"Would have added: {content}")
        return

    script_path = os.path.expanduser('~/.dotfiles/scripts/path/a.sh')
    result = subprocess.run([script_path, content], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Failed to send command, error: {result.stderr}")
    else:
        print(f"A: {content}")


# -------------------------- ROUTINE ------------------------- #


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
        log(f"Failed to fetch routine: {e}")
        return None


if __name__ == "__main__":
    print(get_routine("detach"))
    print(get_config("reduceHeatThreshold"))
