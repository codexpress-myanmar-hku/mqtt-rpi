# mqtt-rpi
The MQTT Server for the Raspberry Pi

## Data Scematics
The MQTT Server on the Raspberry Pi will recieve data in the following format:
`"{\"key\": "value"}"`

Note that the `\"` is necessary so that the parser can parse the data as JSON. (It translates to `"`).

## Plan and Data Flow
The Arduino will send data via the ESP to the Raspberry Pi using the MQTT protocol. The ESP8266 will have the pre-defined IP Address for the Raspberry Pi to which it will send data.

That data will be sent via this Python script to the Node.js server running on port `3000`. Refer to the [thinkspeak-rpi repository](https://github.com/codexpress-myanmar-hku/thinkspeak-rpi) for further information.
