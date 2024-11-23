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


def sample_light():
    
