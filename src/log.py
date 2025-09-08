from datetime import datetime

MAX_LOGS = 5000

_logs = []


def log(message):
    print(f"LOG: {message}")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _logs.append(f"{timestamp} - {message}")

    if len(_logs) > MAX_LOGS:
        del _logs[:500]


def get_logs():
    return _logs
