import pigpio
import time
from device_constants import PA_SENSOR_SLAVE_ID, PREAMP_SENSOR_SLAVE_ID

class DS18B20Reader:
    """
    A class to read a DS18B20 1-Wire sensor and return a temperature string.
    Derived from: https://abyz.me.uk/rpi/pigpio/code/DS18B20-1_py.zip
    """
    def __init__(self, pi, slave_id):
        """
        This uses the file interface to access the remote file system.

        In this case it is used to access the sysfs 1-wire bus interface
        to read any connected DS18B20 temperature sensors.

        The remote file /opt/pigpio/access is used to grant access to
        the remote file system.

        For this example the file must contain the following line which
        grants read access to DS18B20 device files.

        /sys/bus/w1/devices/28*/w1_slave r
        """
        self.pi = pi
        self.slave_id = slave_id

    def temperature(self):
        time.sleep(0.1) # allow settling time
        temperature = '-'
        #pigpio.exceptions = False
        try:
            sensor = '/sys/bus/w1/devices/' + self.slave_id + '/w1_slave'
            h = self.pi.file_open(sensor, pigpio.FILE_READ)
            c, data = self.pi.file_read(h, 1000) # 1000 is plenty to read full file.
            self.pi.file_close(h)
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

    def cancel(self):
        pass

_preamp_temperature_reader = None
_pa_temperature_reader = None

def configure_temperature_sensors(pi):
    global _preamp_temperature_reader, _pa_temperature_reader
    _preamp_temperature_reader = DS18B20Reader(pi, PREAMP_SENSOR_SLAVE_ID)
    _pa_temperature_reader = DS18B20Reader(pi, PA_SENSOR_SLAVE_ID)

def shutdown_temperature_sensors():
    _preamp_temperature_reader.cancel()
    _pa_temperature_reader.cancel()

def read_preamp_temperature():
    return _preamp_temperature_reader.temperature()

def read_pa_temperature():
    return _pa_temperature_reader.temperature()

if __name__ == '__main__':
    pi_outside = pigpio.pi()
    configure_temperature_sensors(pi_outside)
    for i in range(1, 10):
        t1 = read_preamp_temperature()
        t2 = read_pa_temperature()
        print(t1, t2)
        time.sleep(1)
    shutdown_temperature_sensors()
    pi_outside.stop()
