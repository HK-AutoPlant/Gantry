from Class.MotorClass import stepperMotor
import socket

TCP_IP = '000.000.000.000';
TCP_PORT = 0000;
BUFFER_SIZE = 128;

zAxisMotor = stepperMotor(3, 5, 7, 11);
zAxisMotor.Home();


while(True):
    msg = 'z200'; #Read the message:
    if(msg =='Home'):
        zAxisMotor.home();
    elif(msg[0] == 'z'):
        zAxisMotor.move(int(msg[1:]));
    elif(msg == 'Auto'):
        print("Do something Autonomous!")
    else:
        print("Nothing to do..");
