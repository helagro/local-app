from datetime import datetime
import time
from log import log
from interfaces.api.config import get_cashed
from interfaces.actuators.tradfri import get_device
import threading

_should_run = False
_thread = None

# ================================== PUBLIC ================================== #


def start_blink_timer(blink_frequency=None):
    log("Starting blink timer routine.")
    global _should_run, _thread
    _should_run = True

    if not _thread or not _thread.is_alive():
        _thread = threading.Thread(target=_blink_timer, args=(blink_frequency, ), daemon=True)
        _thread.start()


def stop_blink_timer():
    log("Stopping blink timer routine.")
    global _should_run
    _should_run = False


# ================================== PRIVATE ================================= #


def _blink_timer(alert_frequency=None):
    config = get_cashed()
    if not config:
        log("No config found, skipping blink timer routine.")
        return

    alert_frequency = alert_frequency or config.alertFrequency

    while _should_run:
        time.sleep(alert_frequency * 60)
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

    cur_hour = datetime.now().hour
    if cur_hour < 4:
        log("Current time is outside of alert hours, skipping alert.")
        return

    device = get_device(alert_lamp)
    if not device:
        log(f"Alert lamp {alert_lamp} not found, skipping alert.")
        return

    amt_on = device.amt_on()
    device.toggle_individually()
    start_time = time.time()

    # Note - Waits for lamps to react
    for _ in range(20):
        time.sleep(1)
        if amt_on != device.amt_on():
            break

    time.sleep(duration)
    end_time = time.time()
    device.toggle_individually()

    log(f"{duration} alert ran for {end_time - start_time:.2f} seconds")
