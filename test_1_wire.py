import pigpio
from time import sleep

from device_constants import PA_SENSOR_SLAVE_ID, PREAMP_SENSOR_SLAVE_ID

pi = pigpio.pi()

if not pi.connected:
    print('pi not connected')
    exit()

def _read_DS18B20(address):
    temperatute = '-'
    #pigpio.exceptions = False
    try:
        sensor = '/sys/bus/w1/devices/' + address + '/w1_slave'
        h = pi.file_open(sensor, pigpio.FILE_READ)
        c, data = pi.file_read(h, 1000) # 1000 is plenty to read full file.
        pi.file_close(h)
        """
        Typical file contents
        73 01 4b 46 7f ff 0d 10 41 : crc=41 YES
        73 01 4b 46 7f ff 0d 10 41 t=23187
        """
        # NOTE: ti get this working, I needed to convert str to byte objects
        if b'YES' in data:
            (discard, sep, reading) = data.partition(b' t=')
            temp = float(reading) / 1000.0
            temperatute = '{:.1f}'.format(temp)
    except:
        pass
    #pigpio.exceptions = True
    return temperatute

if __name__ == '__main__':
    temp = _read_DS18B20(PREAMP_SENSOR_SLAVE_ID)
    print(temp)