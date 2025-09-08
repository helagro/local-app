import server
import threading
from routines import run_schedule, get_away_for_eve
from log import log

ran_once = False

if __name__ == '__main__':

    if not ran_once:
        ran_once = True

        log("Started")
        print(f"  Is away: {get_away_for_eve()}")
        print("")

        threading.Thread(target=run_schedule, daemon=True).start()

    server.start()
