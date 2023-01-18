import random # ONLY NEEDED TO SIMULATE DATA VALUES DURING DEVELOPMENT
from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

PA_SENSOR_ADDRESS = 'abc'
PREAMP_SENSOR_ADDRESS = 'def'

def _read_sensor(address):
    temperature = random.random() * 30
    txt = '{:.1f} °C'
    return txt.format(temperature)

def read_pa_temperature():
    return _read_sensor(PA_SENSOR_ADDRESS)

def read_preamp_temperature():
    return _read_sensor(PREAMP_SENSOR_ADDRESS)
