#!/usr/bin/python3
from sense_hat import SenseHat

# import paho.mqtt.client as mqtt
from paho.mqtt import client as mqtt, publish, subscribe, subscribeoptions, properties
import os, sys, json, time, datetime

cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
if not (os.path.exists(cfg_path)):
    sys.stderr.write("Configuration file " + cfg_path + " not found.\n")
    sys.exit(1)
fp = open(cfg_path, "r")
cfg = json.load(fp)
fp.close()

if not ("id" in cfg):
    sys.stderr.write("No 'id' field in configuration.\n")
    sys.exit(1)
if not ("broker" in cfg):
    sys.stderr.write("No 'broker' field in configuration.\n")
    sys.exit(1)
if not ("topics" in cfg):
    sys.stderr.write("No 'topics' field in configuration.\n")
    sys.exit(1)
if not ("seconds" in cfg):
    sys.stderr.write("No 'seconds' field in configuration.\n")
    sys.exit(1)


# Función para manejar la conexión con el broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[on_connect] Conectado al broker MQTT")
        #print(client)
        #print(userdata)
        #print(flags)
        #print(rc)
        client.subscribe("homeassistant/status")  # Suscribirse a un tema específico
        print("[on_connect] Subscribed to homeassistant/status topic.")
        
        #client.publish(cfg["topics"]["pressure"] + "/" + cfg["topics"]["config"], json.dumps(message_config_pressure("pressure")))
        #print("[on_connect] Published to "+ cfg["topics"]["pressure"] + "/" + cfg["topics"]["config"] +" topic.")

        #client.publish(cfg["topics"]["humidity"] + "/" + cfg["topics"]["config"], json.dumps(message_config_humidity("humidity")))
        #print(f"[on_connect] Published to " + cfg["topics"]["humidity"] + "/" + cfg["topics"]["config"] + " topic.")
        
        #client.publish(cfg["topics"]["temperature"] + "/" + cfg["topics"]["config"], json.dumps(message_config_temperature("temperature")))
        #print(f"[on_connect] Published to " + cfg["topics"]["temperature"] + "/" + cfg["topics"]["config"] + " topic.")
        
    else:
        print("[on_connect] Connection error. Code: ", rc)

# Función para manejar la conexión con el broker MQTT
def on_subscribe(client, userdata, flags, rc):
    #if rc == 0:
        print("[on_subscribe] Conectado al broker MQTT")
        print(client)
        print(userdata)
        print(flags)
        print(rc)
                
        client.publish(cfg["topics"]["pressure"] + "/" + cfg["topics"]["config"], json.dumps(message_config_pressure("pressure")))
        print("[on_subscribe] Published to "+ cfg["topics"]["pressure"] + "/" + cfg["topics"]["config"] +" topic.")

        client.publish(cfg["topics"]["humidity"] + "/" + cfg["topics"]["config"], json.dumps(message_config_humidity("humidity")))
        print(f"[on_subscribe] Published to " + cfg["topics"]["humidity"] + "/" + cfg["topics"]["config"] + " topic.")
        
        client.publish(cfg["topics"]["temperature"] + "/" + cfg["topics"]["config"], json.dumps(message_config_temperature("temperature")))
        print(f"[on_subscribe] Published to " + cfg["topics"]["temperature"] + "/" + cfg["topics"]["config"] + " topic.")
        
    #else:
     #   print("[on_subscribe] Connection error. Code: ", rc)

def message_config_pressure(sensor):
    message = {
        "device_class": "pressure",
        "state_topic": cfg["topics"][sensor] + "/" + cfg["topics"]["state"],
        "unit_of_measurement": "hPa",
        #"value_template": "{{ value_json.humidity }}",
        "unique_id": "pre01rpi",
        "device" : {
            "identifiers": "sensehat01rpi",
            "name": "SenseHat",
            "sw_version": "1.0",
            "model": "Raspberry Pi 4 Model B+",
            "manufacturer": "Raspberry Pi Foundation"
        }
    }

    return message
