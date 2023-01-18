import random # ONLY NEEDED TO SIMULATE DATA VALUES DURING DEVELOPMENT
from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

PA_CURRENT_VOLTAGE_SENSOR = 0

def _read_sensor(address):
    current = random.random() * 10
    txt = '{:.1f} Amps'
    return txt.format(current)

def read_pa_current():
    return _read_sensor(PA_CURRENT_VOLTAGE_SENSOR)
