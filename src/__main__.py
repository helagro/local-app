import server
import threading
from routines import run_schedule, get_away_for_eve
from log import log
from peripheral import handle_input

ran_once = False

if __name__ == '__main__':

    if not ran_once:
        ran_once = True
        log("Started")

        threading.Thread(target=run_schedule, daemon=True).start()
        threading.Thread(target=server.start, daemon=True).start()

    handle_input()
