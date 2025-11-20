import time
from log import log
from remote_interfaces.config import get_cashed
from transducers.actuators.tradfri import get_device
import threading

_should_run = False

# ================================== PUBLIC ================================== #


def start_blink_timer():
    log("Starting blink timer routine.")
    global _should_run
    _should_run = True

    threading.Thread(target=blink_timer(), daemon=True).start()


def stop_blink_timer():
    log("Stopping blink timer routine.")
    global _should_run
    _should_run = False


# ================================== PRIVATE ================================= #


def blink_timer():
    config = get_cashed()
    if not config:
        log("No config found, skipping blink timer routine.")
        return

    while _should_run:
        alertFrequency = config.alertFrequency
        time.sleep(alertFrequency * 60)

        _alert(config)


def _alert(config):
    if not _should_run:
        return

    do_blink_timer = config.doBlinkTimer
    if not do_blink_timer:
        log(f"Blink timer is {do_blink_timer} in config.")
        return

    pause_delay = config.pauseDelay
    get_device('read').toggle()

    time.sleep(pause_delay)
    get_device('read').toggle()
