# ================================== IMPORT ================================== #

import json
from typing import Literal, TypedDict

from requests import request
import os

try:
    from log import log
except ImportError:

    def log(message: str):
        print(message)


# =================================== TYPES ================================== #

DeviceState = Literal['on', 'off', 'toggle']


class Payload(TypedDict, total=False):
    entity_id: str
    brightness: int
    color_temp_kelvin: int
    state: str
    rgb_color: tuple[int, int, int]
    transition: int
    attributes: dict


# ================================= VARIABLES ================================ #

url = 'http://' + (os.getenv('LOCAL_SERVER_IP') or 'localhost') + ':8123/api'
token = os.getenv('HOME_ASSISTANT_TOKEN')

# ================================== GETTERS ================================= #


def is_on(entity_id: str) -> bool:
    state = get_state(entity_id)
    return (state is not None) and state.get('state') == 'on'


def get_state(entity_id: str):
    return _api(f'/states/{entity_id}')


def get_services():
    return _api(f'/services')


# ================================== ACTIONS ================================= #


def set_state(entity_id: str, state: str, attributes: dict | None = None):
    data: Payload = {'state': state, 'attributes': attributes or {}}
    return _api(f'/states/{entity_id}', method='post', data=data)


def switch(entity_id: str, state: DeviceState):
    if state not in ['on', 'off', 'toggle']:
        raise ValueError("State must be 'on', 'off', or 'toggle'")

    service = _get_service(state)
    domain = entity_id.split('.')[0]

    return _api(f'/services/{domain}/{service}', method='post', data={'entity_id': entity_id})


def switch_custom(entity_id: str, state: DeviceState, payload: Payload):
    service = _get_service(state)
    domain = entity_id.split('.')[0]

    return _api(f'/services/{domain}/{service}', method='post', data={'entity_id': entity_id, **payload})


def brightness(entity_id: str, level: int):
    if not (0 <= level <= 255):
        raise ValueError("Brightness level must be between 0 and 255")

    return _api(f'/services/light/turn_on', method='post', data={'entity_id': entity_id, 'brightness': level})


def color(entity_id: str, color: str | int):
    data: Payload = {'entity_id': entity_id}
    data.update(get_color_dict(color))

    is_on_val = is_on(entity_id)
    if not is_on_val:
        data['brightness'] = 1
        data['transition'] = 0

    res = _api('/services/light/turn_on', method='post', data=data)

    if not is_on_val:
        switch(entity_id, 'off')

    return res


# ================================== HELPERS ================================= #


def get_color_dict(color: str | int) -> dict:
    if isinstance(color, int):
        return {'color_temp_kelvin': color}
    else:
        color_rgb = _hex_to_rgb(color)
        return {'rgb_color': color_rgb}


def _get_service(state: str) -> str:
    if state == 'on':
        return 'turn_on'
    elif state == 'off':
        return 'turn_off'
    elif state == 'toggle':
        return 'toggle'
    else:
        raise ValueError("State must be 'on', 'off', or 'toggle'")


def _hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def _api(endpoint: str, method: str = 'get', data: Payload | None = None, log_response: bool = False):
    if token is None:
        raise Exception('Home Assistant token not set')

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }

    full_url = url + endpoint
    response = request(method, full_url, headers=headers, json=data)

    entity_id = data.get('entity_id', 'unknown') if data else 'unknown'
    log(f"{method} TO {full_url} FOR {entity_id} YIELDED {response.status_code}")

    if response.status_code in [200, 201, 204]:
        if response.content:
            json_response = response.json()
            if log_response:
                log(f"{endpoint} RESPONDED: {json.dumps(json_response, indent=2)}")

            return json_response
        return None
    else:
        log(f"Error in Home Assistant API request to {endpoint}: {response.status_code} - {response.text}")
        return None
