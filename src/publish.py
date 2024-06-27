#!/usr/bin/python3
import datetime
import json
import os
from struct import Struct
import sys
import time
from typing import Dict
import ssl
#from aiohttp import JsonPayload, Payload
import paho.mqtt.client
from paho.mqtt.client import MQTTMessageInfo, Client
from paho.mqtt.client import MQTTMessage
#from pydantic import Json
from sensehatdevice import SenseHatDevice


def load_configuration() -> Dict[str, str | Dict[str, str]]:
    """
    Load the configuration from the 'config.json' file.

    Returns
    -------
    Dict[str, str | Dict[str, str]]
    """
    # Get the path to the config file
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

    # Check if the config file exists
    if not os.path.exists(cfg_path):
        sys.stderr.write("Configuration file " + cfg_path + " not found.\n")
        sys.exit(1)

    # Load the configuration from the file
    content = "{}"
    with open(cfg_path, "r", encoding="utf-8") as fp:
        content = fp.read()
        if content == "":
            sys.stderr.write("Configuration file " + cfg_path + " is empty.\n")
            sys.exit(1)

    init_config = json.loads(content)
    return init_config


def validate_configuration(init_config: Dict[str, str | Dict[str, str]]):
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


def build_mqtt() -> paho.mqtt.client.Client:
    """
    Builds and configures an MQTT client.

    Returns
    -------
    paho.mqtt.client.Client
        The configured MQTT client.
    """
    # Generate a ClientId
    client_id_alt = str(cfg["id"])  # type: ignore

    # Load TLS certificate and key
    # tls_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH, cafile="../ca.crt")
    # tls_context.load_cert_chain(certfile="../server.crt", keyfile="../server.key", password="majestic")
    # Build the MQTT client with the generated client id, clean session, and TCP transport
    build_client = paho.mqtt.client.Client(client_id="sensehat")
    # Set username and password for authentication
    username = cfg["broker"]["username"]
    password = cfg["broker"]["password"]
    if("" not in password):
        build_client.username_pw_set(username, password)
    # Configure TLS
    if (cfg["client"]["certfile"] != ""):
        build_client.tls_insecure_set(True)
        build_client.tls_set(
            certfile=cfg["client"]["certfile"],
            keyfile=cfg["client"]["keyfile"],
            keyfile_password=cfg["client"]["keyfile_password"],
            ca_certs=cfg["client"]["ca_certs"],
            tls_version=ssl.PROTOCOL_TLSv1_2,
        )
    
    # Configure MQTT client callbacks
    
    build_client.on_connect = on_connect
    build_client.on_message = on_message
    #build_client.on_subscribe = on_subscribe
    return build_client


def error_code_message(rc):
    if rc is int:
        return {
            0: "Connection successful",
            1: "Connection refused - incorrect protocol version",
            2: "Connection refused - invalid client identifier",
            3: "Connection refused - server unavailable",
            4: "Connection refused - bad username or password",
            5: "Connection refused - not authorised",
            6 - 255: "undefined",
        }[rc]

    return rc


def print_info(client, userdata, rc, log_header) -> None:
    """
    Print the clientId from a paho.mqtt.client object.

    Args:
        client: The paho.mqtt.client object.

    Returns:
        None

    Parameters
    ----------
    client
    userdata
    log_header
    rc
    """
    if client is paho.mqtt.client.Client:
        print(f"[{log_header}] Client: {client._host} - {client._client_id}")

    print(f"[{log_header}] UserData: {userdata}")
    if rc is MQTTMessage:
        print(f"[{log_header}] Message id: {rc.mid}")
        print(f"[{log_header}] Topic: {rc.topic}")
        print(f"[{log_header}] Qos: {rc.qos}")
        print(f"[{log_header}] Retain: {rc.retain}")
        print(f"[{log_header}] Message payload: {rc.payload.decode()}")
    else:
        if rc is int(0):
            print(f"[{log_header}] ResultCode: {rc} - {error_code_message(rc)}")
        else:
            print(f"[{log_header}] Unknown rc: {rc}")


