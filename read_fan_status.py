import random # ONLY NEEDED TO SIMULATE DATA VALUES DURING DEVELOPMENT
from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

ENCLOSURE_INTAKE_FAN_ADDRESS    = 1
ENCLOSURE_EXTRACT_FAN_ADDRESS   = 2
PA_INTAKE_FAN_ADDRESS           = 3
PA_EXTRACT_FAN_ADDRESS          = 4

def _read_sensor(address):
    moving = bool(random.randint(0, 1))
    return moving

def read_fan_status():
    a = ' ';  b = ' '; c = ' '; d = ' '
    if _read_sensor(ENCLOSURE_INTAKE_FAN_ADDRESS):  a = '1'
    if _read_sensor(ENCLOSURE_INTAKE_FAN_ADDRESS):  b = '2'
    if _read_sensor(PA_INTAKE_FAN_ADDRESS):         c = '3'
    if _read_sensor(PA_EXTRACT_FAN_ADDRESS):        d = '4'
    return a + b + c + d
    #moving = _read_sensor(ENCLOSURE_INTAKE_FAN_ADDRESS)
    #moving &= _read_sensor(ENCLOSURE_EXTRACT_FAN_ADDRESS)
    #moving &= _read_sensor(PA_INTAKE_FAN_ADDRESS)
    #moving &= _read_sensor(PA_EXTRACT_FAN_ADDRESS)
    ##return 'RUN'
    #if moving:
    #    return 'OK'
    #else:
    #    return '-'
