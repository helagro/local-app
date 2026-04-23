import time
import adafruit_dht
import board
from interfaces.api.config import get_cached

_dht = adafruit_dht.DHT22(board.D22, use_pulseio=False)

MAX_ATTEMPTS = 10


def read_temp() -> float:
    cfg = get_cached()
    TEMP_COMPENSATION = cfg.externalTempCompensation if cfg else 0.0

    for _ in range(MAX_ATTEMPTS):
        try:
            return float(_dht.temperature) + (TEMP_COMPENSATION or 0.0)
        except RuntimeError:
            time.sleep(2.5)
    raise RuntimeError("Failed to read from DHT22 sensor after multiple attempts")


def read_hum() -> float:
    for _ in range(MAX_ATTEMPTS):
        try:
            return float(_dht.humidity)
        except RuntimeError:
            time.sleep(2.5)
    raise RuntimeError("Failed to read from DHT22 sensor after multiple attempts")
