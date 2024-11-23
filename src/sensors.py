import asyncio

# ---------------------- SIMPLE READINGS --------------------- #


def read_voc():
    return 500


def read_temp():
    return 25.0


def read_hum():
    return 50.0


def read_light(max=None):
    if max and 1000 > max:
        return None
    else:
        return 1000


def read_uv():
    return 0


def read_pressure():
    return 1000


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
