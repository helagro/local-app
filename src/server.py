from flask import Flask, jsonify
from sensors import read_temp, read_hum, read_light, read_uv, read_pressure
from cycle import get_away_for_eve, get_detached, get_before_wake

app = Flask(__name__)

# ---------------------- HELPER METHODS ---------------------- #


def all_readings():
    return {"temp": read_temp(), "hum": read_hum(), "light": read_light(), "uv": read_uv(), "pressure": read_pressure()}


# ------------------------- ALL ROUTE ------------------------ #


@app.route('/')
def all():
    return jsonify({
        "detached": get_detached(),
        "before_wake": get_before_wake(),
        "away_for_eve": get_away_for_eve(),
        "readings": all_readings()
    })


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


# ------------------------- CONTROL ------------------------- #


def start():
    app.run(debug=True, host='0.0.0.0', port=8004, use_reloader=False)
