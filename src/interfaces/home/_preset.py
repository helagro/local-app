from typing import Literal, TypedDict


class PresetValue(TypedDict):
    level: int | None
    state: Literal['on', 'off', 'keep']
    color: str | int | None


class Preset(TypedDict):
    values: dict[str, PresetValue]
