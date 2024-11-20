import schedule
import time
from outward import is_away, a


def on_night():
    if is_away(): return
    a("night")


test = schedule.every(4).seconds.do(lambda: print('Hello, World!'))
night = schedule.every().day.at("01:00").do(on_night)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(10)
