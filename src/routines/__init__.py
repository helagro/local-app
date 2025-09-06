from remote_interfaces.config import IS_SUMMER_WEATHER, REDUCE_HEAT_THRESHOLD
from remote_interfaces.server_app import HUM, LIGHT_BEFORE_WAKE, LIGHT_DAWN, LIGHT_EVE, LIGHT_NIGHT, PRESSURE, TEMP_EARLY, TEMP_NIGHT, a
import schedule
import time
from remote_interfaces import *
from routines.routine import Routine, SyncedRoutine
from sensors import *
from threading import Thread
from typing import cast

# ------------------------- CONSTANTS ------------------------ #

MAX_NIGHT_LIGHT = 0.2

_voc: float | None = None
_away_when_detached = is_away()

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
    if is_away(): return

    temp = read_temp()
    config: dict | None = cast(dict | None, get_config(''))

    if config is None:
        log("/_on_do_reduce_temp: config is None")
        return

    temp_treshold: None | float = cast(None | float, config.get(REDUCE_HEAT_THRESHOLD, None))
    is_summer_weather: None | float = cast(None | float, config.get(IS_SUMMER_WEATHER, True))

    values_does_exist = temp is not None and temp_treshold is not None and is_summer_weather is not None
    if values_does_exist and not is_summer_weather and cast(float, temp) > cast(float, temp_treshold):
        a(f"reduce temperature - current: {temp} #b")


def _on_eve() -> None:
    _update_routines()
    if _away_when_detached: return

    a('#b prepare for night')
    a('#b prepare for imorgon')


def _on_detached() -> None:
    global _away_when_detached, _voc
    _away_when_detached = is_away()

    if _away_when_detached:
        print(f"Was away for {_on_detached.__name__}")
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
    if (get_config('kill') == True):
        print("Killing local app from config")
        exit(0)

    for routine in _routines.values():
        routine.update()


# --------------------------- SCHEDULES -------------------------- #

_routines: dict[str, Routine] = {
    "night": Routine(name="night", time="02:00", function=_on_night),
    "before_wake": SyncedRoutine(name="before_wake", default_time="07:00", function=_on_before_wake),
    "after_wake": SyncedRoutine(name="after_wake", default_time="09:00", function=_on_morning),
    "reduce_temp": SyncedRoutine(name="reduce_temp", default_time="16:00", function=_on_do_reduce_temp),
    "update": Routine(name="update", time="18:00", function=_on_eve),
    "detached": SyncedRoutine(name="detached", default_time="21:00", function=_on_detached),
}

# -------------------------- GETTERS ------------------------- #


def get_away_for_eve() -> bool:
    return _away_when_detached


def get_routines() -> dict[str, Routine]:
    return _routines


# --------------------------- START -------------------------- #


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(20)
