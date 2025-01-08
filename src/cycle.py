import schedule
import time
from outward import *
from sensors import *
from threading import Thread

# ------------------------- CONSTANTS ------------------------ #

BEFORE_WAKE_ROUTINE_NAME = "before_wake"
AFTER_WAKE_ROUTINE_NAME = "after_wake"
REDUCE_TEMP_ROUTINE_NAME = "lower_heating"
DETACHED_ROUTINE_NAME = "detached"

MAX_NIGHT_LIGHT = 0.2

# ------------------------- VARIABLES ------------------------ #

_before_wake = get_routine(BEFORE_WAKE_ROUTINE_NAME) or "07:00"
_after_wake = get_routine(AFTER_WAKE_ROUTINE_NAME) or "9:00"
_reduce_temp = get_routine(REDUCE_TEMP_ROUTINE_NAME) or "16:00"
_detached = get_routine(DETACHED_ROUTINE_NAME) or "21:00"

_voc: int | None = None
_away_for_eve = is_away()

# -------------------------- GETTERS ------------------------- #


def get_detached() -> str:
    return _detached


def get_before_wake() -> str:
    return _before_wake


def get_reduce_temp_time() -> str:
    return _reduce_temp


def get_away_for_eve() -> bool:
    return _away_for_eve


# --------------------- UPDATING ROUTINE --------------------- #


def _on_do_update() -> None:
    global _before_wake, _detached, _after_wake, _reduce_temp
    _before_wake = _try_updating_routine(BEFORE_WAKE_ROUTINE_NAME, _before_wake, job=morning_schedule, fun=_on_morning)
    _after_wake = _try_updating_routine(AFTER_WAKE_ROUTINE_NAME, _after_wake, job=before_wake_schedule, fun=_on_before_wake)
    _reduce_temp = _try_updating_routine(REDUCE_TEMP_ROUTINE_NAME, _reduce_temp, job=reduce_temp_schedule, fun=_on_do_reduce_temp)
    _detached = _try_updating_routine(DETACHED_ROUTINE_NAME, _detached, job=eve_schedule, fun=_on_eve)


def _try_updating_routine(name: str, old_value: str, job: schedule.Job, fun: callable) -> str | None:
    new_value = get_routine(name)

    if new_value is None:
        log(f"/on_week: {name} is None")
        return old_value

    elif new_value != old_value:
        print(f"on_week: {name} updated to {new_value}")

        schedule.cancel_job(job)
        job = schedule.every().day.at(new_value).do(fun)

    return new_value


# ------------------------- ROUTINES ------------------------ #


def _on_voc() -> None:
    global _voc

    if is_away():
        _voc = None
        log("/on_voc: was away for on_voc")

    else:
        _voc = read_voc()

        if _voc is not None:
            a(f"voc {_voc} s #u")  # reason - is the air quality causing issues?


def _on_eve() -> None:
    global _away_for_eve
    _away_for_eve = is_away()

    if _away_for_eve:
        print("Was away for on_eve")
        return

    track_time_independents()

    callback = lambda x: a(f"{LIGHT_EVE} {x} s #u")
    Thread(target=read_avg_light, args=(callback, )).start()  # reason - are my lights too bright on evenings?


def _on_night() -> None:
    if _away_for_eve: return

    temp = read_temp()
    if temp is not None:
        a(f"{TEMP_NIGHT} {temp} s #u")  # reason - is it too warm to sleep?

    light = read_light(max=MAX_NIGHT_LIGHT)
    if light is not None:
        a(f"{LIGHT_NIGHT} {light} s #u", )  # reason - is it too bright to sleep?


def _on_before_wake() -> None:
    if _away_for_eve: return

    temp = read_temp()
    if temp is not None:
        a(f"{TEMP_EARLY} {read_temp()} s #u")  # reason - do I wake up because it's too warm?

    # reason - do I wake up because it's too bright?
    callback = lambda x: a(f"{LIGHT_BEFORE_WAKE} {x} s #u")
    Thread(target=read_avg_light, args=(callback, ), kwargs={'max': MAX_NIGHT_LIGHT}).start()


def _on_morning() -> None:
    if _away_for_eve: return

    read_avg_light(lambda x: a(f"{LIGHT_DAWN} {x} s #u"))  # reason - is it bright enough to wake up?


def _on_do_reduce_temp() -> None:
    if is_away(): return

    temp = read_temp()
    temp_treshold = get_config("reduceHeatThreshold")
    print(f"reduce_temp HAS temp: {temp}, temp_treshold: {temp_treshold}")

    if temp is not None and temp > temp_treshold:
        a(f"#b reduce temperature - current: {temp}")


# -------------------------- OTHER ------------------------- #


def track_time_independents():
    hum = read_hum()
    if hum is not None:
        a(f"{HUM} {hum / 100} s #u")  # reason - is dry air causing issues?

    pressure = read_pressure()
    if pressure is not None:
        a(f"{PRESSURE} {round(pressure)} s #u")  # reason - does the weather give me headaches?


# --------------------------- SCHEDULES -------------------------- #

voc_schedule = schedule.every(4).days.at("17:00").do(_on_voc)
update_schedule = schedule.every(2).days.at("14:00").do(_on_do_update)

reduce_temp_schedule = schedule.every().day.at(_reduce_temp).do(_on_do_reduce_temp)
eve_schedule = schedule.every().day.at(_detached).do(_on_eve)
night_schedule = schedule.every().day.at("01:00").do(_on_night)
before_wake_schedule = schedule.every().day.at(_before_wake).do(_on_before_wake)
morning_schedule = schedule.every().day.at(_after_wake).do(_on_morning)

# --------------------------- START -------------------------- #


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(20)
