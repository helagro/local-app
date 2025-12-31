from flask import jsonify, Blueprint
from interfaces.sensors import read_temp, read_hum, read_light, read_uv, read_pressure, read_voc, get_last_voc
from features.routines import track_time_independents

bp = Blueprint('readings', __name__)

# ---------------------- HELPER METHODS ---------------------- #


def all_readings():
    return {
        "temp": read_temp(from_hat=False),
        "hum": read_hum(from_hat=False),
        "light": read_light(),
        "uv": read_uv(),
        "pressure": read_pressure(),
        "voc": get_last_voc(),
        "from_hat": {
            "temp": read_temp(from_hat=True),
            "hum": read_hum(from_hat=True),
        }
    }


# ------------------------- UNCATEGORISED ROUTE ------------------------ #


@bp.route('/do_track')
def do_track():
    track_time_independents()
    return "Tracked readings"


# -------------------------- SENSOR ROUTES -------------------------- #


@bp.route('/')
def readings():
    return jsonify(all_readings())


@bp.route('/temp')
def temp():
    return f"{read_temp(from_hat=False)}\n"


@bp.route('/hum')
def hum():
    return f"{read_hum(from_hat=False)}\n"


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
