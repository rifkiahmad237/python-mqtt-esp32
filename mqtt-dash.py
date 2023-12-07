import paho.mqtt.client as mqtt
import json
import time
import threading
topic_pub = "rifki-mqtt/datapub"
topic_sub = "rifki-mqtt/command"
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        data = json.loads(payload)
        # print(f"Received message: {data} on topic {msg.topic}")
        print(f"Suhu: {data['temp_value']}")
        print(f"Kelembaban: {data['hum_value']}")
    except json.JSONDecodeError as err:
        print(f"Error decoding JSON: {err}")


def worker():
    def control(a: str, b: int)-> str:
        data = {"command": a, "com_value":b}
        payload = json.dumps(data)
        client.publish(topic_sub, payload)
        print(f"Published {payload}")
        time.sleep(5)
    while True:
        comand1 = control("LED", 0)
        comand2 = control("LED", 1)


client = mqtt.Client()
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.subscribe(topic_pub)
thread = threading.Thread(target=worker)
thread.start()
client.loop_forever()
# time.sleep(2) 

# while True:
#     if client.is_connected() == False:
#         client.connect("broker.hivemq.com", 1883, 60)
#     # comand1 = control("LED", 0)
#     # comand2 = control("LED", 1)

