from transducers.actuators.led import get_lamp
import time
from evdev import InputDevice, categorize, ecodes, list_devices

MOUSE_PATH = '/dev/input/by-id/usb-MOSART_Semi._2.4G_Wireless_Mouse-event-mouse'


def menu(button_name):
    """Handle a button press"""
    if button_name == 'BTN_LEFT':
        print("Left button action")
        get_lamp('red').toggle()
    elif button_name == 'BTN_RIGHT':
        print("Right button action")
        get_lamp('blue').toggle()
    elif button_name == 'BTN_MIDDLE':
        print("Middle button action")
    elif button_name == 'BTN_EXTRA':
        print("Extra button action")
    elif button_name == 'BTN_SIDE':
        print("Side button action")
    else:
        print(f"Unhandled button: {button_name}")


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
                if event.type == ecodes.EV_KEY and event.keystate == event.key_down:
                    key_event = categorize(event)
                    if key_event.keycode in ('BTN_LEFT', 'BTN_RIGHT', 'BTN_MIDDLE', 'BTN_EXTRA', 'BTN_SIDE'):
                        menu(key_event.keycode)

        except OSError:
            # Device disconnected
            print("Mouse unplugged. Waiting for replug...")
            mouse.close()
            mouse = wait_for_device(MOUSE_PATH)
        except KeyboardInterrupt:
            print("Exiting...")
            mouse.close()
            break
