from typing import Any
from remote_interfaces.server_app import get_routine, log
from collections.abc import Callable
import schedule


class Routine:
    job: Any = None

    def __init__(self, name: str, time: str, function: Callable) -> None:
        self.name = name
        self.time = time
        self._function = function
        self.job = schedule.every().day.at(self.time).do(function)

    def update(self) -> None:
        log(f"/update: Skipped update for local routine {self.name}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, time={self.time!r})"


class SyncedRoutine(Routine):

    def __init__(self, name: str, default_time: str, function: Callable) -> None:
        time = get_routine(name) or default_time
        super().__init__(name, time, function)

    def update(self) -> None:
        new_time = get_routine(self.name)
        if not new_time:
            log(f"/update: Routine {self.name} could not be fetched")
            return

        if new_time != self.time:
            log(f"/update: Routine {self.name} updated to {new_time}")
            self.time = new_time
            schedule.cancel_job(self.job)
            self.job = schedule.every().day.at(self.time).do(self._function)
