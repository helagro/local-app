import os
import requests
from log import log
from dataclasses import dataclass, field
from typing import Dict, List, TypedDict, Literal

# home config ----------------------------------------------------------------------- #

class PresetValue(TypedDict):
    level: int | None
    state: Literal['on', 'off', 'keep']
    color: str | int | None


class Preset(TypedDict):
    values: dict[str, PresetValue]
    
@dataclass
class HomeConfig:
    homeAssistantPath: str

    colors: Dict[str, str] = field(default_factory=dict)
    devices: Dict[str, str] = field(default_factory=dict)
    groups: Dict[str, List[str]] = field(default_factory=dict)
    presets: Dict[str, Preset] = field(default_factory=dict)

# sensor config -------------------------------------------------------------- #

@dataclass
class SensorConfig:
    doTrack: bool
    trackVoc: bool
    
    reduceHeatThreshold: float
    tempCompensation: float
    externalTempCompensation: float

# base config ---------------------------------------------------------------- #

@dataclass
class Config:
    doBlinkTimer: bool
    alertFrequency: int
    pauseDelay: int
    alertLamp: str
    maxBreakMin: int

    kill: bool

    isSummerWeather: bool

    home: HomeConfig
    sensor: SensorConfig


# variables ------------------------------------------------------------------ #

_config: None | Config = None

_CONFIG_URL = os.getenv("MY_CONFIG_URL")
if not _CONFIG_URL:
    raise ValueError("MY_CONFIG_URL environment variable is not set")

# functions ------------------------------------------------------------------ #


def get_cached() -> None | Config:
    return _config


def sync_config() -> None | Config:
    global _config

    try:
        response = requests.get(f"{_CONFIG_URL}/local-app/config.json")
        response.raise_for_status()
        data = response.json()
        _config = Config(
            doBlinkTimer=data.get("doBlinkTimer", False),
            alertFrequency=data.get("alertFrequency", 0),
            pauseDelay=data.get("pauseDelay", 0),
            alertLamp=data.get("alertLamp", ""),
            maxBreakMin=data.get("maxBreakMin", 0),
            kill=data.get("kill", False),
            isSummerWeather=data.get("isSummerWeather", False),

            home=HomeConfig(
                **data.get("home", {})
            ),
            sensor=SensorConfig(
                **data.get("sensor", {})
            ),
        )
        return _config

    except requests.exceptions.RequestException as e:
        log(f"Failed to sync config: {e}")
