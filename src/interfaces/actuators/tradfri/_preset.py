from typing import Literal, TypedDict


class PresetValue(TypedDict):
    level: int | None
    state: Literal['on', 'off']


class Preset(TypedDict):
    values: dict[str, PresetValue]
