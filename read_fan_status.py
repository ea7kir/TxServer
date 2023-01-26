import pigpio
from gpio_constents import ENCLOSURE_INTAKE_FAN_GPIO, ENCLOSURE_EXTRACT_FAN_GPIO
from gpio_constents import PA_INTAKE_FAN_GPIO, PA_EXTRACT_FAN_GPIO

import random # ONLY NEEDED TO SIMULATE DATA VALUES DURING DEVELOPMENT
from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

_pi = None

def _config_fan(gpio):
    return

def configure_fan_sensors(pi):
    global _pi
    _pi = pi
    _config_fan(ENCLOSURE_INTAKE_FAN_GPIO)
    _config_fan(ENCLOSURE_EXTRACT_FAN_GPIO)
    _config_fan(PA_INTAKE_FAN_GPIO)
    _config_fan(PA_EXTRACT_FAN_GPIO)

def shutdown_fan_sensors():
    pass

def _read_sensor(gpio):
    moving = bool(random.randint(0, 1))
    return moving

def read_fan_status():
    a = ' ';  b = ' '; c = ' '; d = ' '
    if _read_sensor(ENCLOSURE_INTAKE_FAN_GPIO):  a = '1'
    if _read_sensor(ENCLOSURE_EXTRACT_FAN_GPIO): b = '2'
    if _read_sensor(PA_INTAKE_FAN_GPIO):         c = '3'
    if _read_sensor(PA_EXTRACT_FAN_GPIO):        d = '4'
    return a + b + c + d
    #moving = _read_sensor(ENCLOSURE_INTAKE_FAN_GPIO)
    #moving &= _read_sensor(ENCLOSURE_EXTRACT_FAN_GPIO)
    #moving &= _read_sensor(PA_INTAKE_FAN_GPIO)
    #moving &= _read_sensor(PA_EXTRACT_FAN_GPIO)
    ##return 'RUN'
    #if moving:
    #    return 'OK'
    #else:
    #    return '-'
