import paho.mqtt.client as mqtt
import requests
import time
import json
import logging
import socket

logging.basicConfig(filename="logs.log" , level=logging.DEBUG)


#Function to get the current time
def timeNow():
    return str(time.asctime(time.localtime())) 

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata,flags, rc):
    client.subscribe("esp/test")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logging.info(msg.topic + " " + str(msg.payload.decode()) + " " + timeNow())
    if msg.payload == 'exit':
        logging.info("Recieved exit command")
        client.disconnect()
    else:
        data = msg.payload.decode()
        logging.info("Recieved data: " + str(data) + " TimeStamp: " + timeNow())
        try:
            data = str(data)
            data_array = data.split(",")
            data_array = [float(d) for d in data_array]
            logging.info(data_array)
            """
            r = requests.post("http://localhost:3000/data", json=json.loads(data))
            if r and r.status_code == 200:
                logging.info("Delivery at: " + timeNow())
            """
        except json.JSONDecodeError:
            logging.warning("Invalid JSON at: " + timeNow())
    
client = mqtt.Client("rbp")
client.username_pw_set("pi","codexpress")
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect("localhost", 1883, 60)
except socket.error:
    logging.error("Error in MQTT Connection")


def main():
    client.loop_forever()

if __name__ == '__main__':
    main()
