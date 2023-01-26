from time import sleep

from read_temperature_sensors import configure_temperature_sensors, shutdown_temperature_sensors
from read_temperature_sensors import read_pa_temperature, read_preamp_temperature
from read_fan_status import configure_fan_sensors, shutdown_fan_sensors, read_fan_status
from read_current_sensor import configure_current_sensors, shutdown_current_sensors, read_pa_current
from switch_relays import configure_relays, shutdown_relays
from switch_relays import switch_28v_On, switch_28v_Off
from switch_relays import switch_12v_On, switch_12v_Off
from switch_relays import switch_5v_On, switch_5v_Off

class ServerData:
    preamp_temp:str = ''
    pa_temp: str = ''
    pa_current: str = ''
    fans: str = ''

def congifure_devices(pi):
    configure_relays(pi)
    configure_current_sensors(pi)
    configure_temperature_sensors(pi)
    configure_fan_sensors(pi)

def shutdown_devices():
    shutdown_relays()
    shutdown_fan_sensors()
    shutdown_current_sensors()
    shutdown_temperature_sensors()

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


