## Enable 1-wire

```
sudo apt install -y i2c-tools python3-smbus
```

Enable with `sudo raspi-config`

```
sudo reboot
```

Testing

```
sudo i2cdetect -y 1
```

Add `/sys/bus/w1/devices/28*/w1_slave r` to `/opt/pigpio/access`

## Enable I2C

Enable with `sudo raspi-config`
