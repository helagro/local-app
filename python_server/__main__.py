from interfaces.actuators.led import get_lamp
from interfaces.api.config import sync_config
from interfaces import socket_server
import server
import threading
from features.routines import run_schedule
from log import log
import threading

ran_once = False

schedule_thread = None
server_thread = None
socket_thread = None


def start_led_off():
    led = get_lamp('blue')
    led.off()


if __name__ == '__main__':

    if not ran_once:
        ran_once = True
        log("Started")
        get_lamp('blue').on()

        sync_config()

        schedule_thread = threading.Thread(target=run_schedule, daemon=True).start()
        server_thread = threading.Thread(target=server.start, daemon=True).start()
        socket_thread = threading.Thread(target=socket_server.start_socket_server, daemon=True).start()
        threading.Timer(5, start_led_off).start()

    threading.Event().wait()

    if schedule_thread:
        schedule_thread.join()
    if server_thread:
        server_thread.join()
    if socket_thread:
        socket_thread.join()
