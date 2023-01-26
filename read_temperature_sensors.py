from gpio_connections import *

import random # ONLY NEEDED TO SIMULATE DATA VALUES DURING DEVELOPMENT
from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

def _DS1820_reachable(slave_id):
    return True

def init_temperature_sensors():
    # init 1-Wire DS18B20 Temperature Sensors using default pin 7
    _ = TEMPERATURE_SENSOR_PIN
    if not _DS1820_reachable(PA_SENSOR_SLAVE_ID):
            print('Unable to reach {PA_SENSOR_SLAVE_ID}')

def _read_DS18820(address):
    temperature = random.random() * 30
    txt = '{:.1f} °C'
    return txt.format(temperature)

def read_pa_temperature():
    return _read_DS18820(PA_SENSOR_SLAVE_ID)

def read_preamp_temperature():
    return _read_DS18820(PREAMP_SENSOR_SLAVE_ID)
