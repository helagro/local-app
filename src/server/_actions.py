from actions import menu, rest_inputs
from flask import jsonify, Blueprint
from remote_interfaces.activity import start_activity, stop_activity, is_running

bp = Blueprint('actions', __name__)


@bp.route('/start')
def start():
    start_activity(track=False)
    return jsonify({"is_running": is_running()})


@bp.route('/stop')
def stop():
    stop_activity(track=False)
    return jsonify({"is_running": is_running()})


@bp.route('/cmd/<string:command>')
def command(command: str):
    menu(command, rest_inputs)

    return jsonify({"command": command, "is_running": is_running()})
