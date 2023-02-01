import pigpio
from time import sleep
from device_constants import PA_CURRENT_ADDRESS, PA_CURRENT_SHUNT_OHM, PA_CURRENT_MAX_AMP
from math import floor
_pi = None
_i2c_bus = None
_handle = None

_INA226_TIME_8MS = 7 # 8.244ms # :UInt8
_INA226_AVERAGES_16 = 2 # :UInt8
_INA226_MODE_SHUNT_BUS_CONTINUOUS = 7 # :UInt8
_INA226_REG_BUS_VOLTAGE = 0x02 # :UInt8
_INA226_REG_CURRENT = 0x04 # :UInt8

_currentLSBs = 0.0

def _config_INA226(address, shunt_ohm, max_amp):
    global _handle
    i2c_flags = 0
    _handle = _pi.i2c_open(_i2c_bus, address, i2c_flags)
    print(f'handel is {_handle}')

    # reset
    INA226_REG_CONFIGURATION = 0x00 # :UInt8
    INA226_RESET = 0x8000 # :UInt16
    _pi.i2c_write_word_data(_handle, INA226_REG_CONFIGURATION, INA226_RESET)

    # configure
    INA226_REG_CALIBRATION = 0x05 # UInt8
    INA226_REG_CONFIGURATION = 0x00 # UInt8
    bus = _INA226_TIME_8MS
    shunt = _INA226_TIME_8MS
    average = _INA226_AVERAGES_16
    mode = _INA226_MODE_SHUNT_BUS_CONTINUOUS

    # calibrate
    currentLSBs = max_amp / float(1 << 15) # max_current / (1 << 15)
    calib: float = 0.00512 / (currentLSBs * shunt_ohm)
    calibReg = int(floor(calib)) # :UInt16
    currentLSBs = 0.00512 / (shunt_ohm * float(calibReg)) # 0.00512 / (r_shunt * calib_reg)
    _pi.i2c_write_word_data(_handle, INA226_REG_CALIBRATION, calibReg) #calibReg.byteSwapped)

    # configure
    configReg = (int(average) << 9) | (int(bus) << 6) | (int(shunt) << 3) | int(mode)
    _pi.i2c_write_word_data(_handle, INA226_REG_CONFIGURATION, configReg) #configReg.byteSwapped)

def configure_current_sensors(pi):
    global _pi, _i2c_bus
    _pi = pi
    _i2c_bus = 1
    _config_INA226(PA_CURRENT_ADDRESS, PA_CURRENT_SHUNT_OHM, PA_CURRENT_MAX_AMP)

def shutdown_current_sensors():
    _pi.i2c_close(_handle)

def _read_sensor(address):
    # read voltage
    voltageReg = int( _pi.i2c_read_word_data(_handle, _INA226_REG_BUS_VOLTAGE) ) #_INA226_REG_BUS_VOLTAGE).byteSwapped ) # return as Int16
    float_volts = float(voltageReg) * 0.00125
    sleep(0.001)
    #read current
    currentReg = int( _pi.i2c_read_word_data(_handle, _INA226_REG_CURRENT) ) #_INA226_REG_CURRENT).byteSwapped ) # return as Int16
    float_current = float(currentReg) * _currentLSBs
    # format
    amps = '{:.1f} Amps'.format(float_current)
    volts = '{:.1f} Volts'.format(float_volts)
    return amps, volts

def read_pa_current():
    return _read_sensor(PA_CURRENT_ADDRESS)

def _read_INA266(address): # returns (current, voltage)
    float_current = 1.23
    float_voltage = 27.89
    return '{:.1f} Amps'.format(float_current), '{:.1f} Volts'.format(float_voltage)


if __name__ == '__main__':
    pi_outside = pigpio.pi()
    configure_current_sensors(pi_outside)
    current, voltage = read_pa_current()
    print(current, voltage)
    shutdown_current_sensors()