def on_connect(client: paho.mqtt.client.Client, userdata, flags, rc: int):
    if rc == int(0):
        print("[on_connect] Connected al broker MQTT")
        print_info(client, userdata, rc, "on_connect")
        # Suscribirse a un tema específico
        # mqtt_client.subscribe("homeassistant/status")
        # print("[on_connect] Subscribed to homeassistant/status topic.")
        # mqtt_client.subscribe("homeassistant/nodered/status")
        # print("[on_connect] Subscribed to homeassistant/nodered/status topic.")
        online_topic = cfg["id"] + cfg["topics"]["availability"]
        client.publish(online_topic, "online")
        mqtt_client.publish(online_topic, "online")
        print("[on_connect] Published to " + online_topic+ " topic.")
        mqtt_client.publish(cfg["topics"]["pressure"] + cfg["topics"]["config"], json.dumps(sensehat_device.message_config_pressure("pressure")))
        print(
            "[on_connect] Published to "
            + cfg["topics"]["pressure"]
            + cfg["topics"]["config"]
            + " topic."
        )
        mqtt_client.publish(cfg["topics"]["humidity"] + cfg["topics"]["config"],json.dumps(sensehat_device.message_config_humidity("humidity")), qos=1, retain=True)
        print(
            f"[on_connect] Published to "
            + cfg["topics"]["humidity"]
            + cfg["topics"]["config"]
            + " topic."
        )
        mqtt_client.publish(
            cfg["topics"]["temperature"] + cfg["topics"]["config"],
            json.dumps(sensehat_device.message_config_temperature("temperature"))
        )
        print(
            f"[on_connect] Published to "
            + cfg["topics"]["temperature"]
            + cfg["topics"]["config"]
            + " topic."
        )
    # elif rc != int(0) and rc[0] != int(0):
    #     print(f"[on_connect] Connection error. Return Code: {error_code_message(rc)}")
    #else:
        # print(
        #     f"[on_connect] Unexpected Result Code: is int: {rc is int} - {type(rc)} {rc}"
        # )


# Function to handle the connection with the broker MQTT
def on_subscribe(client, userdata, flags, rc: int):
    print("[on_subscribe] On Subscribe event! Sending configurations!")
    print_info(client, userdata, rc, "on_subscribe")
    if rc == int(0) or rc[0] == int(0):
        mqtt_client.publish(
            cfg["topics"]["pressure"] + cfg["topics"]["config"],
            json.dumps(sensehat_device.message_config_pressure("pressure"))
        )
        print(
            "[on_subscribe] Published to "
            + cfg["topics"]["pressure"]
            + cfg["topics"]["config"]
            + " topic."
        )
        mqtt_client.publish(
            cfg["topics"]["humidity"] + cfg["topics"]["config"],
            json.dumps(sensehat_device.message_config_humidity("humidity"))
            
        )
        print(
            f"[on_subscribe] Published to "
            + cfg["topics"]["humidity"]
            + cfg["topics"]["config"]
            + " topic."
        )
        mqtt_client.publish(
            cfg["topics"]["temperature"] + cfg["topics"]["config"],
            json.dumps(sensehat_device.message_config_temperature("temperature"))
        )
        print(
            f"[on_subscribe] Published to "
            + cfg["topics"]["temperature"]
            + cfg["topics"]["config"]
            + " topic."
        )
        mqtt_client.publish(
            cfg["id"] + cfg["topics"]["config"],
            json.dumps(sensehat_device.define_sensehat_device())
        )
        print(
            f"[on_subscribe] Published to "
            + cfg["id"]
            + cfg["topics"]["config"]
            + " topic."
        )
    # elif rc != int(0) or rc[0] != int(0):
    #     print(f"[on_subscribe] WARNING: Result Code: {error_code_message(rc)}")
    else:
        print(f"[on_subscribe] Unexpected Result Code: {type(rc)} {rc}")


# Función para manejar la recepción de mensajes MQTT
def on_message(client, userdata, msg):
    print_info(client, userdata, msg, "on_message")
    print(f"[on_message] Topic: {msg.topic}")
    print(f"[on_message] Qos: {msg.qos}")
    print(f"[on_message] Retain: {msg.retain}")
    print(f"[on_message] Message received: {msg.payload.decode()}")


def publish(
    client: paho.mqtt.client.Client,
    topic: str,
    msg: str,
    retain: bool = False,
    qos: int = 0,
) -> MQTTMessageInfo:
    msg_count = 1
    while True:
        result = client.publish(topic, msg, retain=retain, qos=qos)

        if result.rc == 0 or result.is_published():
            print(
                f"[publish] Message {result.mid}: `{msg}` to topic `{topic}` published."
            )
            return result
        print(
            f"[publish] Failed to send message to topic {topic}. Message: {result.mid} - Code: {result.rc}"
        )
        msg_count += 1
        if msg_count > 5:
            print(
                f"[publish] Timeout while retrying... #{msg_count} - Message: {result.mid} - Code: {result.rc}"
            )
            break
        print(
            f"[publish] Retrying... #{msg_count} - Message: {result.mid} - Code: {result.rc}"
        )
        time.sleep(1)
    return result


