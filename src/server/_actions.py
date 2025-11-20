from typing import Literal, cast
from menu import menu, rest_inputs
from flask import jsonify, Blueprint
from remote_interfaces.activity import start_activity, stop_activity, is_running
from transducers.actuators.tradfri import get_device, get_devices

bp = Blueprint('actions', __name__)


@bp.route('/start')
def start():
    start_activity(track=False)
    return jsonify({"is_running": is_running()})


@bp.route('/stop')
def stop():
    stop_activity(track=False)
    return jsonify({"is_running": is_running()})


@bp.route('/toggle')
def toggle():
    if is_running():
        stop_activity()
    else:
        start_activity()

    return jsonify({"is_running": is_running()})


@bp.route('/is-running')
def is_running_route():
    return jsonify({"is_running": is_running()})


@bp.route('/dev/<string:name>/lvl/<int:level>')
def level(name: str, level: int):
    if name not in ['eve', 'day', 'read']:
        return jsonify({"error": "Invalid device name"}), 400

    device = get_device(name)
    device.level(level)

    return jsonify({"is_running": is_running(), "devices": [text for text in get_devices()]})


@bp.route('/c/<string:command>')
def command(command: str):
    menu(command, rest_inputs)

    return jsonify({"is_running": is_running(), "devices": [text for text in get_devices()]})
