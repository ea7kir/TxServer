# import gpio

RELAY_28v_ADDRESS   = 1
RELAY_12v_ADDRESS   = 2  
RELAY_5v_ADDRESS    = 3

ON = 0
OFF = 1

def _switch_relay(address, state):
    pass

def switch_28v_On():
    _switch_relay(RELAY_28v_ADDRESS, ON)

def switch_28v_Off():
    _switch_relay(RELAY_28v_ADDRESS, OFF)

def switch_12v_On():
    _switch_relay(RELAY_12v_ADDRESS, ON)

def switch_12v_Off():
    _switch_relay(RELAY_12v_ADDRESS, OFF)

def switch_5v_On():
    _switch_relay(RELAY_5v_ADDRESS, ON)

def switch_5v_Off():
    _switch_relay(RELAY_5v_ADDRESS, OFF)
