from features.sync import sync_folders
from interfaces.actuators.led import get_lamp
from interfaces.actuators.tradfri import get_device
from interfaces.api.config import sync_config
from interfaces.api.server_app import HUM, LIGHT_BEFORE_WAKE, LIGHT_DAWN, LIGHT_EVE, LIGHT_NIGHT, PRESSURE, TEMP_EARLY, TEMP_NIGHT, a, should_skip_tracking, log_to_server
import schedule
import time
from interfaces.api import *
from features.routines.routine import Routine, SyncedRoutine
from interfaces.sensors import *
from threading import Thread
from typing import cast
from log import log

# ------------------------- VARIABLES ------------------------ #

MAX_NIGHT_LIGHT = 0.2

_voc: float | None = None
_no_track_for_detach = should_skip_tracking()
_eve_led = get_lamp('red')

# ------------------------- ROUTINES ------------------------ #


def _on_night() -> None:
    if _no_track_for_detach: return

    temp = read_temp(from_hat=False)
    if temp is not None:
        a(f"{TEMP_NIGHT} {temp} s #u")

    light = read_light(max=MAX_NIGHT_LIGHT)
    if light is not None:
        a(f"{LIGHT_NIGHT} {light} s #u", )


def _on_before_wake() -> None:
    if _no_track_for_detach:
        get_device('all').turn_off()
        return

    temp = read_temp(from_hat=False)
    if temp is not None:
        a(f"{TEMP_EARLY} {temp} s #u")

    callback = lambda x: a(f"{LIGHT_BEFORE_WAKE} {x} s #u")
    Thread(target=read_avg_light, args=(callback, ), kwargs={'max': MAX_NIGHT_LIGHT}).start()


def _on_morning() -> None:
    if _no_track_for_detach: return

    read_avg_light(lambda x: a(f"{LIGHT_DAWN} {x} s #u"))


def _on_do_reduce_temp() -> None:
    if should_skip_tracking(): return

    temp = read_temp(from_hat=False)
    if temp is None: return

    config = get_cashed()
    if not config: return

    temp_treshold: float = config.reduceHeatThreshold
    is_summer_weather: float = config.isSummerWeather

    if not is_summer_weather and cast(float, temp) > cast(float, temp_treshold):
        a(f"reduce temperature - current: {temp} #b")


def _on_eve() -> None:
    _update_routines()
    if _no_track_for_detach: return

    config = get_cashed()
    if not config: return

    try:
        sync_folders()
    except Exception as e:
        log_to_server(f"Error during /sync-folders in eve routine: {e}")

    for task in config.tasks["eve"]:
        a(task)


def _on_latest_dinner() -> None:
    config = get_cashed()
    if _no_track_for_detach or not config: return

    for task in config.tasks["latestDinner"]:
        a(task)


def _on_full_detach() -> None:
    global _no_track_for_detach, _voc
    _no_track_for_detach = should_skip_tracking()

    if _no_track_for_detach:
        _voc = None
        return

    # Called here to maxmize chance that "away" has been tracked
    track_time_independents()
    _eve_led.on()

    callback = lambda x: a(f"{LIGHT_EVE} {x} s  #u")
    Thread(target=read_avg_light, args=(callback, )).start()


# -------------------------- OTHER ------------------------- #


def track_time_independents():
    hum = read_hum(from_hat=False)
    if hum is not None:
        a(f"{HUM} {hum / 100} s #u")

    pressure = read_pressure()
    if pressure is not None:
        a(f"{PRESSURE} {round(pressure)} s #u")

    # NOTE - Must be called last, interfers with other sensors
    _voc = read_voc()
    if _voc is not None:
        a(f"voc {_voc} s #u")

        if _voc > 100:
            a(f"#b open window - voc ({_voc} > 100)")


def _update_routines() -> None:
    config = sync_config()

    if (config and config.kill == True):
        log("Killing local app from config")
        exit(0)

    for routine in _routines.values():
        routine.update()


# --------------------------- SCHEDULES -------------------------- #

_routines: dict[str, Routine] = {
    "night": Routine(name="night", time="02:00", function=_on_night),
    "before_wake": SyncedRoutine(name="before_wake", default_time="07:00", function=_on_before_wake),
    "after_wake": SyncedRoutine(name="after_wake", default_time="09:00", function=_on_morning),
    "reduce_temp": SyncedRoutine(name="lower_heating", default_time="16:00", function=_on_do_reduce_temp),
    "eve": SyncedRoutine(name="on_eve", default_time="18:00", function=_on_eve),
    "latest_dinner": SyncedRoutine(name="latest_dinner", default_time="20:00", function=_on_latest_dinner),
    "full_detach": SyncedRoutine(name="full_detach", default_time="21:00", function=_on_full_detach),
    "bed_time": SyncedRoutine(name="bed_time", default_time="22:00", function=lambda: _eve_led.off()),
}

# -------------------------- GETTERS ------------------------- #


def get_away_for_eve() -> bool:
    return _no_track_for_detach


def get_routines() -> dict[str, Routine]:
    return _routines


def get_routine_strings() -> list[str]:
    return [repr(routine) for routine in _routines.values()]


# --------------------------- START -------------------------- #


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(20)
