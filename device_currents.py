import pigpio
import time
from device_constants import PA_CURRENT_ADDRESS, PA_CURRENT_SHUNT_OHM, PA_CURRENT_MAX_AMP

class INA226Reader():
    """
    A class to read an INA266 current/voltage sensor.
    """
    def __init__(self, pi, address, shunt_ohm, max_amp):
        self.pi = pi
        self.address = address
        self.shunt_ohm = shunt_ohm
        self.max_amp = max_amp

    def current(self):
        current = 1.1111
        txt = '{:.1f} Amps'
        return txt.format(current)

    def voltage(self):
        voltage = 2.22222
        txt = '{:.1f} Volts'
        return txt.format(voltage)

    def cancel(self):
        pass

_pa_current_sensor = None

def configure_current_sensors(pi):
    global _pa_current_sensor
    _pa_current_sensor = INA226Reader(pi, PA_CURRENT_ADDRESS, PA_CURRENT_SHUNT_OHM, PA_CURRENT_MAX_AMP)

def shutdown_current_sensors():
    _pa_current_sensor.cancel()

def _read_sensor(address):
    current = random.random() * 10
    txt = _pa_current_sensor.current()
    return txt.format(current)

def read_pa_current():
    return _pa_current_sensor.current()

def read_pa_voltage():
    return _pa_current_sensor.voltage()

if __name__ == '__main__':
    pi_outside = pigpio.pi()
    configure_current_sensors(pi_outside)
    for i in range(1, 10):
        amps = read_pa_current()
        volts = read_pa_voltage()
        print(amps, volts)
        time.sleep(1)
    shutdown_current_sensors()
    pi_outside.stop()
