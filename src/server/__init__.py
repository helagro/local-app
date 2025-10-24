from flask import Flask, jsonify, request
from log import log
from remote_interfaces import get_config
from datetime import date
from routines import get_away_for_eve, get_routine_strings, get_routines
from ._readings import all_readings, bp as readings_bp
from ._actions import bp as activity_bp
from os import _exit

startup_date = date.today()

app = Flask(__name__)
app.register_blueprint(readings_bp)
app.register_blueprint(activity_bp)

# ================================== ROUTES ================================== #


@app.route('/')
def all():
    return jsonify({
        "version": "1.0",
        "startup_date": startup_date,
        "away_for_eve": get_away_for_eve(),
        "config": get_config(),
        "routines": get_routine_strings(),
        "readings": all_readings()
    })


@app.route('/logs')
def logs():
    from log import get_logs
    return jsonify({"logs": get_logs()})


@app.route('/quit')
def quit():
    log("Shutting down server...")
    _exit(0)


# ================================ MIDDLEWARE ================================ #


@app.after_request
def before_request_func(response):
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    log(f"REQ TO {request.path} FROM {ip}")
    return response


# ================================== CONTROL ================================= #


def start():
    app.run(debug=True, host='0.0.0.0', port=8004, use_reloader=False)
