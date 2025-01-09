from flask import Flask, jsonify
from sensors import read_temp, read_hum, read_light, read_uv, read_pressure, read_voc, get_last_voc
from cycle import get_away_for_eve, get_detached, get_before_wake, get_reduce_temp_time, track_time_independents
from outward import REDUCE_HEAT_THRESHOLD, get_config

app = Flask(__name__)

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


@app.route('/')
def all():
    return jsonify({
        "version": "1.0",
        "away_for_eve": get_away_for_eve(),
        "config": get_config(""),
        "routines": {
            "before_wake": get_before_wake(),
            "reduce_temp_time": get_reduce_temp_time(),
            "detached": get_detached(),
        },
        "readings": all_readings()
    })


@app.route('/do_track')
def do_track():
    track_time_independents()
    return "Tracked readings"


# -------------------------- SENSOR ROUTES -------------------------- #


@app.route('/readings')
def readings():
    return jsonify(all_readings())


@app.route('/temp')
def temp():
    return f"{read_temp()}\n"


@app.route('/hum')
def hum():
    return f"{read_hum()}\n"


@app.route('/light')
def light():
    return f"{read_light()}\n"


@app.route('/uv')
def uv():
    return f"{read_uv()}\n"


@app.route('/pressure')
def pressure():
    return f"{read_pressure()}\n"


@app.route('/voc')
def voc():
    return f"{read_voc()}\n"


# ------------------------- CONTROL ------------------------- #


def start():
    app.run(debug=True, host='0.0.0.0', port=8004, use_reloader=False)
