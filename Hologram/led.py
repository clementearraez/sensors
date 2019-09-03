import RPi.GPIO as gpio
import time
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(13, gpio.OUT)


while True:
 gpio.output(13, True)
 time.sleep(0.2)
 
 gpio.output(13, False)
 time.sleep(0.2)
