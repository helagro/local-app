from flask import Blueprint, request
from interfaces.actuators.led import get_lamp
from interfaces.home import exec_preset_by_name, get_device, get_devices_string, get_last_preset_name

bp = Blueprint('actions', __name__)


@bp.route('/log-test')
def log_test():
    from interfaces.api.server_app import log_to_server
    log_to_server("Test log from /log-test endpoint")
    return "ok"


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


@bp.route('/dev/<string:name>')
def device(name: str):
    device = get_device(name)

    action = request.args.get('a', default='toggle').lower()

    if action == 'on':
        device.turn_on()
    elif action == 'off':
        device.turn_off()
    else:
        device.toggle()

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


@bp.route('/last-preset')
def get_last_preset():
    preset = get_last_preset_name()
    if not preset:
        return 'NOT FOUND', 404

    return preset


@bp.route('/p/<string:name>')
def preset(name: str):
    state_mode = request.args.get('m', default=None)

    exec_preset_by_name(name, state_mode=state_mode)
    return "ok"
