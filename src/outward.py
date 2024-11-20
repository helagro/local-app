import subprocess
import os
import requests
from datetime import datetime

ROUTINE_ENDPOINT = os.getenv("ROUTINE_ENDPOINT")
if not ROUTINE_ENDPOINT:
    raise ValueError("SECRET_ENDPOINT environment variable is not set")


def is_away():
    result = subprocess.run(
        ["zsh", "-i", "-c", "source ~/.zshrc && tl is/away | st cnt"],
        capture_output=True,
        text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("Return Code:", result.returncode)


def a(content: str):
    result = subprocess.run(["zsh", "-c", f"source ~/.zshrc && a {content}"],
                            capture_output=True,
                            text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("Return Code:", result.returncode)


def get_routine(name: str) -> datetime:
    response = get_routine_str(name)
    time_str = response.replace('.', ':')
    return datetime.strptime(time_str, "%H:%M:%S")


def get_routine_str(name: str) -> str:
    try:
        response = requests.get(ROUTINE_ENDPOINT, params={"q": name})
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch routine: {e}")
