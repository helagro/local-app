from interfaces.api.config import sync_config
from interfaces.api.server_app import HUM, LIGHT_BEFORE_WAKE, LIGHT_DAWN, LIGHT_EVE, LIGHT_NIGHT, PRESSURE, TEMP_EARLY, TEMP_NIGHT, a, should_track, log_to_server
import schedule
import time
from interfaces.api import *
from features.routines.routine import Routine, SyncedRoutine
from interfaces.transducers.sensors import *
from threading import Thread
from typing import cast
from log import log

# ------------------------- VARIABLES ------------------------ #

MAX_NIGHT_LIGHT = 0.2

_voc: float | None = None
_away_when_detached = should_track()

# ------------------------- ROUTINES ------------------------ #


def _on_night() -> None:
    if _away_when_detached: return

    temp = read_temp()
    if temp is not None:
        a(f"{TEMP_NIGHT} {temp} s #u")

    light = read_light(max=MAX_NIGHT_LIGHT)
    if light is not None:
        a(f"{LIGHT_NIGHT} {light} s #u", )


def _on_before_wake() -> None:
    if _away_when_detached: return

    temp = read_temp()
    if temp is not None:
        a(f"{TEMP_EARLY} {read_temp()} s #u")

    callback = lambda x: a(f"{LIGHT_BEFORE_WAKE} {x} s #u")
    Thread(target=read_avg_light, args=(callback, ), kwargs={'max': MAX_NIGHT_LIGHT}).start()


def _on_morning() -> None:
    if _away_when_detached: return

    read_avg_light(lambda x: a(f"{LIGHT_DAWN} {x} s #u"))


def _on_do_reduce_temp() -> None:
    if should_track(): return

    temp = read_temp()
    if temp is None: return

    config = get_cashed()
    if not config: return

    temp_treshold: float = config.reduceHeatThreshold
    is_summer_weather: float = config.isSummerWeather

    if not is_summer_weather and cast(float, temp) > cast(float, temp_treshold):
        a(f"reduce temperature - current: {temp} #b")


def _on_eve() -> None:
    _update_routines()
    if _away_when_detached: return

    config = get_cashed()
    if not config: return

    for task in config.tasks["eve"]:
        a(task)


def _on_latest_dinner() -> None:
    config = get_cashed()
    if _away_when_detached or not config: return

    for task in config.tasks["latestDinner"]:
        a(task)


def _on_detached() -> None:
    global _away_when_detached, _voc
    _away_when_detached = should_track()

    if _away_when_detached:
        log(f"Was away for {_on_detached.__name__}")
        _voc = None
        return

    # Called here to maxmize chance that "away" has been tracked
    track_time_independents()

    callback = lambda x: a(f"{LIGHT_EVE} {x} s  #u")
    Thread(target=read_avg_light, args=(callback, )).start()


# -------------------------- OTHER ------------------------- #


def track_time_independents():
    hum = read_hum()
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
    "detached": SyncedRoutine(name="detached", default_time="21:00", function=_on_detached),
}

# -------------------------- GETTERS ------------------------- #


def get_away_for_eve() -> bool:
    return _away_when_detached


def get_routines() -> dict[str, Routine]:
    return _routines


def get_routine_strings() -> list[str]:
    return [repr(routine) for routine in _routines.values()]


# --------------------------- START -------------------------- #


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(20)
