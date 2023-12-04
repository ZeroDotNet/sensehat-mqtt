#!/usr/bin/python3
import datetime
import json
import os
import random
import sys
import time
import ssl

# import paho.mqtt.client
from paho.mqtt.client import Client, MQTT_CLEAN_START_FIRST_ONLY
from paho.mqtt.client import MQTTMessageInfo
from paho.mqtt.client import MQTTMessage

# from sensehatdevice import SenseHatDevice
from .sensehatdevice import SenseHatDevice


def load_configuration() -> dict:
    """
    Load the configuration from the 'config.json' file.

    Returns
    -------
    object
    """
    # Get the path to the config file
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

    # Check if the config file exists
    if not os.path.exists(cfg_path):
        sys.stderr.write("Configuration file " + cfg_path + " not found.\n")
        sys.exit(1)

    # Load the configuration from the file
    content = ""
    with open(cfg_path, "r", encoding="utf-8") as fp:
        content = fp.read()
        if content == "":
            sys.stderr.write("Configuration file " + cfg_path + " is empty.\n")
            sys.exit(1)

    init_config = json.loads(content)
    return init_config


def validate_configuration(init_config):
    """
    Validate the configuration to ensure it has all the required fields.
    """
    # Check if 'id' field exists
    if not "id" in init_config:
        sys.stderr.write("No 'id' field in configuration.\n")
        sys.exit(1)

    # Check if 'broker' field exists
    if not "broker" in init_config:
        sys.stderr.write("No 'broker' field in configuration.\n")
        sys.exit(1)

    # Check if 'topics' field exists
    if not "topics" in init_config:
        sys.stderr.write("No 'topics' field in configuration.\n")
        sys.exit(1)

    # Check if 'seconds' field exists
    if not "seconds" in init_config:
        sys.stderr.write("No 'seconds' field in configuration.\n")
        sys.exit(1)


def build_mqtt() -> Client:
    """

    Returns
    -------
    object
    """
    # Configuration del cliente MQTT
    # client = mqtt.Client(cfg["id"])
    # Generate a ClientId
    client_id = f"publish-{random.randint(0, 1000)}"
    # Generate a ClientId
    client_id_alt = str(cfg["id"])  # type: ignore
    tls_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    tls_context.load_cert_chain(certfile="../server.crt", keyfile="../server.key")

    build_client = Client(
        client_id=client_id_alt, clean_session=True, reconnect_on_failure=True
    )
    username = "admin"
    password = "majestic"
    build_client.tls_set_context(tls_context)
    build_client.username_pw_set(username, password)
    # Configuration de los callbacks del cliente MQTT
    build_client.on_connect = on_connect
    build_client.on_message = on_message
    build_client.on_subscribe = on_subscribe
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


def print_info(client, userData, resultCode, logHeader) -> None:
    """
    Print the clientId from a paho.mqtt.client object.

    Args:
        client: The paho.mqtt.client object.

    Returns:
        None

    Parameters
    ----------
    client
    userData
    logHeader
    resultCode
    """
    if client is Client:
        print(f"[{logHeader}] Client: {client._host} - {client._client_id}")

    print(f"[{logHeader}] UserData: {userData}")
    if resultCode is int:
        print(
            f"[{logHeader}] ResultCode: {resultCode} - {error_code_message(resultCode)}"
        )
    elif resultCode is MQTTMessage:
        print(f"[{logHeader}] Message id: {resultCode.mid}")
        print(f"[{logHeader}] Topic: {resultCode.topic}")
        print(f"[{logHeader}] Qos: {resultCode.qos}")
        print(f"[{logHeader}] Retain: {resultCode.retain}")
        print(f"[{logHeader}] Message payload: {resultCode.payload.decode()}")
    else:
        print(f"[{logHeader}] Unknown resultCode: {resultCode}")


# Función para manejar la conexión con el broker MQTT
def on_connect(client: Client, userdata, flags, rc):
    if rc is int:
        if rc == 0:
            print("[on_connect] Connected al broker MQTT")
            print_info(client, userdata, rc, "on_connect")
            # Suscribirse a un tema específico
            mqtt_client.subscribe("homeassistant/status")
            print("[on_connect] Subscribed to homeassistant/status topic.")
            mqtt_client.publish(
                cfg["topics"]["pressure"] + cfg["topics"]["config"],
                json.dumps(sensehat_device.message_config_pressure("pressure")),
                qos=1,
                retain=True,
            )
            print(
                "[on_connect] Published to "
                + cfg["topics"]["pressure"]
                + cfg["topics"]["config"]
                + " topic."
            )
            mqtt_client.publish(
                cfg["topics"]["humidity"] + cfg["topics"]["config"],
                json.dumps(sensehat_device.message_config_humidity("humidity")),
                qos=1,
                retain=True,
            )
            print(
                f"[on_connect] Published to "
                + cfg["topics"]["humidity"]
                + cfg["topics"]["config"]
                + " topic."
            )
            mqtt_client.publish(
                cfg["topics"]["temperature"] + cfg["topics"]["config"],
                json.dumps(sensehat_device.message_config_temperature("temperature")),
                qos=1,
                retain=True,
            )
            print(
                f"[on_connect] Published to "
                + cfg["topics"]["temperature"]
                + cfg["topics"]["config"]
                + " topic."
            )
        else:
            print(
                f"[on_connect] Connection error. Return Code: {error_code_message(rc)}"
            )
    else:
        print(f"[on_connect] Unexpected Result Code: {type(rc)} {rc}")


