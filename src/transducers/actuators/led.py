from dataclasses import dataclass
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
        self.led.on()

    def off(self):
        self.is_on = False
        self.led.off()

    def toggle(self):
        if self.is_on:
            self.off()
        else:
            self.on()


_lamps = {
    17: Lamp(17),
}


def get_lamp(pin: int) -> Lamp:
    return _lamps[pin]
