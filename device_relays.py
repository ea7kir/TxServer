import pigpio

from device_constants import RELAY_ON, RELAY_OFF
from device_constants import RELAY_28v_GPIO, RELAY_12v_GPIO, RELAY_5v_GPIO

_pi = None

def _switch_relay(gpio, state):
    _pi.write(gpio, state)

def _config_relay(gpio):
    _pi.set_mode(gpio, pigpio.OUTPUT)
    _pi.write(gpio, RELAY_OFF)

def configure_relays(pi):
    global _pi
    _pi = pi
    _config_relay(RELAY_28v_GPIO)
    _config_relay(RELAY_12v_GPIO)
    _config_relay(RELAY_5v_GPIO)

def shutdown_relays():
    _switch_relay(RELAY_28v_GPIO, RELAY_OFF)
    _switch_relay(RELAY_12v_GPIO, RELAY_OFF)
    _switch_relay(RELAY_5v_GPIO, RELAY_OFF)

def switch_28v_On():
    print("SWITCHING ON 28v")
    _switch_relay(RELAY_28v_GPIO, RELAY_ON)

def switch_28v_Off():
    print("SWITCHING OFF 28v")
    _switch_relay(RELAY_28v_GPIO, RELAY_OFF)

def switch_12v_On():
    print("SWITCHING ON 12v")
    _switch_relay(RELAY_12v_GPIO, RELAY_ON)

def switch_12v_Off():
    print("SWITCHING OFF 12v")
    _switch_relay(RELAY_12v_GPIO,RELAY_OFF)

def switch_5v_On():
    print("SWITCHING ON 5v")
    _switch_relay(RELAY_5v_GPIO, RELAY_ON)

def switch_5v_Off():
    print("SWITCHING OFF 5v")
    _switch_relay(RELAY_5v_GPIO, RELAY_OFF)
