import pigpio
import time
from device_constants import ENCLOSURE_INTAKE_FAN_GPIO, ENCLOSURE_EXTRACT_FAN_GPIO
from device_constants import PA_INTAKE_FAN_GPIO, PA_EXTRACT_FAN_GPIO

class FanReader:
   """
   A class to read speedometer pulses and calculate the RPM.
   Derived from: https://abyz.me.uk/rpi/pigpio/code/read_RPM_py.zip
   """
   def __init__(self, pi, gpio, pulses_per_rev=2.0, weighting=0.0, min_RPM=1000.0):
      """
      Instantiate with the Pi and gpio of the RPM signal
      to monitor.

      Optionally the number of pulses for a complete revolution
      may be specified.  It defaults to 1.

      Optionally a weighting may be specified.  This is a number
      between 0 and 1 and indicates how much the old reading
      affects the new reading.  It defaults to 0 which means
      the old reading has no effect.  This may be used to
      smooth the data.

      Optionally the minimum RPM may be specified.  This is a
      number between 1 and 1000.  It defaults to 5.  An RPM
      less than the minimum RPM returns 0.0.
      """
      self.pi = pi
      self.gpio = gpio
      self.pulses_per_rev = pulses_per_rev

      if min_RPM > 1000.0:
         min_RPM = 1000.0
      elif min_RPM < 1.0:
         min_RPM = 1.0

      self.min_RPM = min_RPM

      self._watchdog = 200 # Milliseconds.

      if weighting < 0.0:
         weighting = 0.0
      elif weighting > 0.99:
         weighting = 0.99

      self._new = 1.0 - weighting # Weighting for new reading.
      self._old = weighting       # Weighting for old reading.

      self._high_tick = None
      self._period = None

      pi.set_mode(gpio, pigpio.INPUT)

      self._cb = pi.callback(gpio, pigpio.RISING_EDGE, self._cbf)
      pi.set_watchdog(gpio, self._watchdog)

   def _cbf(self, gpio, level, tick):

      if level == 1: # Rising edge.

         if self._high_tick is not None:
            t = pigpio.tickDiff(self._high_tick, tick)

            if self._period is not None:
               self._period = (self._old * self._period) + (self._new * t)
            else:
               self._period = t

         self._high_tick = tick

      elif level == 2: # Watchdog timeout.

         if self._period is not None:
            if self._period < 2000000000:
               self._period += (self._watchdog * 1000)

   def RPM(self):
      """
      Returns the RPM.
      """
      RPM = 0.0
      if self._period is not None:
         RPM = 60000000.0 / (self._period * self.pulses_per_rev)
         if RPM < self.min_RPM:
            RPM = 0.0

      return RPM

   def cancel(self):
      """
      Cancels the fan_reader and releases resources.
      """
      self.pi.set_watchdog(self.gpio, 0) # cancel watchdog
      self._cb.cancel()

_enclosure_intake_reader = None
_enclosure_extract_reader = None
_pa_intake_reader = None
_pa_extract_reader = None

def configure_fan_sensors(pi):
    global _enclosure_intake_reader, _enclosure_extract_reader, _pa_intake_reader, _pa_extract_reader
    _enclosure_intake_reader = FanReader(pi, ENCLOSURE_INTAKE_FAN_GPIO)
    _enclosure_extract_reader = FanReader(pi, ENCLOSURE_EXTRACT_FAN_GPIO)
    _pa_intake_reader = FanReader(pi, PA_INTAKE_FAN_GPIO)
    _pa_extract_reader = FanReader(pi, PA_EXTRACT_FAN_GPIO)

def shutdown_fan_sensors():
    _enclosure_intake_reader.cancel()
    _enclosure_extract_reader.cancel()
    _pa_intake_reader.cancel()
    _pa_extract_reader.cancel()

def read_fan_status():
    #print(f'enc int {int(_enclosure_intake_reader.RPM())} enc ext {int(_enclosure_extract_reader.RPM())} pa int {int(_pa_intake_reader.RPM())} pa ext {int(_pa_extract_reader.RPM())}')
    a = '?';  b = '?'; c = '?'; d = '?'
    if _enclosure_intake_reader.RPM() > 1500:      a = '1'
    if _enclosure_extract_reader.RPM() > 1500:     b = '2'
    if _pa_intake_reader.RPM() > 1500:             c = '3'
    if _pa_extract_reader.RPM() > 1500:            d = '4'
    return a + b + c + d

if __name__ == '__main__':
    pi_outside = pigpio.pi()
    configure_fan_sensors(pi_outside)
    for i in range(1, 10):
        status = read_fan_status()
        print(status)
        time.sleep(1)
    shutdown_fan_sensors()
    pi_outside.stop()
