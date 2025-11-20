import time
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection
from sensirion_i2c_sgp4x import Sgp40I2cDevice
from sensirion_gas_index_algorithm.voc_algorithm import VocAlgorithm

# ------------------------- VARIABLES ------------------------ #

RUN_TIME_SEC = 550
voc_algorithm = VocAlgorithm()

# ------------------------- FUNCTIONS ------------------------ #


def read(temperature: float, humidity: float) -> float | None:
    ''' Reads VOC index, then turns off the sensor '''

    transceiver = LinuxI2cTransceiver('/dev/i2c-1')
    i2c_connection = I2cConnection(transceiver)
    sgp40 = Sgp40I2cDevice(i2c_connection)

    try:
        voc_index = _take_reading(sgp40, temperature, humidity)
    except Exception as e:
        raise Exception(str(e))
    finally:
        _turn_off(sgp40, transceiver)

    return voc_index


def _take_reading(sgp40: Sgp40I2cDevice, temperature: float, humidity: float) -> float | None:
    for i in range(RUN_TIME_SEC):
        time.sleep(1)
        sraw_voc = sgp40.measure_raw(temperature=temperature, relative_humidity=humidity)
        voc_index = voc_algorithm.process(sraw_voc.ticks)
        if i % 60 == 0:
            print(f"VOC at {i}: {voc_index}")

    return voc_index


def _turn_off(sgp40: Sgp40I2cDevice, transceiver: LinuxI2cTransceiver) -> None:
    try:
        sgp40.turn_heater_off()
    except:
        pass
    time.sleep(1)
    transceiver.close()
