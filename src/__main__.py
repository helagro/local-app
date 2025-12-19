import server
import threading
from features.routines import run_schedule
from log import log
import threading

ran_once = False

schedule_thread = None
server_thread = None

if __name__ == '__main__':

    if not ran_once:
        ran_once = True
        log("Started")

        schedule_thread = threading.Thread(target=run_schedule, daemon=True).start()
        server_thread = threading.Thread(target=server.start, daemon=True).start()

    threading.Event().wait()

    if schedule_thread:
        schedule_thread.join()
    if server_thread:
        server_thread.join()
