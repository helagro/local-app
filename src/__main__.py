import server
import threading
from cycle import run_schedule, get_away_for_eve

ran_once = False

if __name__ == '__main__':

    if not ran_once:
        ran_once = True

        print("Checks: ")
        print(f"  Is away: {get_away_for_eve()}")
        print("")

        threading.Thread(target=run_schedule, daemon=True).start()

    server.start()
