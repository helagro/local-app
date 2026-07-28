from flask import Blueprint, request
from interfaces.home import exec_preset_by_name, get_device, get_devices_string, get_last_preset_name

bp = Blueprint('actions', __name__)


@bp.route('/<string:name>')
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


@bp.route('/<string:name>/lvl/<int:level>')
def level(name: str, level: int):
    device = get_device(name)
    device.level(level)

    return "ok"


@bp.route('/<string:name>/state')
def state(name: str):
    device = get_device(name)
    return device.is_some_on()


# =================================== COLOR ================================== #


@bp.route('/<string:name>/color/<string:color>')
def color(name: str, color: str):
    device = get_device(name)
    device.color(color)

    return "ok"


@bp.route('/<string:name>/color/<int:color>')
def color_int(name: str, color: int):
    device = get_device(name)
    device.color(color)

    return "ok"
