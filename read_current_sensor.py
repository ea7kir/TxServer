import pigpio
from gpio_connections import *

import random # ONLY NEEDED TO SIMULATE DATA VALUES DURING DEVELOPMENT
from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

def init_current_sensors():
    pass

def _read_sensor(address):
    current = random.random() * 10
    txt = '{:.1f} Amps'
    return txt.format(current)

def read_pa_current():
    return _read_sensor(PA_CURRENT_VOLTAGE_SENSOR)
