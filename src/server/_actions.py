from features.activity import start_activity, stop_activity, is_activity_running
from features.menu import menu, rest_inputs
from flask import jsonify, Blueprint, request
from interfaces.actuators.led import get_lamp
from interfaces.api.time_tracking import track_activity, stop_tracking_activity
from interfaces.home import exec_preset_by_name, get_device, get_devices_string

bp = Blueprint('actions', __name__)


@bp.route('/start')
def start():
    alert_frequency = request.args.get('alert_frequency', default=None, type=float)

    start_activity(track=False, blink_frequency=alert_frequency)
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


@bp.route('/log-test')
def log_test():
    from interfaces.api.server_app import log_to_server
    log_to_server("Test log from /log-test endpoint")
    return "ok"


@bp.route('/is-running')
def is_running_route():
    return jsonify({"is_running": is_activity_running()})


@bp.route('/led/<string:name>')
def led(name: str):
    lamp = get_lamp(name)

    action = request.args.get('a', default='toggle').lower()

    if action == 'on':
        lamp.on()
    elif action == 'off':
        lamp.off()
    else:
        lamp.toggle()

    return "ok"


@bp.route('/dev/<string:name>/lvl/<int:level>')
def level(name: str, level: int):
    device = get_device(name)
    device.level(level)

    return "ok"


@bp.route('/dev/<string:name>/color/<string:color>')
def color(name: str, color: str):
    device = get_device(name)
    device.color(color)

    return "ok"


@bp.route('/dev/<string:name>/color/<int:color>')
def color_int(name: str, color: int):
    device = get_device(name)
    device.color(color)

    return "ok"


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

    return "ok"


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


@bp.route('/p/<string:name>')
def preset(name: str):
    state_mode = request.args.get('m', default=None)

    exec_preset_by_name(name, state_mode=state_mode)
    return "ok"
