import RPi.GPIO as GPIO
from time import sleep
import config

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(config.led['red'], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(config.led['blue'], GPIO.OUT, initial=GPIO.LOW)

while True: # Run forever
  GPIO.output(config.led['red'], GPIO.HIGH) # Turn on
  GPIO.output(config.led['blue'], GPIO.LOW) # Turn off
  sleep(1) # Sleep for 1 second
  GPIO.output(config.led['red'], GPIO.LOW) # Turn off
  GPIO.output(config.led['blue'], GPIO.HIGH) # Turn on
  sleep(1) # Sleep for 1 second
