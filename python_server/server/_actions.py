from flask import Blueprint, request
from interfaces.actuators.led import get_lamp
import schedule
from interfaces.home import exec_preset_by_name, get_device, get_devices_string, get_last_preset_name
import log

bp = Blueprint('actions', __name__)
alarm_job = None


@bp.route('/log-test')
def log_test():
    from interfaces.api.server_app import log_to_server
    log_to_server("Test log from /log-test endpoint")
    return "ok"


@bp.route('/led/<string:name>')
def led(name: str):
    lamp = get_lamp(name)

    action = request.args.get('a', default='toggle').lower()

    if action == 'on':
        lamp.on()
    elif action == 'off':
        lamp.off()
    else:
        lamp.toggle()

    return "ok"


@bp.route('/t/<path:rest>')
def toggle_group(rest: str):
    names = rest.split('/')

    results = []
    for name in names:
        try:
            device = get_device(name)
            device.toggle()
            results.append({"name": name, "ok": True})
        except ValueError as e:
            results.append({
                "name": name,
                "ok": False,
                "error": str(e),
                "available_devices": get_devices_string(),
            })

    return "ok"


@bp.route('/last-preset')
def get_last_preset():
    preset = get_last_preset_name()
    if not preset:
        return 'NOT FOUND', 404

    return preset


@bp.route('/p/<string:name>')
def preset(name: str):
    state_mode = request.args.get('m', default=None)

    exec_preset_by_name(name, state_mode=state_mode)
    return "ok"


@bp.route('/alarm')
def alarm():
    global alarm_job

    time = request.args.get('t')
    if not time:
        return 'Missing time argument', 400

    if alarm_job:
        schedule.cancel_job(alarm_job)

    alarm_job = schedule.every().day.at(time).do(run_alarm)

    log_statement = f'Scheduled alarm for {time}'
    log.log(log_statement)
    return log_statement


@bp.route('/alarm/cancel')
def cancel_alarm():
    if alarm_job:
        schedule.cancel_job(alarm_job)

    return 'Canceled alarm'


# ================================== HELPERS ================================= #


def run_alarm():
    get_device('alarm').turn_on()

    return schedule.CancelJob
