from dataclasses import dataclass
import interfaces.home._api as api


@dataclass
class Group:
    device_names: list[str]

    def __post_init__(self):
        from interfaces.api.config import get_cashed

        config = get_cashed()
        if not config:
            raise Exception("Config not loaded")

        self.device_ids: list[str] = [config.devices[name] for name in self.device_names]

    # getters -------------------------------------------------------------------- #

    def amt_on(self) -> int:
        count = 0
        for id in self.device_ids:
            if api.is_on(id):
                count += 1

        return count

    def is_some_on(self) -> bool:
        for id in self.device_ids:
            if api.is_on(id):
                return True

        return False

    # switch actions -------------------------------------------------------------------- #

    def turn_on(self):
        for id in self.device_ids:
            api.switch(id, 'on')

    def turn_off(self):
        for id in self.device_ids:
            api.switch(id, 'off')

    def toggle(self):
        is_on = self.is_some_on()

        if is_on:
            self.turn_off()
        else:
            self.turn_on()

    def toggle_individually(self):
        for id in self.device_ids:
            api.switch(id, 'toggle')

    # complex actions ------------------------------------------------------------ #

    def level(self, level: int):
        for id in self.device_ids:
            api.brightness(id, level)

    def color(self, color: str):
        from interfaces.api.config import get_cashed
        config = get_cashed()

        color_code = config.colors.get(color, color) if (config and color in config.colors) else color

        for id in self.device_ids:
            api.color(id, color_code)
