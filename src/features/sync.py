import os
import shutil
from log import log
from server._files import HOSTED_FOLDER_PATH

# Source and destination
folder_a = "/media/pi/tb-hdd/public"


def sync_folders():
    # Make sure destination exists
    os.makedirs(HOSTED_FOLDER_PATH, exist_ok=True)

    # 1️⃣ Build sets of filenames (ignore directories if you want)
    files_a = set(f for f in _get_all_files(folder_a) if os.path.isfile(os.path.join(folder_a, f)))
    files_b = set(f for f in _get_all_files(HOSTED_FOLDER_PATH) if os.path.isfile(os.path.join(HOSTED_FOLDER_PATH, f)))

    # 2️⃣ Copy missing files from A → B
    for f in files_a - files_b:
        src = os.path.join(folder_a, f)
        dst = os.path.join(HOSTED_FOLDER_PATH, f)
        shutil.copy2(src, dst)
        log(f"/sync copied: {f}")

    # 3️⃣ Optionally delete files in B that are not in A
    for f in files_b - files_a:
        dst = os.path.join(HOSTED_FOLDER_PATH, f)
        os.remove(dst)
        log(f"/sync deleted: {f}")

    log("Sync complete.")


def _get_all_files(folder):
    file_list = set()
    for root, dirs, files in os.walk(folder):
        for f in files:
            # store relative path so it can be mirrored
            rel_path = os.path.relpath(os.path.join(root, f), folder)
            file_list.add(rel_path)
    return file_list
