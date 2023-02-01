import pigpio
from time import sleep
from device_constants import PA_CURRENT_ADDRESS, PA_CURRENT_SHUNT_OHM, PA_CURRENT_MAX_AMP

# INA266 converted from Swift
# All available constants
#
# INA226_REG_CONFIGURATION: UInt8         = 0x00
# INA226_REG_SHUNT_VOLTAGE: UInt8         = 0x01
# INA226_REG_BUS_VOLTAGE: UInt8           = 0x02
# INA226_REG_POWER: UInt8                 = 0x03
# INA226_REG_CURRENT: UInt8               = 0x04
# INA226_REG_CALIBRATION: UInt8           = 0x05
# INA226_REG_MASK_ENABLE: UInt8           = 0x06
# INA226_REG_ALERT_LIMIT: UInt8           = 0x07
# INA226_REG_MANUFACTURER: UInt8          = 0xFE
# INA226_REG_DIE_ID: UInt8                = 0xFF
#
# INA226_RESET: UInt16                    = 0x8000
# INA226_MASK_ENABLE_CVRF: UInt16         = 0x0008
#
# INA226_BIT_SHUNT                        = 0
# INA226_BIT_BUS                          = 1
# INA226_BIT_MODE                         = 2
#
# INA226_MODE_SHUNT: UInt8                = 1
# INA226_MODE_BUS: UInt8                  = 2
# INA226_MODE_TRIGGERED: UInt8            = 0
# INA226_MODE_CONTINUOUS: UInt8           = 4
#
# INA226_MODE_OFF: UInt16                 = 0
# INA226_MODE_SHUNT_TRIGGERED: UInt16     = 1
# INA226_MODE_BUS_TRIGGERED: UInt16       = 2
# INA226_MODE_SHUNT_BUS_TRIGGERED: UInt16 = 3
# INA226_MODE_OFF2: UInt16                = 4
# INA226_MODE_SHUNT_CONTINUOUS: UInt16    = 5
# INA226_MODE_BUS_CONTINUOUS: UInt16      = 6
# INA226_MODE_SHUNT_BUS_CONTINUOUS: UInt8 = 7
#
# INA226_TIME_01MS: UInt8                 = 0 # 140us
# INA226_TIME_02MS: UInt8                 = 1 # 204us
# INA226_TIME_03MS: UInt8                 = 2 # 332us
# INA226_TIME_05MS: UInt8                 = 3 # 588us
# INA226_TIME_1MS: UInt8                  = 4 # 1.1ms
# INA226_TIME_2MS: UInt8                  = 5 # 2.115ms
# INA226_TIME_4MS: UInt8                  = 6 # 4.156ms
# INA226_TIME_8MS: UInt8                  = 7 # 8.244ms
#
# INA226_AVERAGES_1: UInt8                = 0
# INA226_AVERAGES_4: UInt8                = 1
# INA226_AVERAGES_16: UInt8               = 2
# INA226_AVERAGES_64: UInt8               = 3
# INA226_AVERAGES_128: UInt8              = 4
# INA226_AVERAGES_256: UInt8              = 5
# INA226_AVERAGES_512: UInt8              = 6
# INA226_AVERAGES_1024: UInt8             = 7

_i2c = None #: I2CInterface
_address: int = 0
_shuntOhm: float = 0
_maxAmp: float = 0
_reachable = False
_currentLSBs: float = 0
_configured = False

_INA226_TIME_8MS = 7 # 8.244ms # :UInt8
_INA226_AVERAGES_16 = 2 # :UInt8
_INA226_MODE_SHUNT_BUS_CONTINUOUS = 7 # :UInt8
_INA226_REG_BUS_VOLTAGE = 0x02 # :UInt8
_INA226_REG_CURRENT = 0x04 # :UInt8

private_var_volts: float = 0.0
private_var_amps: float = 0.0

def init(i2c, address: int, shuntOhm: float, maxAmp: float):
    global _i2c, _address, _shuntOhm, _maxAmp
    _i2c = i2c
    _address = address
    _shuntOhm = shuntOhm
    _maxAmp = maxAmp

def supply(): # returns str
    global _reachable, _configured
    if not _configured:
        _reachable = _i2c.isReachable(_address)
        if _reachable:
            reset(_address)
            configure(_address, _shuntOhm, _maxAmp,
                      _INA226_TIME_8MS,
                      _INA226_TIME_8MS,
                      _INA226_AVERAGES_16,
                      _INA226_MODE_SHUNT_BUS_CONTINUOUS)
            _configured = True
    if _reachable and _configured:
        # read_word(_i2c, command) -> Int16
        voltageReg = int( _i2c.readWord(_address, _INA226_REG_BUS_VOLTAGE).byteSwapped ) # return as Int16
        volts = float(voltageReg) * 0.00125
        sleep(0.001)
        # read_word(_i2c, command) -> Int16
        currentReg = int( _i2c.readWord(_address, _INA226_REG_CURRENT).byteSwapped ) # return as Int16
        amps = float(currentReg) * _currentLSBs
    else:
        volts = 0.0
        amps = 0.0
    return '{:.1f} Amps'.format(amps), '{:.1f} Volts'.format(volts)

def reset(address: int):
    INA226_REG_CONFIGURATION = 0x00 # :UInt8
    INA226_RESET = 0x8000 # :UInt16
    # write_word(address, command, value)
    _i2c.writeWord(address, INA226_REG_CONFIGURATION, INA226_RESET.byteSwapped)


def configure(address: int, shuntOhm: float, maxAmp: float, bus, shunt, average, mode):
                                        # bus: UInt8, shunt: UInt8, average: UInt8, mode: UInt8
    INA226_REG_CALIBRATION = 0x05 # UInt8
    INA226_REG_CONFIGURATION = 0x00 # UInt8
    # Calibrate
    currentLSBs = maxAmp / float(1 << 15) # max_current / (1 << 15)
    calib: float = 0.00512 / (currentLSBs * shuntOhm)
    calibReg = int(floor(calib)) # :UInt16
    currentLSBs = 0.00512 / (shuntOhm * float(calibReg)) # 0.00512 / (r_shunt * calib_reg)
    # write_word(address, command, value)
    _i2c.writeWord(address, INA226_REG_CALIBRATION, calibReg.byteSwapped)
    # Configure
    #configReg = (UInt16(average) << 9) | (UInt16(bus) << 6) | (UInt16(shunt) << 3) | UInt16(mode)
    configReg = (int(average) << 9) | (int(bus) << 6) | (int(shunt) << 3) | init(mode)
    # write_word(address, command, value)
    _i2c.writeWord(address, INA226_REG_CONFIGURATION, configReg.byteSwapped)


if __name__ == '__main__':
    pi = pigpio.pi()
    # handle = pi.i2c_open(i2c_bus, i2c_address, i2c_flags)
    #i2c = pi.i2c_open()
    init (1, PA_CURRENT_ADDRESS, PA_CURRENT_SHUNT_OHM, PA_CURRENT_MAX_AMP)
    I, V = supply()
    print(I, V)
