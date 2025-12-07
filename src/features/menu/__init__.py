from interfaces.api.time_tracking import track_activity, stop_tracking_activity
from interfaces.actuators.tradfri import get_device
from log import log

button_inputs = ['BTN_LEFT', 'BTN_RIGHT', 'BTN_MIDDLE', 'BTN_EXTRA', 'BTN_SIDE']
rest_inputs = ['l', 'r', 'm', 'e', 's', 'off', 'on', 'out', 'plant', 'chill']


def menu(command: str, input_set: list[str]) -> str | None:

    try:
        index = input_set.index(command)
    except ValueError:
        log(f"{command} not in {input_set}")
        return f"{command} not in {input_set}"

    match index:
        case 0:
            print("Left button action")
            get_device('eve').toggle()
        case 1:
            print("Right button action")
            get_device('day').toggle()
        case 2:
            print("Middle button action")
            get_device('read').toggle()
        case 3:
            print("Extra button action")
            track_activity()
        case 4:
            print("Side button action")
            stop_tracking_activity()
        case 5:
            print("Turning off all devices")
            get_device('all').turn_off()
        case 6:
            print("Turn on all devices")
            get_device('all').turn_on()
        case 7:
            print('Turning off lamps for leaving')
            get_device('out').turn_off()
        case 8:
            print('Toggle plant lamp')
            get_device('plant').toggle()
        case 9:
            print('Turn on chill group')
            get_device('chill').turn_on()
        case _:
            print(f"Unhandled command: {command}")
            return
