import pigpio
from gpio_connections import *

def _config_relay(relay):   # TODO: should it be gpio or pin ?
    pi.set_mode(relay, pigpio.OUTPUT)
    pi.write(relay, RELAY_OFF)

def init_relays():
    _config_relay(RELAY_28v_PIN)
    _config_relay(RELAY_12v_PIN)
    _config_relay(RELAY_5v_PIN)

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
