from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
sense.clear()
sense.show_message('Hi')
while True:
    temp = (sense.get_temperature())
    temp = round(temp, 1)
    message = str(temp)
    sense.show_message(message)
    sleep (10)
