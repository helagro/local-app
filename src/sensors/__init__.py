import sys
import os
from dotenv import load_dotenv
import time
from typing import Callable
from outward import get_config

sys.path.append(os.path.dirname(__file__))

# ----------------------- COMPENSATE ----------------------- #

load_dotenv()
TEMP_COMPENSATION = get_config('tempCompensation') or 0.0

# ----------------------- SETUP SENSORS ---------------------- #

try:
    import BME280
    bme280 = BME280.BME280()
    bme280.get_calib_param()
except Exception as e:
    print(f"Error initialising BME280: {e}")
    BME280 = None

try:
    import TSL2591
    light = TSL2591.TSL2591()
except Exception as e:
    print(f"Error initialising TSL2591: {e}")
    TSL2591 = None

try:
    import LTR390
    uv = LTR390.LTR390()
except Exception as e:
    print(f"Error initialising LTR390: {e}")
    LTR390 = None

try:
    import sgp40
except Exception as e:
    print(f"Error initialising SGP40: {e}")
    sgp40 = None

# ------------------------ GET LAST VALUE ------------------------ #

_last_voc = None


def get_last_voc() -> float | None:
    return _last_voc


# ---------------------- SIMPLE READINGS --------------------- #


def read_voc() -> float | None:
    global _last_voc

    if sgp40 is None:
        print("SGP40 sensor not initialised")
        return None

    temp = read_temp()
    hum = read_hum()

    if temp is None or hum is None:
        print("Got bad temp or hum value WHEN reading VOC")
        return None

    print("Reading VOC...")
    try:
        _last_voc = sgp40.read(temp, hum)
        return _last_voc

    except Exception as e:
        print(f"Error reading VOC: {e}")
        return None


def read_pressure() -> float | None:
    try:
        return round(bme280.readData()[0], 2)
    except Exception as e:
        print(f"Error reading pressure: {e}")
        return None


def read_temp() -> float | None:
    try:
        raw_temp = bme280.readData()[1] + TEMP_COMPENSATION
        return round(raw_temp, 2)
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None


def read_hum() -> float | None:
    try:
        return round(bme280.readData()[2], 2)
    except Exception as e:
        print(f"Error reading humidity: {e}")
        return None


def read_light(max=None) -> float | None:
    try:
        lux = round(light.Lux(), 2)
    except ZeroDivisionError:
        lux = 0
    except Exception as e:
        print(f"Error reading light: {e}")
        return None

    if max and lux > max:
        return None
    else:
        return lux


def read_uv() -> float | None:
    try:
        return uv.UVS()
    except Exception as e:
        print(f"Error reading UV: {e}")
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
            print("Got bad light value")
            return

        samples.append(value)

        time.sleep(interval)

    average = sum(samples) / len(samples)
    callback(average)
