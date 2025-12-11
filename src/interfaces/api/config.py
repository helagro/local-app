import os
import requests
from interfaces.actuators.tradfri._preset import Preset
from log import log
from dataclasses import dataclass, field
from typing import Dict, List, Literal


@dataclass
class Config:
    doBlinkTimer: bool
    alertFrequency: int
    pauseDelay: int
    alertLamp: str

    doTrack: bool
    kill: bool
    reduceHeatThreshold: float
    isSummerWeather: bool
    tempCompensation: float

    devices: Dict[str, int] = field(default_factory=dict)
    groups: Dict[str, List[str]] = field(default_factory=dict)
    presets: Dict[str, Preset] = field(default_factory=dict)

    tasks: Dict[Literal['eve', 'latestDinner'], List[str]] = field(default_factory=dict)


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
