import pigpio
from device_constants import RELAY_ON, RELAY_OFF
from device_constants import RELAY_28v_GPIO, RELAY_12v_GPIO, RELAY_5v_GPIO

import logging

class RelaySwitcher():
    """
    A class to switch a relay on and off.
    """
    def __init__(self, pi, gpio):
        self.pi = pi
        self.gpio = gpio
        self.pi.set_mode(self.gpio, pigpio.OUTPUT)
        #_pi.set_pad_strength(2, 14) # Set pad 2 to 14 mA.
        self.pi.write(gpio, RELAY_OFF)

    def switch_on(self):
        self.pi.write(self.gpio, RELAY_ON)

    def switch_off(self):
        self.pi.write(self.gpio, RELAY_OFF)

    def cancel(self):
        self.pi.write(self.gpio, RELAY_OFF)

_relay_28v = None
_relay_12v = None
_relay_5v = None

def configure_relays(pi):
    global _relay_28v, _relay_12v, _relay_5v
    _relay_28v = RelaySwitcher(pi, RELAY_28v_GPIO)
    _relay_12v = RelaySwitcher(pi, RELAY_12v_GPIO)
    _relay_5v = RelaySwitcher(pi, RELAY_5v_GPIO)

def shutdown_relays():
    _relay_28v.cancel()
    _relay_12v.cancel()
    _relay_5v.cancel()

def switch_28v_On():
    logging.info('28v PSU goes ON')
    _relay_28v.switch_on()

def switch_28v_Off():
    logging.info('28v PSU goes off')
    _relay_28v.switch_off()

def switch_12v_On():
    logging.info('12v PSU goes ON')
    _relay_12v.switch_on()

def switch_12v_Off():
    logging.info('12v PSU goes OFF')
    _relay_12v.switch_off()

def switch_5v_On():
    logging.info('5v PSU goes ON')
    _relay_5v.switch_on()

def switch_5v_Off():
    logging.info('5v PSU goes OFF')
    _relay_5v.switch_off()
