import pigpio
from device_constants import TEMPERATURE_SENSOR_GPIO, PA_SENSOR_SLAVE_ID, PREAMP_SENSOR_SLAVE_ID

import random # ONLY NEEDED TO SIMULATE DATA VALUES DURING DEVELOPMENT
from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

_pi = None

def _DS1820_reachable(slave_id):
    return True

def _init_DS1820(slave_id):
    _ = TEMPERATURE_SENSOR_GPIO
    # init 1-Wire DS18B20 Temperature Sensors using default pin 7
    _ = TEMPERATURE_SENSOR_GPIO
    if not _DS1820_reachable(slave_id):
            print('Unable to reach {slave_id}')
    
def configure_temperature_sensors(pi):
    global _pi
    _pi = pi
    _init_DS1820(PA_SENSOR_SLAVE_ID)
    _init_DS1820(PREAMP_SENSOR_SLAVE_ID)

def shutdown_temperature_sensors():
    pass

def _read_DS18820(address):
    temperature = random.random() * 30
    txt = '{:.1f} °C'
    return txt.format(temperature)

def read_pa_temperature():
    return _read_DS18820(PA_SENSOR_SLAVE_ID)

def read_preamp_temperature():
    return _read_DS18820(PREAMP_SENSOR_SLAVE_ID)
