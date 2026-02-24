from datetime import datetime
import inspect
from pathlib import Path

MAX_LOGS = 5000
SRC_FOLDER = Path.cwd() / 'src'

_logs = []


def log(message):
    relative_path = get_file_path(depth=2)
    print(f"[{relative_path}] - {message}")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _logs.append(f"{timestamp} - [{relative_path}] - {message}")

    if len(_logs) > MAX_LOGS:
        del _logs[:500]


def get_file_path(depth=1):
    frame_info = inspect.stack()[depth]
    full_path = Path(frame_info.frame.f_code.co_filename).resolve()
    return full_path.relative_to(SRC_FOLDER)


def get_logs():
    return _logs
