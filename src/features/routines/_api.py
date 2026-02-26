from interfaces.api.server_app import get_routines

_routines = {}


def get_routine(name: str) -> str | None:
    return _routines.get(name)


def sync_routines():
    global _routines

    routines = get_routines()
    if not routines: return

    _routines = routines
