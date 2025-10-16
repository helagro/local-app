from log import log


class LED:

    def __init__(self, pin: int):
        self.pin = pin

    def on(self):
        log(f"LED on pin {self.pin} ON")

    def off(self):
        log(f"LED on pin {self.pin} OFF")
