from flask import Flask, jsonify
from sensors import read_temp
from reader import get_away_for_eve, get_detached

app = Flask(__name__)

# ---------------------- HELPER METHODS ---------------------- #


def all_readings():
    return {"temp": read_temp()}


# ------------------------- ALL ROUTE ------------------------ #


@app.route('/')
def all():
    return jsonify({
        "detached": get_detached(),
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


# ------------------------- CONTROL ------------------------- #


def start():
    app.run(debug=True, host='0.0.0.0', port=8004, use_reloader=False)
