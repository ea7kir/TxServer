import pigpio
from device_constants import PA_SENSOR_SLAVE_ID, PREAMP_SENSOR_SLAVE_ID

import random # ONLY NEEDED TO SIMULATE DATA VALUES DURING DEVELOPMENT
from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

_pi = None

def _init_DS18B20(slave_id):
    # nothing to do here
    pass
    
def configure_temperature_sensors(pi):
    global _pi
    _pi = pi
    _init_DS18B20(PA_SENSOR_SLAVE_ID)
    _init_DS18B20(PREAMP_SENSOR_SLAVE_ID)

def shutdown_temperature_sensors():
    # nothing to do here
    pass

def _random_read_DS18B20(slave_id):
    float_temperature = random.random() * 30
    txt = '{:.1f} °C'
    return txt.format(float_temperature)

def _read_DS18B20(slave_id):
    sleep(0.1) # allow settling time
    temperature = '-'
    #pigpio.exceptions = False
    try:
        sensor = '/sys/bus/w1/devices/' + slave_id + '/w1_slave'
        h = _pi.file_open(sensor, pigpio.FILE_READ)
        c, data = _pi.file_read(h, 1000) # 1000 is plenty to read full file.
        _pi.file_close(h)
        """
        Typical file contents
        73 01 4b 46 7f ff 0d 10 41 : crc=41 YES
        73 01 4b 46 7f ff 0d 10 41 t=23187
        """
        # NOTE: to get this working, I needed to treat str as byte objects
        if b'YES' in data:
            (discard, sep, reading) = data.partition(b' t=')
            float_temperature = float(reading) / 1000.0
            temperature = '{:.1f} °C'.format(float_temperature)
    except:
        pass
    #pigpio.exceptions = True
    return temperature

def read_pa_temperature():
    return _read_DS18B20(PA_SENSOR_SLAVE_ID)

def read_preamp_temperature():
    return _read_DS18B20(PREAMP_SENSOR_SLAVE_ID)
