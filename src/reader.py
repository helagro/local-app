import schedule
import time
from outward import is_away, a, get_routine, log

# ------------------------- CONSTANTS ------------------------ #

DETACHED_ROUTINE_NAME = "detached"

# ------------------------- VARIABLES ------------------------ #

_detached = get_routine(DETACHED_ROUTINE_NAME) or "21:00"
_voc = None
_away_for_eve = is_away()

# -------------------------- GETTERS ------------------------- #


def get_detached() -> str:
    return _detached


def get_away_for_eve() -> bool:
    return _away_for_eve


# ------------------------- ROUTINES ------------------------ #


def on_week() -> None:
    global _detached
    new_detached = get_routine(DETACHED_ROUTINE_NAME)

    if new_detached is None:
        log("/on_week: new_detached is None")
    elif new_detached != _detached:
        _detached = new_detached
        print(f"on_week: detached updated to {_detached}")

        schedule.cancel_job(eve_schedule)
        eve_schedule = schedule.every().day.at(_detached).do(on_eve)

    a(f"on_week: detach is {_detached}, btw")


def on_voc() -> None:
    if is_away():
        a("was away for on_voc")
        return
    a(f"on_voc: detached is {_detached}, btw")


def on_eve() -> None:
    global _away_for_eve
    _away_for_eve = is_away()

    if _away_for_eve:
        print("Was away for on_eve")
        return
    #a("on_eve")


def on_night() -> None:
    if _away_for_eve: return
    #a("on_night")


def on_morning() -> None:
    if _away_for_eve: return
    #a("on_morning")


# --------------------------- SCHEDULES -------------------------- #

week_schedule = schedule.every(1).weeks.do(on_week)
voc_schedule = schedule.every(3).days.at("17:00").do(on_voc)
eve_schedule = schedule.every().day.at(_detached).do(on_eve)
night_schedule = schedule.every().day.at("01:00").do(on_night)
morning_schedule = schedule.every().day.at("09:00").do(on_morning)

# --------------------------- START -------------------------- #


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(20)
