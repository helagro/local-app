from features.activity.blink_timer import start_blink_timer, stop_blink_timer
from log import log
from interfaces.api.time_tracking import stop_tracking_activity, track_activity
from interfaces.actuators.led import get_lamp

_lamp = get_lamp('red')
_running = False


def is_activity_running() -> bool:
    return _running


def start_activity(track=True):
    global _running
    _running = True
    log("Started study timer")

    _lamp.on()
    start_blink_timer()

    if track:
        track_activity()


def stop_activity(track=True):
    global _running
    _running = False
    log("Stopped timer")

    _lamp.off()
    stop_blink_timer()

    if track:
        stop_tracking_activity()
