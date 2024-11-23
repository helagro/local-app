import schedule
import time
from outward import is_away, a, get_routine, log

# ------------------------- CONSTANTS ------------------------ #

DETACHED_ROUTINE_NAME = "detached"

# ------------------------- VARIABLES ------------------------ #

detached = get_routine(DETACHED_ROUTINE_NAME) or "21:00"
voc = None
away_for_eve = is_away()

# ------------------------- ROUTINES ------------------------ #


def on_week() -> None:
    global detached
    new_detached = get_routine(DETACHED_ROUTINE_NAME)

    if new_detached is None:
        log("/on_week: new_detached is None")
    elif new_detached != detached:
        detached = new_detached
        print(f"on_week: detached updated to {detached}")

        schedule.cancel_job(eve_schedule)
        eve_schedule = schedule.every().day.at(detached).do(on_eve)

    a(f"on_week: detach is {detached}, btw")


def on_voc() -> None:
    if is_away():
        a("was away for on_voc")
        return
    a(f"on_voc: detached is {detached}, btw")


def on_eve() -> None:
    global away_for_eve
    away_for_eve = is_away()

    if away_for_eve:
        print("Was away for on_eve")
        return
    #a("on_eve")


def on_night() -> None:
    if away_for_eve: return
    #a("on_night")


def on_morning() -> None:
    if away_for_eve: return
    #a("on_morning")


# --------------------------- SCHEDULES -------------------------- #

week_schedule = schedule.every(1).weeks.do(on_week)
voc_schedule = schedule.every(3).days.at("17:00").do(on_voc)
eve_schedule = schedule.every().day.at(detached).do(on_eve)
night_schedule = schedule.every().day.at("01:00").do(on_night)
morning_schedule = schedule.every().day.at("09:00").do(on_morning)

# --------------------------- START -------------------------- #

if __name__ == '__main__':
    print("Checks: ")
    print(f"  Detached is {detached}")
    print(f"  Is away: {away_for_eve}")
    print("")

    while True:
        schedule.run_pending()
        time.sleep(20)