def message_config_humidity(sensor):
    message = {
        "device_class": "humidity",
        "state_topic": cfg["topics"][sensor] + "/" + cfg["topics"]["state"],
        "unit_of_measurement": "%",
        #"value_template": "{{ value_json.humidity }}",
        "unique_id": "hum01rpi",
        "device" : {
            "identifiers": "sensehat01rpi",
            "name": "SenseHat",
            "sw_version": "1.0",
            "model": "Raspberry Pi 4 Model B+",
            "manufacturer": "Raspberry Pi Foundation"
        }
    }

    return message

def message_config_temperature(sensor):
    #client.publish(cfg["topics"]["humidity"], humidity_str)
    message = {

        "device_class": "temperature",
        "state_topic": cfg["topics"][sensor] + "/" + cfg["topics"]["state"],
        "unit_of_measurement": "°C",
        #"value_template": "{{ value_json.temperature }}",
        "unique_id": "temp01rpi",
        "device" : {
            "identifiers": "sensehat01rpi",
            "name": "SenseHat",
            "sw_version": "1.0",
            "model": "Raspberry Pi 4 Model B+",
            "manufacturer": "Raspberry Pi Foundation"
        }
    }

    return message
# Función para manejar la recepción de mensajes MQTT
def on_message(client, userdata, msg):
    print("[on_message] Client: ", client)
    print("[on_message] UserData: ", userdata)
    print("[on_message] Message received: " + msg.payload.decode())


# Configuración del cliente MQTT
# client = mqtt.Client("cliente_mqtt")  # Crea una instancia del cliente MQTT
client = mqtt.Client(cfg["id"])
# Configuración de los callbacks del cliente MQTT
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

if __name__ == "__main__":
    sense = SenseHat()
    seconds = int(cfg["seconds"])
    # print(f"Starting sensehat-mqtt. Warming up during 15 seconds.")
    # time.sleep(15)  # Allow time for sensehat to warm up and avoid erroneous data
    current_time = datetime.datetime.now()
    print(current_time)
    print(f"Starting sensehat-mqtt. Refreshing every {seconds} seconds")
    # Conexión al broker MQTT
    # client.connect(broker_address, 1883)  # Conectarse al broker en el puerto 1883
    #client.connect(cfg["broker"]["host"], port=cfg["broker"]["port"])
    # Bucle principal para mantener la conexión y procesar los mensajes
    #client.loop_start()

    try:
        client.connect(cfg["broker"]["host"], port=cfg["broker"]["port"])
        
        while True:
            client.loop_start()
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
            # client.connect(cfg['broker']['host'], port=cfg['broker']['port'])
            print(f"[{datetime.datetime.now()}] Reading: \n{json_str}\n")
            client.publish(cfg["topics"]["json"], json_str)
            #time.sleep(0.25)
            client.publish(cfg["topics"]["humidity"] + "/" + cfg["topics"]["state"], humidity_str)
            #time.sleep(0.25)
            client.publish(cfg["topics"]["pressure"] + "/" + cfg["topics"]["state"], pressure_str)
            #time.sleep(0.25)
            client.publish(cfg["topics"]["temperature"] + "/" + cfg["topics"]["state"], temp_room_str)
            #time.sleep(0.25)
            client.publish(cfg["topics"]["temp_room"], temp_room_str)
            #time.sleep(0.25)
            client.publish(cfg["topics"]["cpu"], temp_cpu)
            #time.sleep(0.25)
            client.publish(cfg["topics"]["temp_cpu"], temp_cpu_str)
            #time.sleep(0.25)
            client.publish(cfg["topics"]["temp_avg"], temp_avg_str)
            time.sleep(seconds)
    except KeyboardInterrupt as exc:
        print("KeyboardException, quitting...")
        print(exc)
    except BaseException as ex:
        print("UnknownException, quitting...", ex)
        print("Stop")
    finally:
        # client.disconnect()
        # Cerrar la conexión con el broker MQTT
        print("Quitting...Closing loop and connection...")
        client.loop_stop()
        client.disconnect()
        current_time = datetime.datetime.now()
        print(current_time)
        print("Done!")

    # end
