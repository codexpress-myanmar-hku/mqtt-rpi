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

#We will use a pre-defined conversion of data into JSON
def convertTOJSON(x):
    data = {
        "temp": x[0],
        "humidity": x[1],
        "soil_moist": x[2],
        "soil_temp" : x[3],
        "input_voltage": x[4],
        "input_current": x[5]
    }   
    return data

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata,flags, rc):
    client.subscribe("esp/test")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logging.info("MQTT INCOMING MESSAGE: " + msg.topic + " " + str(msg.payload.decode()) + " at timestamp: " + timeNow())
    if msg.payload == 'exit':
        logging.info("Recieved exit command")
        client.disconnect()
    else:
        data = msg.payload.decode()
        x = None
        try:
            data = str(data)
            data_array = data.split(",")
            data_array = [float(d) for d in data_array]
            logging.info(data_array)
            x = convertTOJSON(data_array)
            logging.info("DATA ENTRY: " + str(x))
            r = requests.post("http://localhost:3000/data", json=x)
            if r and r.status_code == 200:
                logging.info("Delivery at: " + timeNow())

        except ValueError:
            logging.warning("Error in data parsing: " + timeNow())
        
        except json.JSONDecodeError:
            logging.warning("Invalid JSON" + str(x))
    
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
