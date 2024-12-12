import asyncio
import sys
import os

sys.path.append(os.path.dirname(__file__))

try:
    import BME280
    import TSL2591
    import LTR390
    # import SGP40

    from sensirion_gas_index_algorithm.voc_algorithm import VocAlgorithm
except Exception as e:
    print(f"Error importing sensor libraries: {e}")

# ----------------------- SETUP SENSORS ---------------------- #

try:
    bme280 = BME280.BME280()
    bme280.get_calib_param()
except Exception as e:
    print(f"Error initialising BME280: {e}")

try:
    light = TSL2591.TSL2591()
except Exception as e:
    print(f"Error initialising TSL2591: {e}")

try:
    uv = LTR390.LTR390()
except Exception as e:
    print(f"Error initialising LTR390: {e}")

try:
    sgp = SGP40.SGP40()
except Exception as e:
    print(f"Error initialising SGP40: {e}")

# ---------------------- SIMPLE READINGS --------------------- #


def read_voc() -> float | None:
    temp = read_temp()
    hum = read_hum()

    if temp is None or hum is None:
        print("Got bad temp or hum value WHEN reading VOC")
        return None

    try:
        voc_raw = sgp.measureRaw(tmp, hum)
         
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
        return round(bme280.readData()[1], 2)
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None


def read_hum() -> float:
    try:
        return round(bme280.readData()[2], 2)
    except Exception as e:
        print(f"Error reading humidity: {e}")
        return None


def read_light(max=None) -> float | None:
    try:
        raw_lux = light.Lux()
        lux = 0.0 if raw_lux == 0 else round(light.Lux(), 2)
    except Exception as e:
        print(f"Error reading light: {e}")
        return None

    if max and lux > max:
        return None
    else:
        return lux


def read_uv() -> float:
    try:
        return uv.UVS()
    except Exception as e:
        print(f"Error reading UV: {e}")
        return None


# ------------------------- ADVANCED ------------------------- #


async def read_avg_light(callback: callable, max=None):
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
        await asyncio.sleep(interval)

    average = sum(samples) / len(samples)
    callback(average)
