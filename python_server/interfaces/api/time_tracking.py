import subprocess
from log import log


def track_activity():
    log("Starting activity tracking")
    subprocess.run(['zsh', '-i', '-c', 'tgs study'], stdin=subprocess.DEVNULL, timeout=5)


def stop_tracking_activity():
    log("Stopping activity tracking")
    subprocess.run(['zsh', '-i', '-c', 'toggl stop'], stdin=subprocess.DEVNULL, timeout=5)
