from sense_hat import SenseHat

sense = SenseHat()
temp1 = sense.get_temperature_from_pressure()
print("T from Pressure: %s C" % temp1)
temp2 = sense.get_temperature_from_humidity()
print("T from Humidity: %s C" % temp2)
temp3 = sense.get_temperature()
print("T: %s C" % temp3)
tempAvg = round( (temp1 + temp2) / 2, 1)
print("Average T: %s C" % tempAvg)

