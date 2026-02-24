from datetime import datetime
import inspect
import os

MAX_LOGS = 5000

_logs = []


def log(message):
    frame = inspect.stack()[1]
    filename = os.path.basename(frame.filename)
    print(f"[{filename}] - {message}")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _logs.append(f"{timestamp} - [{filename}] - {message}")

    if len(_logs) > MAX_LOGS:
        del _logs[:500]


def get_logs():
    return _logs
