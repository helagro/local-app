import schedule
import time
from outward import is_away, a, get_routine, log
from sensors import read_voc, read_temp, read_hum, read_light, read_uv, read_pressure, read_avg_light

# ------------------------- CONSTANTS ------------------------ #

BEFORE_WAKE_ROUTINE_NAME = "before_wake"
DETACHED_ROUTINE_NAME = "detached"

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


def get_voc() -> int | None:
    return _voc


# --------------------- UPDATING ROUTINE --------------------- #


def _on_week() -> None:
    global _before_wake, _detached
    _before_wake = _try_updating_routine(BEFORE_WAKE_ROUTINE_NAME, _before_wake, morning_schedule, _on_morning)
    _detached = _try_updating_routine(DETACHED_ROUTINE_NAME, _detached, eve_schedule, _on_eve)


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
        a("was away for on_voc")

    else:
        _voc = read_voc()


def _on_eve() -> None:
    global _away_for_eve
    _away_for_eve = is_away()

    if _away_for_eve:
        print("Was away for on_eve")
        return

    a(f"voc {_voc} s")  # reason - is the air quality causing issues?
    a(f"hum {read_hum()} s")  # reason - is dry air causing issues?
    a(f"pressure {read_pressure()} s")  # reason - does the weather give me headaches?
    a(f"light_eve {read_avg_light()} s")  # reason - are my lights too bright at night?


def _on_night() -> None:
    if _away_for_eve: return

    a(f"temp_night {read_temp()} s")  # reason - is it too warm to sleep?
    a(f"light_night {read_light()} s")  # reason - is it too bright to sleep?


def _on_before_wake() -> None:
    if _away_for_eve: return

    a(f"temp_before_wake {read_temp()} s")  # reason - do I wake up because it's too warm?
    a(f"light_before_wake {read_avg_light()} s")  # reason - do I wake up because it's too bright?


def _on_morning() -> None:
    if _away_for_eve: return

    a(f"light_morning {read_avg_light()} s")  # reason - it it bright enough to wake up?


# --------------------------- SCHEDULES -------------------------- #

week_schedule = schedule.every(1).weeks.do(_on_week)
# voc_schedule = schedule.every(3).days.at("17:00").do(on_voc)

eve_schedule = schedule.every().day.at(_detached).do(_on_eve)
night_schedule = schedule.every().day.at("01:00").do(_on_night)
before_wake_schedule = schedule.every().day.at(_before_wake).do(_on_before_wake)
morning_schedule = schedule.every().day.at("09:00").do(_on_morning)

# --------------------------- START -------------------------- #


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(20)
