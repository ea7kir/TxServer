from time import sleep

from read_temperature_sensors import read_pa_temperature, read_preamp_temperature
from read_fan_status import read_fan_status
from read_current_sensor import read_pa_current
from switch_relays import switch_28v_On, switch_28v_Off
from switch_relays import switch_12v_On, switch_12v_Off
from switch_relays import switch_5v_On, switch_5v_Off

class RoofData:
    preamp_temp:str = ''
    pa_temp: str = ''
    pa_current: str = ''
    fans: str = ''
    connected: bool = False

def process_roof_data(connection):
    roof_data = RoofData()

    while True:
        roof_data.preamp_temp = read_preamp_temperature()
        roof_data.pa_temp:str = read_pa_temperature()
        roof_data.pa_current:str = read_pa_current()
        roof_data.fans = read_fan_status()
        print('sensors read')
        connection.send(roof_data)
        sleep(1.0)


