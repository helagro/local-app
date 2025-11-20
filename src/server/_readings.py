from flask import jsonify, Blueprint
from transducers.sensors import read_temp, read_hum, read_light, read_uv, read_pressure, read_voc, get_last_voc
from features.routines import track_time_independents

bp = Blueprint('readings', __name__)

# ---------------------- HELPER METHODS ---------------------- #


def all_readings():
    return {
        "temp": read_temp(),
        "hum": read_hum(),
        "light": read_light(),
        "uv": read_uv(),
        "pressure": read_pressure(),
        "voc": get_last_voc()
    }


# ------------------------- UNCATEGORISED ROUTE ------------------------ #


@bp.route('/do_track')
def do_track():
    track_time_independents()
    return "Tracked readings"


# -------------------------- SENSOR ROUTES -------------------------- #


@bp.route('/readings')
def readings():
    return jsonify(all_readings())


@bp.route('/temp')
def temp():
    return f"{read_temp()}\n"


@bp.route('/hum')
def hum():
    return f"{read_hum()}\n"


@bp.route('/light')
def light():
    return f"{read_light()}\n"


@bp.route('/uv')
def uv():
    return f"{read_uv()}\n"


@bp.route('/pressure')
def pressure():
    return f"{read_pressure()}\n"


@bp.route('/voc')
def voc():
    return f"{read_voc()}\n"
