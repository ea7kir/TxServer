import pigpio
from device_constants import PA_CURRENT_ADDRESS, PA_CURRENT_SHUNT_OHM, PA_CURRENT_MAX_AMP

import random # ONLY NEEDED TO SIMULATE DATA VALUES DURING DEVELOPMENT
from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

_pi = None

# address: 0x42, shuntOhm: 0.002, maxAmp: 10
def _config_INA226(address, shunt_ohm, max_amp):
    pass

def configure_current_sensors(pi):
    global _pi
    _pi = pi
    _config_INA226(PA_CURRENT_ADDRESS, PA_CURRENT_SHUNT_OHM, PA_CURRENT_MAX_AMP)

def shutdown_current_sensors():
    pass

def _read_sensor(address):
    current = random.random() * 10
    txt = '{:.1f} Amps'
    return txt.format(current)

def read_pa_current():
    return _read_sensor(PA_CURRENT_ADDRESS)
