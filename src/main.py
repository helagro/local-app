import schedule
import time
from outward import is_away, a, get_routine

detach = None
voc = None


def on_week():
    global detach
    detach = get_routine("detach")
    a(f"on_week: detach is {detach}, btw")


def on_voc():
    if is_away():
        a("was away for on_voc")
        return
    a(f"on_voc: detach is {detach}, btw")


def on_night():
    if is_away():
        print("Was away for on_night")
        return
    a("on_night")


# --------------------------- SCHEDULES -------------------------- #

test_schedule = schedule.every(40).seconds.do(lambda: print('Hello, World!'))
#night_schedule = schedule.every().day.at("01:00").do(on_night)
voc_schedule = schedule.every(3).days.at("17:00").do(on_voc)
week_schedule = schedule.every(1).weeks.do(on_week)

# --------------------------- START -------------------------- #

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(10)
