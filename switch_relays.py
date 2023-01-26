import pigpio
from gpio_connections import *

def init_relays():
    pi.set_mode(RELAY_28v_PIN, pigpio.OUTPUT)
    pi.set_mode(RELAY_12v_PIN, pigpio.OUTPUT)
    pi.set_mode(RELAY_5v_PIN, pigpio.OUTPUT)

def _switch_relay(pin, state):
    return
    pi.write(pin, state)

def switch_28v_On():
    print("SWITCHING ON 28v")
    _switch_relay(RELAY_28v_PIN, RELAY_ON)

def switch_28v_Off():
    print("SWITCHING OFF 28v")
    _switch_relay(RELAY_28v_PIN, RELAY_OFF)

def switch_12v_On():
    print("SWITCHING ON 12v")
    _switch_relay(RELAY_12v_PIN, RELAY_ON)

def switch_12v_Off():
    print("SWITCHING OFF 12v")
    _switch_relay(RELAY_12v_PIN,RELAY_OFF)

def switch_5v_On():
    print("SWITCHING ON 5v")
    _switch_relay(RELAY_5v_PIN, RELAY_ON)

def switch_5v_Off():
    print("SWITCHING OFF 5v")
    _switch_relay(RELAY_5v_PIN, RELAY_OFF)
