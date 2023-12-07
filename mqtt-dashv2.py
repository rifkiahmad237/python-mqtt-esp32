import paho.mqtt.client as mqtt
import json
import time
from tkinter import *
from tkinter import ttk

topic_pub = "rifki-mqtt/datapub"
topic_sub = "rifki-mqtt/command"

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
        self.ledButton = Button(self.window, text="OFF", command=self.ledControl)
        self.ledButton.place(x=72, y=125, width=42, height=24)
        self.ledLabel = Label(self.window, text="LED Control")
        self.ledLabel.place(x=59, y=161, width=67, height=21)

    def ledControl(self):
        if self.ledButton.cget("text") == "OFF":
            self.ledButton.config(text="ON")
            self.control("LED", 1)
        else:
            self.ledButton.config(text="OFF")
            self.control("LED", 0)

    # def update_gui(self):
    #     # Dapatkan data dari MQTT dan perbarui GUI
    #     data = self.get_data_from_mqtt()
    #     self.tempTextBox.config(text=str(data.get("temp_value", "0")))
    #     self.humTextBox.config(text=str(data.get("hum_value", "0")))

    #     # Jadwalkan pembaruan GUI setiap 1000 ms (1 detik)
    #     self.window.after(1000, self.update_gui)

    def get_data_from_mqtt(self):
        # Ambil data dari MQTT atau gunakan nilai default jika tidak ada data
        # Pastikan untuk mengganti implementasi ini dengan cara yang sesuai dengan skema Anda
        return {"temp_value": "0", "hum_value": "0"}

    def control(self, a: str, b: int) -> None:
        data = {"command": a, "com_value": b}
        payload = json.dumps(data)
        client.publish(topic_sub, payload)
        print(f"Published {payload}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        data = json.loads(payload)
        print(f"Suhu: {data['temp_value']}")
        print(f"Kelembaban: {data['hum_value']}")
    except json.JSONDecodeError as err:
        print(f"Error decoding JSON: {err}")
            # Dapatkan data dari MQTT dan perbarui GUI
    mqtt_gui.tempTextBox.config(text=str(data['temp_value']))
    mqtt_gui.humTextBox.config(text=str(data['hum_value']))

    # Jadwalkan pembaruan GUI setiap 1000 ms (1 detik)
    mqtt_gui.window.after(1000, on_message(client, userdata, msg))

client = mqtt.Client()
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.subscribe(topic_pub)

root = Tk()
mqtt_gui = GUI(root)
root.mainloop()
