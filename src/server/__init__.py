from flask import Flask, jsonify
from remote_interfaces import get_config
from datetime import date
from routines import get_away_for_eve, get_routines
from ._readings import all_readings, bp as readings_bp

startup_date = date.today()

app = Flask(__name__)
app.register_blueprint(readings_bp)

# ================================== ROUTES ================================== #


@app.route('/')
def all():
    return jsonify({
        "version": "1.0",
        "startup_date": startup_date,
        "away_for_eve": get_away_for_eve(),
        "config": get_config(),
        "routines": get_routines(),
        "readings": all_readings()
    })


# ================================== CONTROL ================================= #


def start():
    app.run(debug=True, host='0.0.0.0', port=8004, use_reloader=False)
