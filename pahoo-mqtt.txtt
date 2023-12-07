from paho.mqtt import client as mqtt_client
import json

broker = 'iot.reyax.com'
port = 1883
topic = "api/request"
topic_sub = "api/notification/37/#"
# generate client ID with pub prefix randomly
client_id = 'your client id'
username = 'your username'
password = 'your password'
deviceId = "your deviceId"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)


    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, status):
    msg = "{\"action\":\"command/insert\",\"deviceId\":\""+deviceId+"\",\"command\":{\"command\":\"LED_control\",\"parameters\":{\"led\":\""+status+"\"}}}"
    result = client.publish(msg,topic)
    msg_status = result[0]
    if msg_status ==0:
        print(f"message : {msg} sent to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #print(f"Recieved '{msg.payload.decode()}' from '{msg.topic}' topic")
        y = json.loads(msg.payload.decode())
        temp = y["notification"]["parameters"]["temp"]
        hum = y["notification"]["parameters"]["humi"]
        print("temperature: ",temp,", humidity:",hum)



    client.subscribe(topic_sub)
    client.on_message = on_message

def main():
    client = connect_mqtt()
    subscribe(client)

    client.loop_forever()

if __name__ == '__main__':
    main()