def mqtt_connect(param_client: paho.mqtt.client.Client) -> paho.mqtt.client.Client:
    """
    Connects the MQTT client to the broker and publishes an "online" message.

    Args:
        param_client: The MQTT client object.

    Returns:
        The connected MQTT client object.
    """
    topic = cfg["id"] + cfg["topics"]["availability"]
    # param_client.will_clear()
    param_client.will_set(topic, "offline")
    print(f"[mqtt_connect] Will set to topic {topic} with message 'offline'")
    # Connect to the MQTT broker
    
    param_client.connect(
        cfg["broker"]["host"], port=cfg["broker"]["port"], keepalive=60
    )
    # Publish an "online" message
    print(f"[mqtt_connect] Connected to {cfg['broker']['host']}:{cfg['broker']['port']}")
    print(f"[mqtt_connect] Username: {cfg['broker']['username']}")
    
    info = param_client.publish(topic, "online");
    
    #MQTTMessageInfo
    if info.is_published():
        print(f"[mqtt_connect] Message sent to topic {topic} with message 'online'")
    else:
        print(f"[mqtt_connect] Message failed to topic {topic} with message 'online'")
    
    dev = sensehat_device.define_sensehat_device();
    topic_disco = cfg["id"] + "/config";
    discovery = param_client.publish(topic_disco, json.dumps(dev));
    if discovery.is_published():
        print(f"[mqtt_connect] Message sent to topic {topic_disco} with device info")
    else:
        print(f"[mqtt_connect] Message failed to topic {topic_disco} with device info")
        print(f"[mqtt_connect] {json.dumps(dev)}");

    
    return param_client


def run():
    """
    Run the main function.

    This function performs the following steps:
    1. Loads the configuration using the `load_configuration()` function.
    2. Validates the loaded configuration using the `validate_configuration()` function.
    3. Builds an MQTT client using the `build_mqtt()` function.
    4. Retrieves the refresh interval from the configuration and converts it to an integer.
    5. Initializes a `SenseHatDevice` object using the loaded configuration.
    6. Connects to the MQTT broker using the `mqtt_connect()` function.
    7. Starts the MQTT client loop using the `mqtt_client.loop_start()` function.
    8. Enters an infinite loop to continuously read sensor data and publish it to the MQTT broker.
    9. Handles keyboard interrupts and other exceptions gracefully.
    10. Stops the MQTT client loop and disconnects from the MQTT broker.
    11. Prints the current time and exits.

    Parameters:
    - None

    Return:
    - None
    """
    exit_code = 0
    seconds = int(cfg["seconds"])
    # print(f"Starting sense-hat-mqtt. Warming up during 15 seconds.")
    # time.sleep(15)  # Allow time for sense-hat to warm up and avoid erroneous data
    current_time = datetime.datetime.now()
    print(current_time)
    print(f"Starting sense-hat-mqtt. Refreshing every {seconds} seconds")

    try:
        counter = 1
        sensehat_device.show_message(f"{counter}")
        mqtt_connect(mqtt_client)
        mqtt_client.loop_start()
        #mqtt_client.loop_forever()
        while True:
            mqtt_client.reconnect()
            counter = counter + 1
            metrics = sensehat_device.calculate_metrics()
            json_read = metrics["messages"]["json"]
            print(f"[{datetime.datetime.now()}] Reading: {json_read}")
            # print(f"[DEBUG]: {json.dumps(metrics)}")
            publish(
                mqtt_client,
                cfg["topics"]["humidity"] + cfg["topics"]["state"],
                metrics["humidity"],
                retain=False,
            )
            time.sleep(0.25)
            publish(
                mqtt_client,
                cfg["topics"]["pressure"] + cfg["topics"]["state"],
                metrics["pressure"],
                retain=False,
            )
            time.sleep(0.25)
            publish(
                mqtt_client,
                cfg["topics"]["temperature"] + cfg["topics"]["state"],
                metrics["temp_room"],
                retain=False,
            )
            time.sleep(0.25)
            publish(
                mqtt_client,
                cfg["topics"]["temp_cpu"] + cfg["topics"]["state"],
                metrics["temp_cpu"],
                retain=False,
            )
            print(f"Sleeping for {seconds} seconds.")
            time.sleep(seconds)
    except KeyboardInterrupt as exc:
        print("KeyboardException, quitting...")
        print(exc)
    except ConnectionResetError as cre:
        print("Connection error, sleeping...", cre)
        print(f"Ex Type: {type(cre)}")
        # sys.stderr.write(f"Exception: {cre}\n")
        exit_code = 8
    except BaseException as exx:
        print("UnknownException, quitting...", exx)
        print(f"Ex Type: {type(exx)}")
        sys.stderr.write(f"Exception: {exx}\n")
        exit_code = 1
        print("Stop")
    finally:
        # client.disconnect()
        # Cerrar la conexión con el broker MQTT
        print("Quitting...Closing loop and connection...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        current_time = datetime.datetime.now()
        print(f"[{current_time}] Exit! Done!")
        
    return exit_code

cfg = load_configuration()
validate_configuration(cfg)
mqtt_client: Client = build_mqtt()

try:
    sensehat_device = SenseHatDevice(cfg)
except BaseException as ex:
    print("SenseHat device initialization failed, quitting...", ex)
    # print(ex.with_traceback())
    print(f"Ex Type: {type(ex)}")
    sys.stderr.write(f"Exception: {ex}\n")
    #sys.stderr.write(f"Traceback: {ex.with_traceback()}\n")
    print("Stop")
    sys.exit(1)

if __name__ == "__main__":
    # Main Program
    ec = run()
    while ec == 8:
        time.sleep(300)
        ec = run()
    
    
    sys.exit(ec)

    # end
