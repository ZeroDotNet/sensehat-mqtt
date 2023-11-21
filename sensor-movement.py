#!/usr/bin/env python

import RPi.GPIO as GPIO
from colorama import Fore
import time

pir_sensor = 11 #17 # antes era 6.

piezo = 29 #5 # antes era el 7

GPIO.setmode(GPIO.BOARD)

GPIO.setup(piezo,GPIO.OUT)

GPIO.setup(pir_sensor, GPIO.IN)

current_state = 0
print(Fore.BLUE + "Hola!")
try:

    while True:

        time.sleep(0.1)

        current_state = GPIO.input(pir_sensor)

        if current_state == 1:

            print("GPIO pin %s is %s" % (pir_sensor, current_state))
            print(Fore.RED + "Movimiento detectado")

            GPIO.output(piezo,True)

            time.sleep(2)

            GPIO.output(piezo,False)

            time.sleep(0.1)

except KeyboardInterrupt:
    print(Fore.GREEN + "Adios")
    pass

finally:

    GPIO.cleanup()
