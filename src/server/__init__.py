from flask import Flask, jsonify, request, send_from_directory, abort
from log import log
from interfaces.api.config import get_cashed
from datetime import date
from features.routines import get_away_for_eve, get_routine_strings
from ._readings import all_readings, bp as readings_bp
from ._actions import bp as actions_bp
from ._files import bp as files_bp
from os import _exit
from interfaces.api.config import sync_config

startup_date = date.today()

app = Flask(__name__)
app.register_blueprint(readings_bp, url_prefix='/sens')
app.register_blueprint(files_bp, url_prefix='/files')
app.register_blueprint(actions_bp)

# ================================== ROUTES ================================== #


@app.route('/')
def all():
    return jsonify({
        "version": "1.0",
        "startup_date": startup_date,
        "away_for_eve": get_away_for_eve(),
        "config": get_cashed(),
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


@app.route('/sync')
def sync():
    sync_config()
    return jsonify({"status": "Config synced"})


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


# ================================ MIDDLEWARE ================================ #


@app.after_request
def before_request_func(response):
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    log(f"REQ TO {request.path} FROM {ip}")
    return response


# ================================== CONTROL ================================= #


def start():
    app.run(debug=True, host='0.0.0.0', port=8004, use_reloader=False)
