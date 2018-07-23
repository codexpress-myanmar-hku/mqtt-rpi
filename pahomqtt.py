import paho.mqtt.client as mqtt
import requests
import time
import json
import logging

logging.basicConfig(filename="logs.log" , level=logging.DEBUG)

def timeNow():
    return str(time.asctime(time.localtime())) 

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata,flags, rc):
    client.subscribe("esp/test")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logging.info(msg.topic + " " + str(msg.payload.decode()) + " " + str(time.asctime(time.localtime())))
    if msg.payload == 'exit':
        logging.info("Recieved exit command")
        client.disconnect()
    else:
        data = msg.payload.decode()
        print(data, timeNow())
        try:
            r = requests.post("http://localhost:3000/data", json=json.loads(data))
            if r and r.status_code == 200:
                logging.info("Delivery at: " + str(time.asctime(time.localtime())))
        
        except json.JSONDecodeError:
            logging.warning("Invalid JSON at: " + str(time.asctime(time.localtime())))
        
client = mqtt.Client("rbp")
client.username_pw_set("pi","codexpress")
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

def main():
    client.loop_forever()

if __name__ == '__main__':
    main()
