from features.activity import start_activity, stop_activity, is_activity_running
from features.menu import menu, rest_inputs
from flask import jsonify, Blueprint
from interfaces.api.time_tracking import track_activity, stop_tracking_activity
from interfaces.actuators.tradfri import get_device, get_devices_string

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


@bp.route('/t/<path:rest>')
def toggle_group(rest: str):
    names = rest.split('/')

    results = []
    for name in names:
        try:
            device = get_device(name)
            device.toggle()
            results.append({"name": name, "ok": True})
        except ValueError as e:
            results.append({
                "name": name,
                "ok": False,
                "error": str(e),
                "available_devices": get_devices_string(),
            })

    return jsonify({
        "is_running": is_activity_running(),
        "results": results,
    })


@bp.route('/c/<path:rest>')
def command(rest: str):
    commands = rest.split('/')

    outputs = []
    for cmd in commands:
        out = menu(cmd, rest_inputs)
        outputs.append({"command": cmd, "output": out})

    return jsonify({
        "is_running": is_activity_running(),
        "results": outputs,
    })
