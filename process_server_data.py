from time import sleep

from read_temperature_sensors import read_pa_temperature, read_preamp_temperature
from read_fan_status import read_fan_status
from read_current_sensor import read_pa_current
from switch_relays import switch_28v_On, switch_28v_Off
from switch_relays import switch_12v_On, switch_12v_Off
from switch_relays import switch_5v_On, switch_5v_Off

class ServerData:
    preamp_temp:str = ''
    pa_temp: str = ''
    pa_current: str = ''
    fans: str = ''

def arm_for_tx():
    print("SWITCHING ON POWER SUPPLIES")
    switch_5v_On()
    switch_28v_On()
    switch_12v_On()

def disarm_for_tx():
    print("SWITCHING OFF POWER SUPPLIES")
    switch_28v_Off()
    switch_5v_Off()
    switch_12v_Off()

def read_server_data():
    server_data = ServerData()
    server_data.preamp_temp = read_preamp_temperature()
    server_data.pa_temp:str = read_pa_temperature()
    server_data.pa_current:str = read_pa_current()
    server_data.fans = read_fan_status()
    sleep(1)
    return server_data    


