from flask import jsonify, Blueprint
from activity import start_activity, stop_activity, is_running

bp = Blueprint('activity', __name__)


@bp.route('/start')
def start():
    start_activity(track=False)
    return jsonify({"is_running": is_running()})


@bp.route('/stop')
def stop():
    stop_activity(track=False)
    return jsonify({"is_running": is_running()})
