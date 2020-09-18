import paho.mqtt.client as mqtt
import math 
import json
import odrive
from odrive.enums import *

# The callback for when the client receives a CONNACK response from the server.
odrv0 = odrive.find_any()
print(str(odrv0.vbus_voltage))
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
#odrv0.axis0.requested_state = AXIS_STATE_IDLE


position = [0,0,0]
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test/topic")

# The callback for when a PUBLISH message is received from the server.


#Har behover vi ha en konverteringsfaktor mellan encodersnspp och mm
mm_to_encoder = 1/(25*math.pi/2048)


def on_message(client, userdata, msg):
    print(str(msg.payload,'utf-8'))
    message = str(msg.payload, 'utf-8')
    #print('x' in str(msg.payload))
    global position
    #print('hej1')
    #print(msg.payload[msg.payload.find('x')+1:])
    if ('x' in message):
        #print('hej2')
        position[0] = position[0] + int(message[message.find('x')+1:])
        #print('hej3')
        odrv0.axis0.controller.move_to_pos(position[0]*mm_to_encoder)
        print('input='+str(position[0]*mm_to_encoder))
        print(position)
    elif ('y' in message):
        position[1] = position[1] + int(message[message.find('y')+1:])
        print(position)
    elif ('z' in message):
        position[2] = position[2] + int(message[message.find('z')+1:])
        print(position)
    elif ('off' in message):
        odrv0.axis0.requested_state = AXIS_STATE_IDLE
    elif ('on' in message):
        odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL


    #dessa ar inte korrekta, det ska sta nagot liknande skulle jag tro.
    #serial.bus.to.odrive = "odrv0.axis0.controller.move_to_pos(" + str(position[0]*mm_to_encoder) + ")"
    #serial.bus.to.odrive = "odrv0.axis1.controller.move_to_pos(" + str(position[1]*mm_to_encoder) + ")"
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('192.168.1.104', 10000, 60)
client.loop_forever()
