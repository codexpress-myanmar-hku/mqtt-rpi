import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata,flags, rc):
    client.subscribe("esp/test")
    print "The connection to the MQTT server is established."

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print msg.topic + " " + str(msg.payload)
    if msg.payload == 'exit':
        print "Recieved exit command"
        client.disconnect()

client = mqtt.Client("rbp")
client.username_pw_set("pi","codexpress")
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

def main():
    client.loop_forever()

if __name__ == '__main__':
    main()
