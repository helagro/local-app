import os
from flask import send_from_directory, abort, Blueprint, redirect, url_for, jsonify
from random import choice
from log import log

HOSTED_FOLDER_PATH = '/media/pi/16_GB_USB/public'

bp = Blueprint('files', __name__)


@bp.route('/sync')
def sync_files():
    from features.sync import sync_folders
    sync_folders()
    return jsonify({"status": "Sync initiated"})


@bp.route('/rand-path/<path:filename>')
def random_path(filename):
    return get_random_file_url(filename)


@bp.route('/rand/<path:filename>')
def random_file(filename):
    # ✅ Redirect to the main /<path:filename> route
    return redirect(url_for('files.files', filename=get_random_file_url(filename)))


@bp.route("/", defaults={"filename": ""})
@bp.route('/<path:filename>')
def files(filename):
    if os.path.isdir(HOSTED_FOLDER_PATH):
        full_path = os.path.realpath(os.path.join(HOSTED_FOLDER_PATH, filename))
        is_host_path = full_path == os.path.realpath(HOSTED_FOLDER_PATH)

        if not full_path.startswith(os.path.realpath(HOSTED_FOLDER_PATH) + os.sep) and not is_host_path:
            abort(403, description="Access denied")

        if os.path.isdir(full_path):
            contents = [f for f in os.listdir(full_path) if not f.startswith('.')]
            return jsonify({
                "path":
                filename,
                "rand":
                url_for('files.random_file', filename=filename, _external=True),
                "contents": [{
                    f: url_for('files.files', filename=os.path.join(filename, f), _external=True)
                } for f in contents]
            })

        return send_from_directory(HOSTED_FOLDER_PATH, filename)
    else:
        abort(404, description="Host folder not found")


# ================================== HELPERS ================================= #


def get_random_file_url(filename: str) -> str:
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
    files = [f for f in files if not f.startswith('.')]
    if not files:
        abort(404, description="No files found in directory")

    chosen_file = choice(files)
    file_path = os.path.realpath(os.path.join(full_path, chosen_file))

    log(f"Chose random file: {file_path}")

    # 🔒 Double-check chosen file is inside HOSTED_FOLDER_PATH
    if not file_path.startswith(base_path + os.sep):
        abort(403, description="Access denied")

    # Compute relative path (relative to HOSTED_FOLDER_PATH)
    return os.path.relpath(file_path, base_path)
