import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe('raspberry/status')
    client.subscribe('homeassistant/status')
    client.subscribe('homeassistant/device/rpi')
    # Send a message to the raspberry/topic every 1 second, 5 times in a row
    for i in range(3):
        # The four parameters are topic, sending content, QoS and whether retaining the message respectively
        client.publish('raspberry/topic', payload=i, qos=0, retain=False)
        print(f"send {i} to raspberry/topic")


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` on topic `{msg.topic}`")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.will_clear()
client.will_set('raspberry/status', b'{"status": "offline", "client": "publisher"}')
client.connect("192.168.1.101", 1883, 60)

client.loop_forever()
