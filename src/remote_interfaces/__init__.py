import os
import sys

from remote_interfaces.config import get_config
from remote_interfaces.server_app import get_routine, log_to_server

script_dir = os.path.expanduser("~/.dotfiles/scripts/lang/python")
sys.path.append(script_dir)
import exist

# -------------------------- FUNCTIONS ------------------------- #


def is_away() -> bool:
    if get_config('doTrack') == False: return True

    try:
        away_dict = exist.values('away', 1, None)
        return list(away_dict.values())[0] == 1
    except Exception as e:
        log_to_server(f"/is_away - failed to check if away: {e}")
        return False


# -------------------------- TESTING ENTRY POINT ------------------------- #

if __name__ == "__main__":
    print(get_routine("detach"))
    print(get_config("reduceHeatThreshold"))
