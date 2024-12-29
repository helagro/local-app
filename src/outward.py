import subprocess
import os
import requests
import sys
import re

script_dir = os.path.expanduser("~/.dotfiles/scripts")
sys.path.append(script_dir)
import exist

A_PATTERN = r'^[a-zA-Z0-9\s\-_\.]+$'

# -------------------------- VALUES -------------------------- #

PRESSURE = 'weather_air_pressure'
HUM = 'hum_indoor'

LIGHT_EVE = 'light_eve'
LIGHT_NIGHT = 'light_night'
LIGHT_BEFORE_WAKE = 'light_before_wake'
LIGHT_DAWN = 'light_dawn'

TEMP_NIGHT = 'temp_night_indoor'
TEMP_EARLY = 'temp_early_indoor'

# -------------------------- ENVIRONMENT ------------------------- #

ROUTINE_ENDPOINT = os.getenv("ROUTINE_ENDPOINT")
if not ROUTINE_ENDPOINT:
    raise ValueError("SECRET_ENDPOINT environment variable is not set")

# -------------------------- IS AWAY ------------------------- #


def is_away() -> bool:
    try:
        away_dict = exist.main('away', 1, None)
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
    if not re.fullmatch(A_PATTERN, content):
        print(f"Invalid content: {content}")
        return

    if not do_exec:
        print(f"Would have added: {content}")
        return

    result = subprocess.run(["zsh", "-c", f"source ~/.zshrc && a {content}"], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Failed to send command, error: {result.stderr}")
    else:
        print(f"A: {content}")


# -------------------------- ROUTINE ------------------------- #


def get_routine(name: str) -> str | None:
    try:
        response = requests.get(ROUTINE_ENDPOINT, params={"q": name})
        response.raise_for_status()
        return _format_time(response.text)
    except requests.exceptions.RequestException as e:
        log(f"Failed to fetch routine: {e}")
        return None


def _format_time(time_str):
    time_str = time_str.replace('.', ':')
    parts = time_str.split(':')

    hours = parts[0].zfill(2)
    minutes = parts[1].zfill(2)

    return f"{hours}:{minutes}"
