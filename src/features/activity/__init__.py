from features.activity.blink_timer import start_blink_timer, stop_blink_timer
from interfaces.api.config import get_cashed
from log import log
from interfaces.api.time_tracking import stop_tracking_activity, track_activity
from interfaces.actuators.led import get_lamp
import threading

_work_lamp = get_lamp('yellow')
_break_lamp = get_lamp('green')
_running = False
_break_thread = None


def is_activity_running() -> bool:
    return _running


def toggle_activity(track=True):
    if _running:
        stop_activity(track=track)
    else:
        start_activity(track=track)


def start_activity(track=True):
    global _running, _break_thread
    _running = True
    log("Started study timer")

    if _break_thread:
        _break_lamp.off()
        _break_thread.cancel()
        _break_thread = None

    _work_lamp.on()
    start_blink_timer()

    if track:
        track_activity()


def stop_activity(track=True):
    global _running
    _running = False
    log("Stopped timer")

    _work_lamp.off()
    stop_blink_timer()

    if track:
        stop_tracking_activity()

    start_break()


def start_break():
    global _break_thread
    config = get_cashed()

    if _break_thread is not None:
        _break_thread.cancel()

    if config and config.maxBreakMin:
        _break_lamp.on()
        _break_thread = threading.Timer(
            config.maxBreakMin * 60,
            lambda: _break_lamp.off(),
        )
        _break_thread.daemon = True
        _break_thread.start()
