import pigpio
import time
from math import floor
from device_constants import PA_CURRENT_ADDRESS, PA_CURRENT_SHUNT_OHM, PA_CURRENT_MAX_AMP

class INA226Reader():
    """
    A class to read an INA266 current/voltage sensor.
    """
    _INA226_RESET = 0x8000 # :UInt16
    _INA226_REG_CALIBRATION = 0x05 # UInt8
    _INA226_REG_CONFIGURATION = 0x00 # UInt8
    _INA226_TIME_8MS = 7 # 8.244ms # :UInt8
    _INA226_AVERAGES_16 = 2 # :UInt8
    _INA226_MODE_SHUNT_BUS_CONTINUOUS = 7 # :UI
    _INA226_REG_BUS_VOLTAGE = 0x02 # :UInt8
    _INA226_REG_CURRENT = 0x04 # :UInt8
    _pi = None
    _handle = None
    _available = False
    _currentLSBs = None

    def __init__(self, pi, address, shunt_ohm, max_amp):
        """
        Use 'sudo i2cdetect -y 1' to display the connected I2C devices.
        """
        self._pi = pi
        I2C_BUSS = 1
        try:
            # open
            self._handle = self._pi.i2c_open(I2C_BUSS, address) #, I2C_FLAGS)

            # reset
            time.sleep(0.200)
            self._pi.i2c_write_word_data(self._handle, self._INA226_REG_CONFIGURATION, self._INA226_RESET)

            # configure
            time.sleep(0.200)
            shunt = self._INA226_TIME_8MS
            average = self._INA226_AVERAGES_16
            mode = self._INA226_MODE_SHUNT_BUS_CONTINUOUS

            # calibrate
            time.sleep(0.200)
            self._currentLSBs = max_amp / float(1 << 15) # max_current / (1 << 15)
            calib: float = 0.00512 / (self._currentLSBs * shunt_ohm)
            calibReg = int(floor(calib)) # :UInt16
            self._currentLSBs = 0.00512 / (shunt_ohm * float(calibReg)) # 0.00512 / (r_shunt * calib_reg)
            self._pi.i2c_write_word_data(self._handle, self._INA226_REG_CALIBRATION, calibReg) #calibReg.byteSwapped)

            # configure
            time.sleep(0.200)
            configReg = (int(average) << 9) | (int(I2C_BUSS) << 6) | (int(shunt) << 3) | int(mode)
            self._pi.i2c_write_word_data(self._handle, self._INA226_REG_CONFIGURATION, configReg) #configReg.byteSwapped)
            self._available = True
        except:
            print(f'EXCEPTION configuring INA266 at {hex(address)}')
            self._available = False

    def current(self):
        if not self._available:
            return '? Amps'
        try:
            time.sleep(0.200)
            currentReg = int( self._pi.i2c_read_word_data(self._handle, self._INA226_REG_CURRENT) ) #_INA226_REG_CURRENT).byteSwapped ) # return as Int16
            float_current = float(currentReg) * self._currentLSBs
        except:
            print(f'EXCEPTION reading current value')
            return '? Amps'
        return '{:.1f} Amps'.format(float_current)
        

    def voltage(self):
        if not self._available:
            return '? Volts'
        try:
            time.sleep(0.200)
            voltageReg = int( self._pi.i2c_read_word_data(self._handle, self._INA226_REG_BUS_VOLTAGE) ) #_INA226_REG_BUS_VOLTAGE).byteSwapped ) # return as Int16
            float_volts = float(voltageReg) * 0.00125
        except:
            print(f'EXCEPTION reading voltage value')
            return '? Volts'
        return '{:.1f} Volts'.format(float_volts)

    def cancel(self):
        time.sleep(0.200)
        self._pi.i2c_close(self._handle)

_pa_current_sensor = None

def configure_current_sensors(pi):
    global _pa_current_sensor
    _pa_current_sensor = INA226Reader(pi, PA_CURRENT_ADDRESS, PA_CURRENT_SHUNT_OHM, PA_CURRENT_MAX_AMP)

def shutdown_current_sensors():
    _pa_current_sensor.cancel()

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
