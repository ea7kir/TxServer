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

def arm_for_tx():
    print("SWITCHING ON POWER SUPPLIES", flush=True)
    switch_5v_On()
    switch_28v_On()
    switch_12v_On()

def disarm_for_tx():
    print("SWITCHING OFF POWER SUPPLIES", flush=True)
    switch_28v_Off()
    switch_5v_Off()
    switch_12v_Off()

def process_roof_data(pipe):
    request = pipe.recv()
    print(f'process_roof_data got {request} from conn2', flush=True)

    roof_data = RoofData()
    roof_data.preamp_temp = read_preamp_temperature()
    roof_data.pa_temp:str = read_pa_temperature()
    roof_data.pa_current:str = read_pa_current()
    roof_data.fans = read_fan_status()
    sleep(1)

    print('process_roof_data will send to conn2', flush=True)
    pipe.send(roof_data)
    


