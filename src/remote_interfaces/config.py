import os
import requests
from log import log

REDUCE_HEAT_THRESHOLD = 'reduceHeatThreshold'
IS_SUMMER_WEATHER = 'isSummerWeather'

_CONFIG_URL = os.getenv("MY_CONFIG_URL")
if not _CONFIG_URL:
    raise ValueError("MY_CONFIG_URL environment variable is not set")


def get_config(name: str | None = None) -> str | dict | None | float:
    try:
        response = requests.get(f"{_CONFIG_URL}/local-app/settings.json")
        response.raise_for_status()
        json = response.json()

        return json[name] if name else json
    except requests.exceptions.RequestException as e:
        log(f"Failed to fetch config: {e}")
        return None
