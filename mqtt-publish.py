import paho.mqtt.client as mqtt
import json
import time

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883, 60)

data = {
    "sensor": "temperature",
    "value": 25.5,
    "unit": "Celsius"
}

while True:
    payload = json.dumps(data)
    client.publish("esp32/sensor", payload)
    print(f"Published: {payload}")
    time.sleep(1)
