from sense_hat import SenseHat
import time

sense = SenseHat()

number = [
1,1,1,1, # Zero
1,0,0,1,
1,0,0,1,
1,0,1,1,
0,0,1,0, # One
0,1,1,0,
0,0,1,0,
0,1,1,1,
0,1,1,1, # Two
0,0,1,1,
0,1,1,0,
0,1,1,1,
1,1,1,1, # Three
0,0,1,1,
0,0,1,1,
1,1,1,1,
0,1,0,1, # Four
0,1,1,1,
0,0,0,1,
0,0,0,1,
0,1,1,1, # Five
0,1,1,0,
0,0,1,1,
0,1,1,1,
0,1,0,0, # Six
0,1,1,1,
0,1,0,1,
0,1,1,1,
0,1,1,1, # Seven
0,0,0,1,
0,0,1,0,
0,1,0,0,
0,1,1,1, # Eight
0,1,1,1,
0,1,1,1,
0,1,1,1,
0,1,1,1, # Nine
0,1,0,1,
0,1,1,1,
0,0,0,1
]
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

# Ejemplo de uso: mostrar la letra 'A' en color rojo
#show_character('A', (255, 0, 0))

def show_message(text, rgb):
    first = True
    for char in text:
        show_character(char, rgb, first)
        time.sleep(1)  # Espera un segundo antes de mostrar el siguiente carácter
        sense.clear()  # Limpia la pantalla entre cada carácter
        first = False
celcius_color = [0,255,0] # Red
fahrenheit_color = [0,255,0] # Green
negative_celcius_color = [0,255,255] # Cyan
negative_fahrenheit_color = [0,0,255] # Blue
empty = [0,0,0] # Black

display = [
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0
]
while True:
    sense.low_light = False
    #sense.load_image("space.png")
    celcius = int(round(sense.get_temperature()))
    show_message(str(celcius), [0, 128, 0])
    #show_character(str(int(celcius/10)), [0, 128, 0])
    #time.sleep(1)
    #sense.clear()
    #show_character(str(int(celcius%10)), [0, 128, 0])
    time.sleep(1)
    
    # Display the temperatures
    #sense.set_pixels(display)
    #sense.load_image("space.png")
    #time.sleep(5)
    sense.low_light = True
    sense.load_image('space.png')
    time.sleep(5)
