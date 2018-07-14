import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
	print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
#	client.subscribe("$SYS/#")
	print("connected")
	client.subscribe("esp/test")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	if msg.payload.decode() == "rbp exit":
		print("Ordered to exit")
		client.disconnect()

client = mqtt.Client("rbp")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("username","password")
client.connect("192.168.1.137", 1883, 60)
print("After connect")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_start()
client.subscribe("esp/test,0")
client.publish("esp/test","rbp python message")
time.sleep(4)
#client.loop_stop()
#client.loop_forever()
#client.disconnect()
