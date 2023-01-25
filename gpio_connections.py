import pigpio

pi = pigpio.pi() # TODO: need to close ?

# current sensors
PA_CURRENT_VOLTAGE_SENSOR       = 0

# fan sensores
ENCLOSURE_INTAKE_FAN_ADDRESS    = 1
ENCLOSURE_EXTRACT_FAN_ADDRESS   = 2
PA_INTAKE_FAN_ADDRESS           = 3
PA_EXTRACT_FAN_ADDRESS          = 4

# temerature sensors
PA_SENSOR_ADDRESS               = 'abc'
PREAMP_SENSOR_ADDRESS           = 'def'

# relay pins
RELAY_28v_PIN                   = 1 # TODO: what pin to use
RELAY_12v_PIN                   = 2  
RELAY_5v_PIN                    = 3

# relay logic
GPIO_ON                         = 0  # TODO: int or bool?
GPIO_OFF                         = 1

