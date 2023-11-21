#!/usr/bin/python3
from sense_hat import SenseHat

# import paho.mqtt.client as mqtt
import os, sys, json, time

if __name__ == "__main__":
    sense = SenseHat()
    try:
        
        # Credit to yaab-arduino.blogspot.com for this formula, which measures temperature from the
        # sensehat but also takes CPU temperature into account for a slightly more accurate reading.
        temp_room = round(
            (
                (
                    sense.get_temperature_from_pressure()
                    + sense.get_temperature_from_humidity()
                )
                / 2
            ),
            1,
        )
        temp_room_str = str(temp_room)
        temp_cpu = round(
            float(
                os.popen("vcgencmd measure_temp")
                .readline()
                .replace("temp=", "")
                .replace("'C\n", "")
            ),
            1,
        )
        temp_cpu_str = str(temp_cpu)
        # calculates the real temperature compesating CPU heating
        temp_avg = round(temp_room - ((temp_cpu - temp_room)/1.5), 1)
        temp_avg_str = str(temp_avg)
        humidity = round(sense.get_humidity(), 1)
        humidity_str = str(humidity)
        pressure = round(sense.get_pressure(), 2)
        pressure_str = str(pressure)
        json_str = (
            '{ "temperature_avg": '
            + temp_avg_str
            + ', "temperature_room": '
            + temp_room_str
            + ', "temperature_cpu": '
            + temp_cpu_str
            + ', "pressure": '
            + pressure_str
            + ', "humidity": '
            + humidity_str
            + "}"
        )
    except KeyboardInterrupt as exc:
        print("KeyboardException, quitting...")
        print(exc)
    except BaseException as ex:
        print("UnknownException, quitting...", ex)
        print("Stop")
    finally:
        print(result)
    # end