# Function to handle the connection with the broker MQTT
def on_subscribe(client, userdata, flags, rc):
    if type(rc) == int:
        if rc == 0:
            print("[on_subscribe] On Subscribe event! Sending configurations!")
            print_info(client, userdata, rc, "on_subscribe")
            print(flags)
            mqtt_client.publish(
                cfg["topics"]["pressure"] + cfg["topics"]["config"],
                json.dumps(sensehat_device.message_config_pressure("pressure")),
                qos=1,
                retain=True,
            )
            print(
                "[on_connect] Published to "
                + cfg["topics"]["pressure"]
                + cfg["topics"]["config"]
                + " topic."
            )
            mqtt_client.publish(
                cfg["topics"]["humidity"] + cfg["topics"]["config"],
                json.dumps(sensehat_device.message_config_humidity("humidity")),
                qos=1,
                retain=True,
            )
            print(
                f"[on_connect] Published to "
                + cfg["topics"]["humidity"]
                + cfg["topics"]["config"]
                + " topic."
            )
            mqtt_client.publish(
                cfg["topics"]["temperature"] + cfg["topics"]["config"],
                json.dumps(sensehat_device.message_config_temperature("temperature")),
                qos=1,
                retain=True,
            )
            print(
                f"[on_connect] Published to "
                + cfg["topics"]["temperature"]
                + cfg["topics"]["config"]
                + " topic."
            )
        else:
            print("[on_subscribe] Connection error!")
            print(f"[on_subscribe] Error Code: {error_code_message(rc)}")
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
    client: Client, topic: str, msg: str, retain: bool = False, qos: int = 0
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


def mqtt_connect(param_client: Client):
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
    # Connect to the MQTT broker
    param_client.connect(
        cfg["broker"]["host"],
        port=cfg["broker"]["port"],
        keepalive=60,
        clean_start=MQTT_CLEAN_START_FIRST_ONLY,
    )
    # Publish an "online" message
    topic = cfg["id"] + cfg["topics"]["availability"]
    param_client.publish(topic, "online")
    return param_client


cfg = load_configuration()
validate_configuration(cfg)
mqtt_client = build_mqtt()


if __name__ == "__main__":
    # Main Program
    # Usage

    # mqtt_client: Client = build_mqtt()
    # sensehat_device = SenseHatDevice(cfg)
    sensehat_device = SenseHatDevice(cfg)
    exit_code = 0
    seconds = int(cfg["seconds"])
    # print(f"Starting sense-hat-mqtt. Warming up during 15 seconds.")
    # time.sleep(15)  # Allow time for sense-hat to warm up and avoid erroneous data
    current_time = datetime.datetime.now()
    print(current_time)
    print(f"Starting sense-hat-mqtt. Refreshing every {seconds} seconds")

    try:
        # sense = SenseHat()
        mqtt_connect(mqtt_client)
        mqtt_client.loop_start()
        while True:
            metrics = sensehat_device.calculate_metrics()
            json_read = metrics["messages"]["json"]
            print(f"[{datetime.datetime.now()}] Reading: {json_read}")
            # print(f"[DEBUG]: {json.dumps(metrics)}")
            publish(
                mqtt_client,
                cfg["topics"]["humidity"] + cfg["topics"]["state"],
                metrics.["humidity"],
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
    except BaseException as ex:
        print("UnknownException, quitting...", ex)
        print("Stop")
        print(f"Ex Type: {type(ex)}")
        sys.stderr.write(f"Exception: {ex}\n")
        sys.stderr.write(f"Traceback: {ex.with_traceback().format_exc()}\n")
        exit_code = 1
    finally:
        # client.disconnect()
        # Cerrar la conexión con el broker MQTT
        print("Quitting...Closing loop and connection...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        current_time = datetime.datetime.now()
        print(f"[{current_time}] Exit! Done!")
        sys.exit(exit_code)

    # end
