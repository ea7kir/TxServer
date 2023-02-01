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

# DS18B20 temerature sensors
# Sset the slave ID for each DS18B20 TO-92 device
# To find those available, type: cd /sys/bus/w1/devices/
# and look for directors named like: 28-3c01d607d440
#
# To enable the 1-wire bus add 'dtoverlay=w1-gpio' to /boot/config.txt and reboot.
# For permissions, add '/sys/bus/w1/devices/28*/w1_slave r' to /opt/pigpio/access.
# Default connection is data line to GPIO 4 (pin 7).
# Connect 3V3 or 5V for power, ground to ground.
# 4k7 pull-up on data line to 3V3, and data line to pin 7 GPIO 4.
#TEMPERATURE_SENSOR_GPIO         = 4  # DEFAULT is pin 7  GPIO_4
PA_SENSOR_SLAVE_ID              = '28-3c01d607e348' # pin 7 GPIO_4
PREAMP_SENSOR_SLAVE_ID          = '28-3c01d607d440' # pin 7 GPIO_4

# Waveshare RPi Relay Board
RELAY_28v_GPIO                  = 26 # pin 37 GPIO_26 (CH1 P25)
RELAY_12v_GPIO                  = 20 # pin 38 GPIO_20 (CH2 P28)
RELAY_5v_GPIO                   = 21 # pin 40 GPIO_21 (CH3 P29)
# NOTE: the opto coupleers need reverse logic
RELAY_ON                        = 0
RELAY_OFF                       = 1
