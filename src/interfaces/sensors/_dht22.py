import adafruit_dht
import board

_dht = adafruit_dht.DHT22(board.D22, use_pulseio=False)


def read_temp() -> float:
    return float(_dht.temperature)


def read_hum() -> float:
    return float(_dht.humidity)
