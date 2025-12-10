import time
from log import log
from interfaces.api.config import get_cashed
from interfaces.actuators.tradfri import get_device
import threading

_should_run = False
_thread = None

# ================================== PUBLIC ================================== #


def start_blink_timer():
    log("Starting blink timer routine.")
    global _should_run, _thread
    _should_run = True

    if not _thread or not _thread.is_alive():
        _thread = threading.Thread(target=_blink_timer, daemon=True)
        _thread.start()


def stop_blink_timer():
    log("Stopping blink timer routine.")
    global _should_run
    _should_run = False


# ================================== PRIVATE ================================= #


def _blink_timer():
    config = get_cashed()
    if not config:
        log("No config found, skipping blink timer routine.")
        return

    while _should_run:
        alertFrequency = config.alertFrequency
        time.sleep(alertFrequency * 60)

        _run_scheduled_alert(config)


def _run_scheduled_alert(config):
    if not _should_run:
        return

    do_blink_timer = config.doBlinkTimer
    if not do_blink_timer:
        log(f"Blink timer is {do_blink_timer} in config.")
        return

    pause_delay = config.pauseDelay
    _alert(pause_delay)


def _alert(duration):
    config = get_cashed()
    if not config:
        log("No config found, skipping alert.")
        return

    alert_lamp = config.alertLamp
    if not alert_lamp:
        log("No alert lamp configured, skipping alert.")
        return

    get_device(alert_lamp).toggle()

    time.sleep(duration)
    get_device(alert_lamp).toggle()
