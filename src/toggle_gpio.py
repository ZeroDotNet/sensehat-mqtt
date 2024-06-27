 import RPi.GPIO as GPIO
 import time
 import sys

 # Function to toggle GPIO port
 def toggle_gpio_port(port, interval):
     GPIO.setmode(GPIO.BCM)
     GPIO.setup(port, GPIO.OUT)

     try:
         while True:
             # Turn on GPIO port
             GPIO.output(port, True)
             time.sleep(interval)
             # Turn off GPIO port
             GPIO.output(port, False)
             time.sleep(interval)
     except KeyboardInterrupt:
         # Clean up GPIO on CTRL+C exit
         GPIO.cleanup()
     GPIO.cleanup()  # Clean up GPIO on normal exit

 if __name__ == "__main__":
     if len(sys.argv) != 3:
         print("Usage: python3 toggle_gpio.py <GPIO port #> <interval_in_seconds>")
         sys.exit(1)

     port = int(sys.argv[1])
     interval = float(sys.argv[2])
     toggle_gpio_port(port, interval)
