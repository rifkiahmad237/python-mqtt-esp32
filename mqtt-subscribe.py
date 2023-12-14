import paho.mqtt.client as mqtt
import json
import time
import threading
from tkinter import *
from tkinter import ttk
topic_pub = "rifki-mqtt/datapub"
topic_sub = "rifki-mqtt/command"
thread_stop = threading.Event()
class GUI:
    def __init__(self, window) -> None:
        self.window = window
        window.title("Simple MQTT Dashboard")
        window.geometry("185x202")
        window.resizable(False, False)
        self.tempTextBox = Label(self.window, text="0", borderwidth=2, relief="solid")
        self.tempTextBox.place(x=30, y=42, width=50, height=35)
        self.labelTemp = Label(self.window, text="Temperature")
        self.labelTemp.place(x=18, y=90, width=76, height=21)
        self.humTextBox = Label(self.window, text="0", borderwidth=2, relief="solid")
        self.humTextBox.place(x=110, y=42, width=50, height=35)
        self.labelTemp = Label(self.window, text="Humidity")
        self.labelTemp.place(x=100, y=90, width=76, height=21)
        self.ledButton = Button(self.window, text="OFF", command=ledControl)
        self.ledButton.place(x=72, y=125, width=42, height=24)
        self.ledLabel = Label(self.window, text="LED Control")
        self.ledLabel.place(x=59, y=161, width=67, height=21)


def ledControl():
    if mqtt_gui.ledButton.config("text")[-1] == "OFF":
        mqtt_gui.ledButton.config(text="ON")
        thread = threading.Thread(target=control, args=("LED", 1, thread_stop))
        thread.start()
    else:
        mqtt_gui.ledButton.config(text="OFF")
        thread_stop.set()
        thread = threading.Thread(target=control, args=("LED", 0, thread_stop))
        thread.start()
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        data = json.loads(payload)
        # print(f"Received message: {data} on topic {msg.topic}")
        print(f"Suhu: {data['temp_value']}")
        print(f"Kelembaban: {data['hum_value']}")
    except json.JSONDecodeError as err:
        print(f"Error decoding JSON: {err}")


def control(a: str, b: int, stop_event: threading.Event)-> None:
    while not stop_event.is_set():
        data = {"command": a, "com_value":b}
        payload = json.dumps(data)
        client.publish(topic_sub, payload)
        print(f"Published {payload}")
        time.sleep(1)

client = mqtt.Client()
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.subscribe(topic_pub)
root = Tk()
mqtt_gui=GUI(root)
root.mainloop()
client.loop_forever()
# time.sleep(2) 

# while True:
#     if client.is_connected() == False:
#         client.connect("broker.hivemq.com", 1883, 60)
#     # comand1 = control("LED", 0)
#     # comand2 = control("LED", 1)

