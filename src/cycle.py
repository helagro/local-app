import schedule
import time
from outward import is_away, a, get_routine, log
from sensors import read_voc, read_temp, read_hum, read_light, read_uv, read_pressure

# ------------------------- CONSTANTS ------------------------ #

BEFORE_WAKE_ROUTINE_NAME = "before_wake"
DETACHED_ROUTINE_NAME = "detached"

# ------------------------- VARIABLES ------------------------ #

_before_wake = get_routine(BEFORE_WAKE_ROUTINE_NAME) or "07:00"
_detached = get_routine(DETACHED_ROUTINE_NAME) or "21:00"

_voc = None
_away_for_eve = is_away()

# -------------------------- GETTERS ------------------------- #


def get_detached() -> str:
    return _detached


def get_before_wake() -> str:
    return _before_wake


def get_away_for_eve() -> bool:
    return _away_for_eve


# --------------------- UPDATING ROUTINE --------------------- #


def on_week() -> None:
    global _before_wake, _detached
    _before_wake = try_updating_routine(BEFORE_WAKE_ROUTINE_NAME, _before_wake, morning_schedule, on_morning)
    _detached = try_updating_routine(DETACHED_ROUTINE_NAME, _detached, eve_schedule, on_eve)


def try_updating_routine(name: str, old_value: str, job: schedule.Job, fun: callable) -> str | None:
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


def on_voc() -> None:
    global _voc

    if is_away():
        a("was away for on_voc")
        return

    _voc = read_voc()


def on_eve() -> None:
    global _away_for_eve
    _away_for_eve = is_away()

    if _away_for_eve:
        print("Was away for on_eve")
        return

    a(f"voc {_voc}")
    a(f"hum {read_hum()}")
    a(f"light {read_light()}")
    a(f"pressure {read_pressure()}")


def on_night() -> None:
    if _away_for_eve: return

    a(f"uv {read_uv()}")
    a(f"temp {read_temp()}")
    a(f"light {read_light()}")


def on_before_wake() -> None:
    if _away_for_eve: return

    a(f"temp {read_temp()}")
    a(f"light {read_light()}")


def on_morning() -> None:
    if _away_for_eve: return

    a(f"light {read_light()}")


# --------------------------- SCHEDULES -------------------------- #

week_schedule = schedule.every(1).weeks.do(on_week)
voc_schedule = schedule.every(3).days.at("17:00").do(on_voc)

eve_schedule = schedule.every().day.at(_detached).do(on_eve)
night_schedule = schedule.every().day.at("01:00").do(on_night)
before_wake_schedule = schedule.every().day.at(_before_wake).do(on_before_wake)
morning_schedule = schedule.every().day.at("09:00").do(on_morning)

# --------------------------- START -------------------------- #


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(20)
