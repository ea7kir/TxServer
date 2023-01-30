import pigpio
from time import sleep

from device_temperatures import configure_temperature_sensors, shutdown_temperature_sensors
from device_temperatures import read_pa_temperature, read_preamp_temperature
from device_fans import configure_fan_sensors, shutdown_fan_sensors, read_fan_status
from device_currents import configure_current_sensors, shutdown_current_sensors, read_pa_current
from device_relays import configure_relays, shutdown_relays
from device_relays import switch_28v_On, switch_28v_Off
from device_relays import switch_12v_On, switch_12v_Off
from device_relays import switch_5v_On, switch_5v_Off

class ServerData:
    preamp_temp = '-'
    pa_temp = '-'
    pa_current = '-'
    fans = '-'

_pi = None

def congifure_devices():
    global _pi
    _pi = pigpio.pi()
    configure_relays(_pi)
    configure_current_sensors(_pi)
    configure_temperature_sensors(_pi)
    configure_fan_sensors(_pi)

def shutdown_devices():
    shutdown_relays()
    shutdown_fan_sensors()
    shutdown_current_sensors()
    shutdown_temperature_sensors()
    _pi.stop()

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


