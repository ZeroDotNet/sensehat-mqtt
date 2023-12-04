import os
import datetime

from sense_hat import SenseHat


class SenseHatDevice:
    def __init__(self, config):
        """
        Initializes a new instance of the class with the provided configuration.

        Parameters:
            config (object): The configuration object.

        Returns:
            None

        Parameters
        ----------
        config

        Returns
        -------
        SenseHatDevice
        """
        self.sense = SenseHat()
        #self.sense.show_message(config["id"])
        self.sense.show_message("Starting")
        self.sense.clear()
        self.cfg = config

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

    def message_config_humidity(self, sensor) -> object:
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
            "availability_topic": self.cfg["topics"][sensor]
            + self.cfg["topics"]["availability"],
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

    def message_config_pressure(self, sensor):
        """Generate a message configuration for the pressure sensor.

        Parameters
        ----------
        sensor
        """
        message = {
            "device_class": "pressure",
            "availability_topic": self.cfg["topics"][sensor]
            + self.cfg["topics"]["availability"],
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

    def message_config_temperature(self, sensor):
        """Generate a message configuration for the temperature sensor.

        Parameters
        ----------
        sensor
        """
        message = {
            "device_class": "temperature",
            "availability_topic": self.cfg["topics"][sensor]
            + self.cfg["topics"]["availability"],
            "state_topic": self.cfg["topics"][sensor] + self.cfg["topics"]["state"],
            "unit_of_measurement": "°C",
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

    def message_config_cpu_temperature(self, sensor):
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
            "availability_topic": self.cfg["topics"][sensor]
            + self.cfg["topics"]["availability"],
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

    def calculate_metrics(self) -> dict[str, float | dict[str, str]] | None:
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
            + ', timestamp: "' + str(current_time) + '" }'
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
            "timestamp": current_time
        }
        return result
