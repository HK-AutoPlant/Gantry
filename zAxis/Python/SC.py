# A sketch to test the serial communication with the Arduino.

import serial
import time

BAUD_RATE = 115200

#'/dev/ttyACM0'

class usbCommunication():
    def __init__(self, port, baudRate):
        self.message = None;
        self.ser = serial.Serial(port, baudRate, timeout=1)

	#Input: #z100 for z 100mm down. z-100 for 100mm up
	# Homing: send "home"
    def sendMessage(self, msg):
        self.ser.write(msg.encode('utf-8')) 

	#Output: Confirms whats has been sent
	# if input NOT understood it reports that aswell
    def readMessage(self):
        self.message = self.ser.readline().decode('utf-8').rstrip()
        print(self.message)

    def messageRecieved(self):
        if(self.ser.in_waiting > 0):
            return True
        else:
            return False

# zAxisUsbPort = '/dev/ttyUSB1'

# test = usbCommunication(zAxisUsbPort, BAUD_RATE)

# while(True):
#     msg = input("Input Command: ")
#     test.sendMessage(msg)
#     while(test.messageRecieved() is True):
#         test.readMessage()
