from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json
import uuid
import os
from enum import Enum
import threading
from os import path

timers = {}


class Action(Enum):
    SET_STATE = 0
    TEMPORARY_ON = 1
    TOGGLE = 2


api = lambda x: print('API not yet initialized')
gateway = None
credentials_path = path.join('..', 'config', 'generated_tradfri_credentials.json')
gateway_addr: str | None = os.environ.get("TRADFRI_ADDR")

if not gateway_addr:
    raise PytradfriError("E-3: TRADFRI_ADDR is not set")
else:
    print(f"Using Tradfri Gateway at {gateway_addr}")


def init() -> None:

    print("Connecting to Tradfri Gateway...")

    success = auth_with_generated_credentials()
    if not success:
        key = os.environ.get("TRADFRI_CODE")
        if not key:
            raise PytradfriError("E-39: TRADFRI_CODE is not set")
        auth_with_key(key)


# ----------------------- AUTHENTICATE ----------------------- #


def auth_with_generated_credentials() -> bool:
    conf = load_json(credentials_path)

    try:
        api_factory = APIFactory(host=gateway_addr, psk_id=conf["identity"], psk=conf["key"])
        setup_api(api_factory)
        return True

    except KeyError:
        return False


def auth_with_key(key: str) -> None:
    identity = uuid.uuid4().hex
    apiFactory = APIFactory(host=gateway_addr, psk_id=identity)

    try:
        psk = apiFactory.generate_psk(key)
        save_json(credentials_path, {"identity": identity, "key": psk})
        setup_api(apiFactory)
    except AttributeError:
        raise PytradfriError("E-2: Invalid key")


def setup_api(apiFactory: APIFactory) -> None:
    global api, gateway

    api = apiFactory.request
    if not api:
        raise PytradfriError("Failed to create API handler")

    gateway = Gateway()
    print("Connected to Tradfri Gateway")


# --------------------------- METHODS -------------------------- #


def get_devices() -> list[dict]:
    if not gateway:
        raise PytradfriError('Gateway not initialized')

    devices = api(api(gateway.get_devices()))
    applicableDevices = []

    for device in devices or []:
        if device.has_light_control or device.has_socket_control or device.has_blind_control:
            applicableDevices.append({"id": device.id, "name": device.name})

    return applicableDevices


def execute(deviceID: int, action: int, payload: int) -> None:
    try:
        device = getDevice(deviceID)
        deviceControl = getDeviceControl(device)

        if not device:
            raise PytradfriError(f'Device with ID {deviceID} not found')

        print("Executing action:", action, "with payload:", payload, "on device:", device)

        if (timers.get(deviceID)):
            timers[deviceID].cancel()

        if action == Action.SET_STATE.value:
            if payload == 1:
                api(deviceControl.set_state(True))
            elif payload == 0:
                api(deviceControl.set_state(False))
            else:
                print(f"E-22: Invalid payload {payload}")

        elif action == Action.TEMPORARY_ON.value:
            api(deviceControl.set_state(True))
            timer = threading.Timer(payload, lambda: afterTemporaryOn(deviceID, deviceControl))
            timer.start()
            timers[deviceID] = timer

        elif action == Action.TOGGLE.value:
            if device.has_light_control:
                api(deviceControl.set_state(not deviceControl.lights[0].state))
            elif device.has_socket_control:
                api(deviceControl.set_state(not deviceControl.sockets[0].state))
            elif device.has_blind_control:
                api(deviceControl.set_state(not deviceControl.blinds[0].state))
            else:
                raise PytradfriError(f"E-7: Device {device.id} has no valid control")

        else:
            raise PytradfriError(f"E-5: Invalid action {action}")
    except Exception as e:
        print(f"E-57: execute tradfri error: {e}")


def getDevice(deviceID: int):
    if not gateway:
        raise PytradfriError('Gateway not initialized')

    return api(gateway.get_device(deviceID))


def getDeviceControl(device):
    if device.has_light_control:
        return device.light_control
    elif device.has_socket_control:
        return device.socket_control
    elif device.has_blind_control:
        return device.blind_control
    else:
        raise PytradfriError(f"E-6: Device {device.id} has no control")


def afterTemporaryOn(deviceID: int, deviceControl) -> None:
    api(deviceControl.set_state(False))
    timers.pop(deviceID)


init()
