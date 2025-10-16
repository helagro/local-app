from transducers.actuators.led import get_lamp
from transducers.actuators.tradfri import get_device
import time
from evdev import InputDevice, categorize, ecodes
import subprocess

MOUSE_PATH = '/dev/input/by-id/usb-MOSART_Semi._2.4G_Wireless_Mouse-event-mouse'


def menu(button_name):
    """Handle a button press"""
    if button_name == 'BTN_LEFT':
        print("Left button action")
        get_device('eve').toggle()

    elif button_name == 'BTN_RIGHT':
        print("Right button action")
        get_device('day').toggle()

    elif button_name == 'BTN_MIDDLE':
        print("Middle button action")
        get_device('read').toggle()

    elif button_name == 'BTN_EXTRA':
        print("Extra button action")
        get_lamp('red').on()
        subprocess.run(['zsh', '-i', '-c', 'tgs study'], stdin=subprocess.DEVNULL, timeout=5)

    elif button_name == 'BTN_SIDE':
        print("Side button action")
        get_lamp('red').off()
        subprocess.run(['zsh', '-i', '-c', 'toggl stop'], stdin=subprocess.DEVNULL, timeout=5)

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
                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)
                    if key_event.keystate == key_event.key_down:
                        code = key_event.keycode if isinstance(key_event.keycode, str) else key_event.keycode[0]

                        menu(code)

        except OSError:
            # Device disconnected
            print("Mouse unplugged. Waiting for replug...")
            mouse.close()
            mouse = wait_for_device(MOUSE_PATH)
        except KeyboardInterrupt:
            print("Exiting...")
            mouse.close()
            break
