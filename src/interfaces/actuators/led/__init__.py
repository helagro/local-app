from dataclasses import dataclass
from typing_extensions import Literal
from log import log
import threading

try:
    from gpiozero import LED
except Exception as e:
    log(f"Error initialising LEDS: {e}")
    from interfaces.actuators.led._mocks import LED


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

    def blink(self):
        self.on()

        threading.Timer(0.1, self.off).start()


_lamps = {
    'blue': Lamp(17),
    'red': Lamp(27),
    'green': Lamp(24),
    'yellow': Lamp(23),
}


def get_lamp(pin: str) -> Lamp:
    return _lamps[pin]
