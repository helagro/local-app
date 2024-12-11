import asyncio

import BME280
import TSL2591
import LTR390

# ----------------------- SETUP SENSORS ---------------------- #

bme280 = BME280.BME280()
bme280.get_calib_param()

light = TSL2591.TSL2591()

uv = LTR390.LTR390()

# ---------------------- SIMPLE READINGS --------------------- #


def read_voc():
    return 500


def read_pressure():
    return round(bme280.readData()[0], 2)


def read_temp():
    return round(bme280.readData()[1], 2)


def read_hum():
    return round(bme280.readData()[2], 2)


def read_light(max=None):
    lux = round(light.Lux(), 2)

    if max and lux > max:
        return None
    else:
        return lux


def read_uv():
    return uv.UVS()


# ------------------------- ADVANCED ------------------------- #


async def read_avg_light(callback: callable, max=None):
    interval = 15 * 60
    duration = 45 * 60

    num_samples = duration // interval
    samples = []

    for _ in range(num_samples):
        value = read_light(max=max)
        samples.append(value)
        await asyncio.sleep(interval)

    average = sum(samples) / len(samples)
    callback(average)
