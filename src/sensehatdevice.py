"""
Represents a SenseHat device and provides methods to calculate various metrics.
:copyright: (c) 2022-present Dan Rodrigues
:license: MIT, see LICENSE for more details.
"""
from operator import concat

from typing import Dict
import datetime
import os
import sys
from xml.sax import default_parser_list
from sense_hat import SenseHat


class SenseHatDevice:
    """
    Represents a SenseHat device and provides methods to calculate various metrics.
    """
    

    def __init__(self, config: Dict[str, str | Dict[str, str]] | None):
        """
        Initializes a new instance of the class with the provided configuration.

        Parameters:
            config (object): The configuration object.

        Returns:
            None
        """

        def validate_configuration(init_config: Dict[str, str] | None):
            """
            Validate the configuration to ensure it has all the required fields.
            """
            # Check if 'id' field exists
            if "id" not in init_config:
                sys.stderr.write("No 'id' field in configuration.\n")
                sys.exit(1)

            # Check if 'broker' field exists
            if "broker" not in init_config:
                sys.stderr.write("No 'broker' field in configuration.\n")
                sys.exit(1)

            # Check if 'topics' field exists
            if "topics" not in init_config:
                sys.stderr.write("No 'topics' field in configuration.\n")
                sys.exit(1)

            # Check if 'seconds' field exists
            if "seconds" not in init_config:
                sys.stderr.write("No 'seconds' field in configuration.\n")
                sys.exit(1)

        # Store the configuration object
        self.cfg = config
        validate_configuration(self.cfg)

        # Initialize the SenseHat device
        self.sense = SenseHat()

        # Show a message on the SenseHat display
        # self.sense.show_message("Starting")

        # Clear the SenseHat display
        self.sense.clear()

    def get_temperature(self):
        """
        Get the temperature using the `sense` object.

        Returns:
            The temperature as a float.
        """
        return self.sense.get_temperature()

    def get_humidity(self):
        """Get the humidity value from the SenseHat sensor."""
        return self.sense.get_humidity()

    def get_pressure(self):
        """Get the pressure value from the SenseHat sensor."""
        return self.sense.get_pressure()

    def message_config_humidity(self, sensor) -> Dict[str, str | Dict[str, str]]:
        """Generate a message configuration for the humidity sensor.

        Parameters
        ----------
        sensor

        Returns
        -------
        object
        """
        message = {
            "device_class": "humidity",
            "availability_topic": self.cfg["id"] + self.cfg["topics"]["availability"],
            "state_topic": self.cfg["topics"][sensor] + self.cfg["topics"]["state"],
            "unit_of_measurement": "%",
            "icon": "mdi:water-percent",
            "name": "Humidity",
            "unique_id": "hum01rpi",
            "device": {
                "identifiers": "sensehat01rpi",
                "name": "SenseHat",
                "sw_version": "1.0",
                "model": "Raspberry Pi 4 Model B+",
                "manufacturer": "Raspberry Pi Foundation",
            },
        }
        return message

    def message_config_pressure(self, sensor) -> Dict[str, str]:
        """Generate a message configuration for the pressure sensor.

        Parameters
        ----------
        sensor
        """
        message = {
            "device_class": "pressure",
            "availability_topic": self.cfg["id"] + self.cfg["topics"]["availability"],
            "state_topic": self.cfg["topics"][sensor] + self.cfg["topics"]["state"],
            "unit_of_measurement": "hPa",
            "icon": "mdi:axis-arrow",
            "name": "Pressure",
            "unique_id": "pre01rpi",
            "device": {
                "identifiers": "sensehat01rpi",
                "name": "SenseHat",
                "sw_version": "1.0",
                "model": "Raspberry Pi 4 Model B+",
                "manufacturer": "Raspberry Pi Foundation",
            },
        }
        return message

    def message_config_temperature(self, sensor) -> Dict[str, str]:
        """Generate a message configuration for the temperature sensor.

        Parameters
        ----------
        sensor
        """
        message = {
            "device_class": "temperature",
            "availability_topic": self.cfg["id"] + self.cfg["topics"]["availability"],
            "state_topic": self.cfg["topics"][sensor] + self.cfg["topics"]["state"],
            "unit_of_measurement": "°C",
            "state_class": "measurement",
            "temperature_unit": "C",
            "icon": "mdi:temperature-celsius",
            "name": "Temperature",
            "unique_id": "temp01rpi",
            "device": {
                "identifiers": "sensehat01rpi",
                "name": "SenseHat",
                "sw_version": "1.0",
                "model": "Raspberry Pi 4 Model B+",
                "manufacturer": "Raspberry Pi Foundation",
            },
        }
        return message

    def message_config_cpu_temperature(self, sensor) -> Dict[str, str]:
        """
        Generates a message configuration for CPU temperature sensor.

        Args:
            sensor (str): The name of the sensor.

        Returns:
            dict: A dictionary containing the message configuration for CPU temperature sensor.

        Parameters
        ----------
        sensor

        """
        message = {
            "device_class": "temperature",
            "availability_topic": self.cfg["id"] + self.cfg["topics"]["availability"],
            "state_topic": self.cfg["topics"][sensor] + self.cfg["topics"]["state"],
            "unit_of_measurement": "°C",
            "temperature_unit": "C",
            "entity_category": "measurement",
            "icon": "mdi:temperature-celsius",
            # "state_class": "measurement",
            "name": "CPU Temperature",
            "object_id": "sensehat.sensor.cpu.temperature",
            # "value_template": "{{ value_json.temperature }}",
            "unique_id": "cputemp01rpi",
            "device": {
                "identifiers": "sensehat01rpi",
                "name": "SenseHat",
                "sw_version": "1.0",
                "model": "Raspberry Pi 4 Model B+",
                "manufacturer": "Raspberry Pi Foundation",
            },
        }
        return message


    def show_message(self, message):
        #self.sense.clear()
        self.sense.show_message(message)

    # create a function to define a device with a few sensors for home assistant by using mqtt discovery feature.
    def define_device(self, device_name: str, device_id: str, availability_topic: str, state_topic: str, device_class: str, unit_of_measurement: str, icon: str, name: str, unique_id: str, model: str, manufacturer: str) -> Dict[str, str | Dict[str, str]]:
        """
        Define a device with multiple sensors for Home Assistant using MQTT discovery feature.

        Args:
            device_name (str): The name of the device.
            device_id (str): The unique ID of the device.
            availability_topic (str): The availability topic of the device.
            state_topic (str): The state topic of the device.
            device_class (str): The class of the device.
            unit_of_measurement (str): The unit of measurement of the device.
            icon (str): The icon of the device.
            name (str): The name of the device.
            unique_id (str): The unique ID of the device.
            model (str): The model of the device.
            manufacturer (str): The manufacturer of the device.

        Returns:
            dict: A dictionary containing the message configuration for the device.
        """
        message = {
            "device_class": device_class,
            "availability_topic": availability_topic,
            "state_topic": state_topic,
            "unit_of_measurement": unit_of_measurement,
            "icon": icon,
            "name": name,
            "unique_id": unique_id,
            "device": {
                "identifiers": device_id,
                "name": device_name,
                "sw_version": "1.0",
                "model": model,
                "manufacturer": manufacturer,
            },
        }
        return message



    def define_sensehat_device(self):
        """
        Define a SenseHat device with multiple sensors for Home Assistant using MQTT discovery feature.
        """
        # Define the configuration for the device
        device_name = "SenseHat"
        device_id = "sensehat01rpi"
        availability_topic = self.cfg["topics"]["device"] + self.cfg["topics"]["availability"]
        model = "Raspberry Pi 4 Model B+"
        manufacturer = "Raspberry Pi Foundation"

        # Define and publish the message configurations for each sensor
        humidity_config = self.define_device(
            device_name=device_name,
            device_id=device_id,
            availability_topic=availability_topic,
            state_topic=self.cfg["topics"]["humidity"] + self.cfg["topics"]["state"],
            device_class="humidity",
            unit_of_measurement="%",
            icon="mdi:water-percent",
            name="Humidity",
            unique_id="hum01rpi",
            model=model,
            manufacturer=manufacturer,
        )
        

        pressure_config = self.define_device(
            device_name=device_name,
            device_id=device_id,
            availability_topic=availability_topic,
            state_topic=self.cfg["topics"]["pressure"] + self.cfg["topics"]["state"],
            device_class="pressure",
            unit_of_measurement="hPa",
            icon="mdi:axis-arrow",
            name="Pressure",
            unique_id="pre01rpi",
            model=model,
            manufacturer=manufacturer,
        )
        
        state_topic =(self.cfg["topics"]["temperature"].join(self.cfg["topics"]["state"])).lower()
        temperature_config = self.define_device(
            device_name=device_name,
            device_id=device_id,
            availability_topic=availability_topic,
            state_topic=state_topic,
            device_class="temperature",
            unit_of_measurement="°C",
            icon="mdi:temperature-celsius",
            name="Temperature",
            unique_id="temp01rpi",
            model=model,
            manufacturer=manufacturer,
        )

        # return an object with the message configurations for each sensors
        return {
            "device_name": device_name,
            "device_id": device_id,
            "availability_topic": availability_topic,
            "model": model,
            "manufacturer": manufacturer,
            "humidity": humidity_config,
            "pressure": pressure_config,
            "temperature": temperature_config
        }
        
            
        
        





    # def calculate_metrics(self) -> dict[str, float | dict[str, str]] | None:
    def calculate_metrics(self) -> Dict[str, str | Dict[str, str]]:
        """
        Calculates various metrics including temperature, humidity, and pressure.

        :return: A dictionary containing the calculated metrics:
                 - 'temp_room': float - the temperature in the room
                 - 'temp_cpu': float - the CPU temperature
                 - 'temp_avg': float - the average temperature compensating for CPU heating
                 - 'humidity': float - the humidity level
                 - 'pressure': float - the air pressure
                 - 'messages': dict - formatted values in JSON format
        """
        # Credit to yaab-arduino.blogspot.com for this formula, which measures temperature from the
        # sense-hat but also takes CPU temperature into account for a slightly more accurate reading.
        temp_room = round(
            number=float(
                (
                        self.sense.get_temperature_from_pressure()
                        + self.sense.get_temperature_from_humidity()
                )
                / 2
            ),
            ndigits=1,
        )
        temp_room_str = str(temp_room)
        temp_cpu = round(
            number=float(
                os.popen("vcgencmd measure_temp")
                .readline()
                .replace("temp=", "")
                .replace("'C\n", "")
            ),
            ndigits=1,
        )
        temp_cpu_str = str(temp_cpu)
        # calculates the real temperature compensating CPU heating
        temp_avg = round(temp_room - ((temp_cpu - temp_room) / 1.5), 1)
        temp_avg_str = str(temp_avg)
        humidity = round(self.sense.get_humidity(), 1)
        humidity_str = str(humidity)
        pressure = round(self.sense.get_pressure(), 2)
        pressure_str = str(pressure)
        current_time = datetime.datetime.now()
        json_str = (
                '{ "avg": '
                + temp_avg_str
                + ', "room": '
                + temp_room_str
                + ', "cpu": '
                + temp_cpu_str
                + ', "pressure": '
                + pressure_str
                + ', "humidity": '
                + humidity_str
                + ', "temperature": '
                + temp_room_str
                + ', timestamp: "'
                + str(current_time)
                + '" }'
        )
        formatted_values = {
            "temp_room": temp_room_str,
            "temp_cpu": temp_cpu_str,
            "temp_avg": temp_avg_str,
            "humidity": humidity_str,
            "pressure": pressure_str,
            "json": json_str,
        }
        result = {
            "temp_room": temp_room,
            "temp_cpu": temp_cpu,
            "temp_avg": temp_avg,
            "humidity": humidity,
            "pressure": pressure,
            "messages": formatted_values,
            "timestamp": current_time,
        }
        return result
