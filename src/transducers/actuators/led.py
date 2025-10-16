from dataclasses import dataclass
from typing_extensions import Literal
from log import log

try:
    from gpiozero import LED
except Exception as e:
    log(f"Error initialising LEDS: {e}")
    from transducers.actuators._mocks import LED


@dataclass
class Lamp:
    pin: int
    is_on: bool = False

    def __post_init__(self):
        self.led = LED(self.pin)

    def on(self):
        self.is_on = True

        try:
            self.led.on()
        except Exception as e:
            log(f"Error turning on LED on pin {self.pin}: {e}")

    def off(self):
        self.is_on = False

        try:
            self.led.off()
        except Exception as e:
            log(f"Error turning off LED on pin {self.pin}: {e}")

    def toggle(self):
        if self.is_on:
            self.off()
        else:
            self.on()


_lamps = {
    'blue': Lamp(17),
    'red': Lamp(27),
}


def get_lamp(pin: Literal['blue', 'red']) -> Lamp:
    return _lamps[pin]
