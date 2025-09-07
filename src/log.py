_logs = []


def log(message):
    _logs.append(message)
    print(f"LOG: {message}")


def get_logs():
    return _logs
