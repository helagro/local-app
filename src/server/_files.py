import os
from flask import Flask, jsonify, request, send_from_directory, abort, Blueprint
from random import choice

HOSTED_FOLDER_PATH = ''

bp = Blueprint('files', __name__)


@bp.route('/rand/<path:filename>')
def random_file(filename):
    base_path = os.path.realpath(HOSTED_FOLDER_PATH)

    if not os.path.isdir(base_path):
        abort(404, description="Host folder not found")

    full_path = os.path.realpath(os.path.join(base_path, filename))

    # 🔒 Ensure requested folder is within HOSTED_FOLDER_PATH
    if not full_path.startswith(base_path + os.sep):
        abort(403, description="Access denied")

    if not os.path.isdir(full_path):
        abort(404, description="Folder not found")

    files = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]

    if not files:
        abort(404, description="No files found in directory")

    chosen_file = choice(files)
    file_path = os.path.realpath(os.path.join(full_path, chosen_file))

    # 🔒 Double-check chosen file is inside HOSTED_FOLDER_PATH
    if not file_path.startswith(base_path + os.sep):
        abort(403, description="Access denied")

    return send_from_directory(full_path, chosen_file)


@bp.route('/<path:filename>')
def files(filename):
    if os.path.isdir(HOSTED_FOLDER_PATH):
        return send_from_directory(HOSTED_FOLDER_PATH, filename)
    else:
        abort(404, description="Folder not found")
