import subprocess

from log import log
from transducers.actuators.led import get_lamp

_lamp = get_lamp('red')
_running = False


def start_activity(track=True):
    global _running
    _running = True
    log("Started study timer")

    _lamp.on()
    if track:
        subprocess.run(['zsh', '-i', '-c', 'tgs study'], stdin=subprocess.DEVNULL, timeout=5)


def stop_activity(track=True):
    global _running
    _running = False
    log("Stopped timer")

    _lamp.off()
    if track:
        subprocess.run(['zsh', '-i', '-c', 'toggl stop'], stdin=subprocess.DEVNULL, timeout=5)


def is_running() -> bool:
    return _running
