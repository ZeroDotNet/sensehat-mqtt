#!/usr/bin/env python

import RPi.GPIO as GPIO
from colorama import Fore
import time
from sense_hat import SenseHat
from datetime import datetime

# SenseHat display
sense = SenseHat()
sense.low_light = True
sense.show_message("Starting", scroll_speed=0.05)
# Clear the SenseHat display
# self.sense.clear()

pir_sensor = 33 #13 # 11 #17 # antes era 6.

piezo = 29 #5 # antes era el 7

GPIO.setmode(GPIO.BOARD)

GPIO.setup(piezo,GPIO.OUT)

GPIO.setup(pir_sensor, GPIO.IN)


def show_character(char, rgb, first=True):
     # Define el color RGB
     r, g, b = rgb

     # Establece el color del texto y el color de fondo (negro por defecto)
     text_colour = [r, g, b]
     back_colour = [255, 255, 255]
     if first == True and  char == '3':
         back_colour = [128, 0, 0]

     # Usa la función show_letter para mostrar un único carácter
     sense.show_letter(char, text_colour=text_colour, back_colour=back_colour)

current_state = 0
print(Fore.BLUE + "Hola!")
counter = 0
last_value = 0
try:

    while True:

        time.sleep(1)
        current_state = GPIO.input(pir_sensor)
        if current_state != last_value:
            last_value = current_state
            if current_state == 1:

                #print("GPIO pin %s is %s" % (pir_sensor, current_state))
                counter = counter + 1
                print(Fore.RED + str(datetime.now()) + " - Movimiento detectado! (" + str(counter) + ")")
                # sense.show_message(str(counter))
                # show_character(str(counter), [255, 255, 255], True)
                sense.show_message(str(counter), text_colour=[255, 0, 0], scroll_speed=0.5)
                GPIO.output(piezo, GPIO.HIGH)


                # time.sleep(1)

                # GPIO.output(piezo,False)

                # time.sleep(0.1)
            else:
                GPIO.output(piezo, 0)
                print(Fore.GREEN + "Sin Movimiento " + str(datetime.now()))
                # time.sleep(1)
            time.sleep(1)

except KeyboardInterrupt:
    print(Fore.GREEN + "Adios")
    pass

finally:
    sense.clear()
    GPIO.cleanup()


