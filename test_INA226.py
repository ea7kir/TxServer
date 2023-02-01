import pigpio
from time import sleep
from device_constants import PA_CURRENT_ADDRESS, PA_CURRENT_SHUNT_OHM, PA_CURRENT_MAX_AMP

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
    float_current = 7.89
    return '{:.1f} Amps'.format(float_current)

def read_pa_current():
    return _read_sensor(PA_CURRENT_ADDRESS)

def _read_INA266(address): # returns (current, voltage)
    float_current = 1.23
    float_voltage = 27.89
    return '{:.1f} Amps'.format(float_current), '{:.1f} Volts'.format(float_voltage)


if __name__ == '__main__':
    pi_outside = pigpio.pi()
    configure_current_sensors(pi_outside)
    current = read_pa_current()
    voltage = '-'
    print(current, voltage)