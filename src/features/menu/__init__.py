from features.activity import toggle_activity
from interfaces.actuators.led import get_lamps
from interfaces.api.time_tracking import track_activity, stop_tracking_activity
from interfaces.actuators.tradfri import exec_preset_by_name, get_device
from log import log

rest_inputs = ['0', '1', '2', '3', '4']


def menu(command: str, input_set: list[str]) -> str | None:

    try:
        index = input_set.index(command)
    except ValueError:
        log(f"{command} not in {input_set}")
        return f"{command} not in {input_set}"

    match index:
        case 0:
            get_device('eve').toggle()
        case 1:
            exec_preset_by_name('chill')
        case 2:
            exec_preset_by_name('work')
        case 3:
            get_device('out').toggle()

            leds = get_lamps()
            for led in leds.values():
                led.off()
        case 4:
            toggle_activity()
        case _:
            log(f"Unhandled command: {command}")
            return
