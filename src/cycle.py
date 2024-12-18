import schedule
import time
from outward import *
from sensors import *
from threading import Thread

# ------------------------- CONSTANTS ------------------------ #

BEFORE_WAKE_ROUTINE_NAME = "before_wake"
DETACHED_ROUTINE_NAME = "detached"

MAX_NIGHT_LIGHT = 0.2

# ------------------------- VARIABLES ------------------------ #

_before_wake = get_routine(BEFORE_WAKE_ROUTINE_NAME) or "07:00"
_detached = get_routine(DETACHED_ROUTINE_NAME) or "21:00"

_voc: int | None = None
_away_for_eve = is_away()

# -------------------------- GETTERS ------------------------- #


def get_detached() -> str:
    return _detached


def get_before_wake() -> str:
    return _before_wake


def get_away_for_eve() -> bool:
    return _away_for_eve


# --------------------- UPDATING ROUTINE --------------------- #


def _on_week() -> None:
    global _before_wake, _detached
    _before_wake = _try_updating_routine(BEFORE_WAKE_ROUTINE_NAME, _before_wake, job=morning_schedule, fun=_on_morning)
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


def _on_eve() -> None:
    global _away_for_eve
    _away_for_eve = is_away()

    if _away_for_eve:
        print("Was away for on_eve")
        return

    track_time_independents()

    callback = lambda x: a(f"{LIGHT_EVE} {x} s")
    Thread(target=read_avg_light, args=(callback, )).start()  # reason - are my lights too bright on evenings?


def _on_night() -> None:
    if _away_for_eve: return

    temp = read_temp()
    if temp is not None:
        a(f"{TEMP_NIGHT} {temp} s")  # reason - is it too warm to sleep?

    light = read_light(max=MAX_NIGHT_LIGHT)
    if light is not None:
        a(f"{LIGHT_NIGHT} {light} s", )  # reason - is it too bright to sleep?


def _on_before_wake() -> None:
    if _away_for_eve: return

    temp = read_temp()
    if temp is not None:
        a(f"{TEMP_EARLY} {read_temp()} s")  # reason - do I wake up because it's too warm?

    # reason - do I wake up because it's too bright?
    callback = lambda x: a(f"{LIGHT_BEFORE_WAKE} {x} s")
    Thread(target=read_avg_light, args=(callback, ), kwargs={'max': MAX_NIGHT_LIGHT}).start()


def _on_morning() -> None:
    if _away_for_eve: return

    read_avg_light(lambda x: a(f"light_morning {x} s", do_exec=False))  # reason - is it bright enough to wake up?


# -------------------------- OTHER ------------------------- #


def track_time_independents():
    hum = read_hum()
    if hum is not None:
        a(f"{HUM} {hum / 100} s")  # reason - is dry air causing issues?

    pressure = read_pressure()
    if pressure is not None:
        a(f"{PRESSURE} {round(pressure)} s")  # reason - does the weather give me headaches?

    if _voc is not None:
        a(f"voc {_voc} s", do_exec=False)  # reason - is the air quality causing issues?


# --------------------------- SCHEDULES -------------------------- #

week_schedule = schedule.every(1).weeks.do(_on_week)
# voc_schedule = schedule.every(3).days.at("17:00").do(_on_voc)

eve_schedule = schedule.every().day.at(_detached).do(_on_eve)
night_schedule = schedule.every().day.at("01:00").do(_on_night)
before_wake_schedule = schedule.every().day.at(_before_wake).do(_on_before_wake)
morning_schedule = schedule.every().day.at("09:00").do(_on_morning)

# --------------------------- START -------------------------- #


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(20)
