from typing import Literal, TypedDict


class PresetValue(TypedDict):
    level: int | None
    state: Literal['on', 'off', 'keep']


class Preset(TypedDict):
    values: dict[str, PresetValue]
