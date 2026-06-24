from features.activity import is_activity_blocking, start_activity, stop_activity, is_activity_running
from flask import jsonify, Blueprint, request
from interfaces.actuators.led import get_lamp
from interfaces.api.time_tracking import track_activity, stop_tracking_activity

bp = Blueprint('activity', __name__)


@bp.route('/start')
def start():
    should_block = request.args.get('blocking', default=True, type=int) != 0
    alert_frequency = request.args.get('alert_frequency', default=None, type=float)

    start_activity(track=False, blink_frequency=alert_frequency, blocking=should_block)
    return "ok"


@bp.route('/stop')
def stop():
    stop_activity(track=False)
    return "ok"


@bp.route('/toggle')
def toggle():
    if is_activity_running():
        stop_tracking_activity()
    else:
        track_activity()

    return "ok"


@bp.route('/is-running')
def is_running_route():
    return jsonify({"is_running": is_activity_running()})


@bp.route('/is-blocking')
def is_blocking_route():
    return jsonify({"is_blocking": is_activity_blocking()})
