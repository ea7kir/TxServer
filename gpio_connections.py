import pigpio

pi = pigpio.pi() # TODO: need to close ? # TODO: move to main()

# INA226 current/voltage sensors
# To discover I2C devices
# $ sudo i2cdetect -y 1
#
# self.supply5v  = INA226(i2c: i2cs[1], address: 0x40, shuntOhm: 0.002, maxAmp: 5)
# self.supply12v = INA226(i2c: i2cs[1], address: 0x41, shuntOhm: 0.002, maxAmp: 5)
# self.supply28v = INA226(i2c: i2cs[1], address: 0x42, shuntOhm: 0.002, maxAmp: 10)
PA_CURRENT_VOLTAGE_SENSOR       = 0 # I2C pin3 GPIO2 SDA, pin 5 GPIO3 SCL

# fan
ENCLOSURE_INTAKE_FAN_ADDRESS    = 6  # pin 31 GPIO_6
ENCLOSURE_EXTRACT_FAN_ADDRESS   = 13 # pin 33 GPIO_13
PA_INTAKE_FAN_ADDRESS           = 19 # pin 35 GPIO_19
PA_EXTRACT_FAN_ADDRESS          = 26 # pin 37 GPIO_26

# DS18820 temerature sensors
# Sset the slave ID for each DS18B20 TO-92 device
# To find those available, type: cd /sys/bus/w1/devices/
# and look for directors named like: 28-3c01d607d440
# these are the names to enter here
# $ /sys/bus/w1/devices/
TEMPERATURE_SENSOR_PIN          = 4  # pin 7  GPIO_4
PA_SENSOR_SLAVE_ID              = '28-3c01d607e348' # pin 7 GPIO_4
PREAMP_SENSOR_SLAVE_ID          = '28-3c01d607d440' # pin 7 GPIO_4

# relay
RELAY_28v_PIN                   = 36 # pin 36 GPIO16
RELAY_12v_PIN                   = 38 # pin 38 GPIO20
RELAY_5v_PIN                    = 40 # pin 40 GPIO21
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
