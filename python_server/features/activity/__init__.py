from datetime import datetime
from features.activity._blink_timer import start_blink_timer, stop_blink_timer
from interfaces.api.config import get_cached
from log import log
from interfaces.api.time_tracking import stop_tracking_activity, track_activity
from interfaces.actuators.led import get_lamp
import threading

_work_lamp = get_lamp('yellow')
_break_lamp = get_lamp('green')

_running = False
_blocking = False
_break_thread = None


def is_activity_running() -> bool:
    return _running


def is_activity_blocking() -> bool:
    return _blocking


def toggle_activity(track=True):
    if _running:
        stop_activity(track=track)
    else:
        start_activity(track=track)


def start_activity(track=True, blink_frequency=None, blocking=True):
    global _running, _break_thread, _blocking
    _blocking = blocking
    _running = True
    log("Started study timer. Blocking: %s Frequency: %s" % (blocking, blink_frequency))

    if _break_thread:
        _break_lamp.off()
        _break_thread.cancel()
        _break_thread = None

    _work_lamp.on()
    if not blocking:
        _break_lamp.on()

    start_blink_timer(blink_frequency)

    if track:
        track_activity()


def stop_activity(track=True):
    global _running, _blocking
    _running = False
    _blocking = False
    log("Stopped timer")

    _work_lamp.off()
    _break_lamp.off()
    stop_blink_timer()

    if track:
        stop_tracking_activity()

    start_break()


def start_break():
    global _break_thread
    config = get_cached()

    if _break_thread is not None:
        _break_thread.cancel()

    cur_hour = datetime.now().hour
    if config and config.maxBreakMin and cur_hour >= 8 and cur_hour < 20:
        _break_lamp.on()
        _break_thread = threading.Timer(
            config.maxBreakMin * 60,
            lambda: _break_lamp.off(),
        )
        _break_thread.daemon = True
        _break_thread.start()
