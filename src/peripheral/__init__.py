from log import log
from actions import menu, button_inputs
import time
from evdev import InputDevice, categorize, ecodes
from transducers.actuators.led import get_lamp

MOUSE_PATH = '/dev/input/by-id/usb-MOSART_Semi._2.4G_Wireless_Mouse-event-mouse'
blue_led = get_lamp('blue')


def wait_for_device(path):
    """Wait until the device exists and is ready"""
    while True:

        try:
            device = InputDevice(path)
            print(f"Device found: {device}")
            return device
        except Exception as e:
            print(f"Waiting for device {path}... ({e})")

        time.sleep(60)


def handle_input():
    mouse = wait_for_device(MOUSE_PATH)

    while True:
        try:
            for event in mouse.read_loop():
                # Only handle key/button events
                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)
                    if key_event.keystate == key_event.key_down:
                        code = key_event.keycode if isinstance(key_event.keycode, str) else key_event.keycode[0]

                        menu(code, button_inputs)
                        blue_led.blink()

        except OSError:
            print("Mouse unplugged. Waiting for replug...")
            mouse.close()
            mouse = wait_for_device(MOUSE_PATH)
        except KeyboardInterrupt:
            print("Exiting...")
            mouse.close()
            return
