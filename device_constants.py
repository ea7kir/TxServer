# constants

# TODO: install i2c-tools
# sudo apt install -y i2c-tools
# TODO: enable I2C in config

# There's an INA266 C library at https://github.com/MarioAriasGa/raspberry-pi-ina226

# INA226 current/voltage sensors
# To discover I2C devices
# $ sudo i2cdetect -y 1
# TODO: address could be 0x40, 0x41 or 0x42
PA_CURRENT_ADDRESS              = 0x40 # I2C pin3 GPIO2 SDA, pin 5 GPIO3 SCL
PA_CURRENT_SHUNT_OHM            = 0.002
PA_CURRENT_MAX_AMP              = 10

# fan sensors
ENCLOSURE_INTAKE_FAN_GPIO       = 6  # pin 31 GPIO_6
ENCLOSURE_EXTRACT_FAN_GPIO      = 13 # pin 33 GPIO_13
PA_INTAKE_FAN_GPIO              = 19 # pin 35 GPIO_19
PA_EXTRACT_FAN_GPIO             = 26 # pin 37 GPIO_26

# DS18820 temerature sensors
# Sset the slave ID for each DS18B20 TO-92 device
# To find those available, type: cd /sys/bus/w1/devices/
# and look for directors named like: 28-3c01d607d440
# these are the names to enter here
# $ /sys/bus/w1/devices/
TEMPERATURE_SENSOR_GPIO         = 4  # pin 7  GPIO_4
PA_SENSOR_SLAVE_ID              = '28-3c01d607e348' # pin 7 GPIO_4
PREAMP_SENSOR_SLAVE_ID          = '28-3c01d607d440' # pin 7 GPIO_4

# Waveshare RPi Relay Board
RELAY_28v_GPIO                  = 26 # pin 37 GPIO_26 (CH1 P25)
RELAY_12v_GPIO                  = 20 # pin 38 GPIO_20 (CH2 P28)
RELAY_5v_GPIO                   = 21 # pin 40 GPIO_21 (CH3 P29)
# NOTE: the opto coupleers need reverse logic
RELAY_ON                        = 0  # TODO: int or bool?
RELAY_OFF                       = 1

# SatServer used...
# RELAY_0 = 17 # pin 11 # Relay 0 - AC to Psu12v Contactor
# RELAY_1 = 27 # pin 13 # Relay 1 - AC to Psu28v Contactor
# RELAY_2 = 22 # pin 15 # Relay 2 - 5v to RX Pi
# RELAY_3 = 10 # pin 19 # Relay 3 - 12v to Pluto Fan, Driver Fan, PA LH Fan, PA RH Fan
# RELAY_4 = 9  # pin 21 # Relay 4 - 5v to Pluto Vcc
# RELAY_5 = 11 # pin 23 # Relay 5 - 5v to Driver Vcc (PTT)
# RELAY_6 = 5  # pin 29 # Relay 6 - 28v to PA Bias (PTT)
# RELAY_7 = 6  # pin 31 # Relay 7 - reserved
# 
# RELAY_OFF = 1 # note: the opto coupleers need reverse logic
# RELAY_ON = 0
