from flask import Blueprint, jsonify
from tradfri import get_devices, Action

bp = Blueprint('iot', __name__)

# -------------------------- GET-ENDPOINTS ------------------------- #


@bp.route('/devices', methods=['GET'])
def get_ikea_devices():
    return jsonify(get_devices())


@bp.route('/api/actions', methods=['GET'])
def get_actions():
    return jsonify({action.name: action.value for action in Action})
