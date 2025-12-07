from features.activity import start_activity, stop_activity, is_activity_running
from features.menu import menu, rest_inputs
from flask import jsonify, Blueprint
from interfaces.api.time_tracking import track_activity, stop_tracking_activity
from interfaces.actuators.tradfri import get_device

bp = Blueprint('actions', __name__)


@bp.route('/start')
def start():
    start_activity(track=False)
    return jsonify({"is_running": is_activity_running()})


@bp.route('/stop')
def stop():
    stop_activity(track=False)
    return jsonify({"is_running": is_activity_running()})


@bp.route('/toggle')
def toggle():
    if is_activity_running():
        stop_tracking_activity()
    else:
        track_activity()

    return jsonify({"is_running": is_activity_running()})


@bp.route('/is-running')
def is_running_route():
    return jsonify({"is_running": is_activity_running()})


@bp.route('/dev/<string:name>/lvl/<int:level>')
def level(name: str, level: int):
    device = get_device(name)
    device.level(level)

    return jsonify({"is_running": is_activity_running()})


@bp.route('/c/<string:command>')
def command(command: str):
    output = menu(command, rest_inputs)

    return jsonify({"is_running": is_activity_running(), "output": output})
