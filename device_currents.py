import pigpio
import time
from math import floor
from device_constants import PA_CURRENT_ADDRESS, PA_CURRENT_SHUNT_OHM, PA_CURRENT_MAX_AMP
#import numpy as np

def byteSwapped(word):
    """ 16 bit word byte swap """
    b1 = word >> 8
    b2 = word & 0xFF
    result = b2 << 8
    result |= b1
    return result

class INA226Reader():
    """
    A class to read an INA266 current/voltage sensor.
    """
    def __init__(self, pi, address, shunt_ohm, max_amp):
        """
        Use 'sudo i2cdetect -y 1' to display the connected I2C devices.
        """
        self.pi = pi
        self.INA226_RESET = 0x8000 # :UInt16
        self.INA226_REG_CALIBRATION = 0x05 # UInt8
        self.INA226_REG_CONFIGURATION = 0x00 # UInt8
        self.INA226_TIME_8MS = 7 # 8.244ms # :UInt8
        self.INA226_AVERAGES_16 = 2 # :UInt8
        self.INA226_MODE_SHUNT_BUS_CONTINUOUS = 7 # :UI
        self.INA226_REG_BUS_VOLTAGE = 0x02 # :UInt8
        self.INA226_REG_CURRENT = 0x04 # :UInt8

        try:
            # Open
            i2c_bus = 1
            self.handle = self.pi.i2c_open(i2c_bus, address) #, i)

            # Reset
            #                                             UInt8                          UInt16
            self.pi.i2c_write_word_data(self.handle, self.INA226_REG_CONFIGURATION, byteSwapped(self.INA226_RESET))

            # Configure
            shunt = self.INA226_TIME_8MS
            average = self.INA226_AVERAGES_16
            mode = self.INA226_MODE_SHUNT_BUS_CONTINUOUS

            self.currentLSBs = max_amp / float(1 << 15)
            calib: float = 0.00512 / (self.currentLSBs * shunt_ohm)
            calibReg = int(floor(calib)) # :UInt16
            self.currentLSBs = 0.00512 / (shunt_ohm * float(calibReg))
            #                                             UInt8                   UInt16
            self.pi.i2c_write_word_data(self.handle, self.INA226_REG_CALIBRATION, byteSwapped(calibReg))

            configReg = (int(average) << 9) | (int(self.INA226_TIME_8MS) << 6) | (int(shunt) << 3) | int(mode)
            #                                             UInt8                     UInt16
            self.pi.i2c_write_word_data(self.handle, self.INA226_REG_CONFIGURATION, byteSwapped(configReg))
            self.available = True
        except:
            print(f'EXCEPTION configuring INA266 at {hex(address)}')
            self.available = False

    def volts_amps(self):
        if not self.available:
            return '? Volts', '? Amps'
        try:
            #                                      UInt16                               UInt8
            voltageReg = byteSwapped( int( self.pi.i2c_read_word_data(self.handle, self.INA226_REG_BUS_VOLTAGE) ) )
            float_volts = float(voltageReg) * 0.00125
            time.sleep(0.001)
            #                                      UInt16                               UInt8
            currentReg = byteSwapped( int( self.pi.i2c_read_word_data(self.handle, self.INA226_REG_CURRENT) ) )
            float_current = float(currentReg) * self.currentLSBs
        except:
            print(f'EXCEPTION reading volts/amps')
            return '? Volts', '? Amps'
        return '{:.1f} Volts'.format(float_volts), '{:.1f} Amps'.format(float_current)
        

    def cancel(self):
        time.sleep(0.200)
        self.pi.i2c_close(self.handle)

_pa_current_sensor = None

def configure_current_sensors(pi):
    global _pa_current_sensor
    _pa_current_sensor = INA226Reader(pi, PA_CURRENT_ADDRESS, PA_CURRENT_SHUNT_OHM, PA_CURRENT_MAX_AMP)

def shutdown_current_sensors():
    _pa_current_sensor.cancel()

def read_pa_current():
    volts, amps = _pa_current_sensor.volts_amps()
    return amps

def read_pa_voltage():
    volts, amps = _pa_current_sensor.volts_amps()
    return volts

if __name__ == '__main__':
#    a = 0x1234
#    b = byteSwapped(a)
#    print(hex(a), hex(b))
#    exit(0)
    pi_outside = pigpio.pi()
    configure_current_sensors(pi_outside)
    for i in range(1, 10):
        volts, amps = _pa_current_sensor.volts_amps()
        print(volts, amps)
        time.sleep(1)
    shutdown_current_sensors()
    pi_outside.stop()
