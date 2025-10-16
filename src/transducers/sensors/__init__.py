import sys
import os
from dotenv import load_dotenv
import time
from typing import Callable
from remote_interfaces import get_config
from log import log

sys.path.append(os.path.dirname(__file__))

# ----------------------- COMPENSATE ----------------------- #

load_dotenv()
TEMP_COMPENSATION = get_config('tempCompensation') or 0.0

# ----------------------- SETUP SENSORS ---------------------- #

try:
    import transducers.sensors._BME280 as _BME280
    bme280 = _BME280.BME280()
    bme280.get_calib_param()
except Exception as e:
    log(f"Error initialising BME280: {e}")
    _BME280 = None

try:
    import transducers.sensors._TSL2591 as _TSL2591
    light = _TSL2591.TSL2591()
except Exception as e:
    log(f"Error initialising TSL2591: {e}")
    _TSL2591 = None

try:
    import transducers.sensors._LTR390 as _LTR390
    uv = _LTR390.LTR390()
except Exception as e:
    log(f"Error initialising LTR390: {e}")
    _LTR390 = None

try:
    import transducers.sensors._sgp40 as _sgp40
except Exception as e:
    log(f"Error initialising SGP40: {e}")
    _sgp40 = None

# ------------------------ GET LAST VALUE ------------------------ #

_last_voc = None


def get_last_voc() -> float | None:
    return _last_voc


# ---------------------- SIMPLE READINGS --------------------- #


def read_voc() -> float | None:
    global _last_voc

    if _sgp40 is None:
        log("SGP40 sensor not initialised")
        return None

    temp = read_temp()
    hum = read_hum()

    if temp is None or hum is None:
        log("Got bad temp or hum value WHEN reading VOC")
        return None

    log("Reading VOC...")
    try:
        _last_voc = _sgp40.read(temp, hum)
        return _last_voc

    except Exception as e:
        log(f"Error reading VOC: {e}")
        return None


def read_pressure() -> float | None:
    try:
        return round(bme280.readData()[0], 2)
    except Exception as e:
        log(f"Error reading pressure: {e}")
        return None


def read_temp() -> float | None:
    try:
        raw_temp = bme280.readData()[1] + TEMP_COMPENSATION
        return round(raw_temp, 2)
    except Exception as e:
        log(f"Error reading temperature: {e}")
        return None


def read_hum() -> float | None:
    try:
        return round(bme280.readData()[2], 2)
    except Exception as e:
        log(f"Error reading humidity: {e}")
        return None


def read_light(max=None) -> float | None:
    try:
        lux = round(light.Lux(), 2)
    except ZeroDivisionError:
        lux = 0
    except Exception as e:
        log(f"Error reading light: {e}")
        return None

    if max and lux > max:
        return None
    else:
        return lux


def read_uv() -> float | None:
    try:
        return uv.UVS()
    except Exception as e:
        log(f"Error reading UV: {e}")
        return None


# ------------------------- ADVANCED ------------------------- #


def read_avg_light(callback: Callable, max=None) -> None:
    interval = 15 * 60
    duration = 45 * 60

    num_samples = duration // interval
    samples = []

    for _ in range(num_samples):
        value = read_light(max=max)
        if value is None:
            log("Got bad light value")
            return

        samples.append(value)

        time.sleep(interval)

    average = sum(samples) / len(samples)
    callback(average)
