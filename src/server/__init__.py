from flask import Flask, jsonify
from outward import get_config
from datetime import date
from cycle import get_away_for_eve, get_detached, get_before_wake, get_reduce_temp_time
from .readings import all_readings, bp as readings_bp

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
        "config": get_config(""),
        "routines": {
            "before_wake": get_before_wake(),
            "reduce_temp_time": get_reduce_temp_time(),
            "detached": get_detached(),
        },
        "readings": all_readings()
    })


# ================================== CONTROL ================================= #


def start():
    app.run(debug=True, host='0.0.0.0', port=8004, use_reloader=False)
