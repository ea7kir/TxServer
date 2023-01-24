import pigpio

RELAY_28v_PIN   = 1 # TODO: what pin to use
RELAY_12v_PIN   = 2  
RELAY_5v_PIN    = 3

ON = 0  # TODO: int or bool?
OFF = 1

# pi = pigpio.pi() # TODO: need to close ?

# pi.set_mode(RELAY_28v_PIN, pigpio.OUTPUT)
# pi.set_mode(RELAY_12v_PIN, pigpio.OUTPUT)
# pi.set_mode(RELAY_5v_PIN, pigpio.OUTPUT)

def _switch_relay(pin, state):
    pass
    # pi.write(pin, state)

def switch_28v_On():
    _switch_relay(RELAY_28v_PIN, ON)

def switch_28v_Off():
    _switch_relay(RELAY_28v_PIN, OFF)

def switch_12v_On():
    _switch_relay(RELAY_12v_PIN, ON)

def switch_12v_Off():
    _switch_relay(RELAY_12v_PIN, OFF)

def switch_5v_On():
    _switch_relay(RELAY_5v_PIN, ON)

def switch_5v_Off():
    _switch_relay(RELAY_5v_PIN, OFF)
