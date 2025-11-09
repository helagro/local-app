import os
import requests
from log import log
from dataclasses import dataclass, field
from typing import Dict, List, Literal


@dataclass
class Config:
    doTrack: bool
    kill: bool
    reduceHeatThreshold: float
    isSummerWeather: bool
    tempCompensation: float
    tasks: Dict[Literal['eve', 'latest_dinner'], List[str]] = field(default_factory=dict)


# variables ------------------------------------------------------------------ #

_config: None | Config = None

_CONFIG_URL = os.getenv("MY_CONFIG_URL")
if not _CONFIG_URL:
    raise ValueError("MY_CONFIG_URL environment variable is not set")

# functions ------------------------------------------------------------------ #


def get_cashed() -> None | Config:
    return _config


def sync_config() -> None | Config:
    global _config

    try:
        response = requests.get(f"{_CONFIG_URL}/local-app/config.json")
        response.raise_for_status()
        data = response.json()
        _config = Config(**data)
        return _config

    except requests.exceptions.RequestException as e:
        log(f"Failed to sync config: {e}")
