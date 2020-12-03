#include <Arduino.h>
#include "Classes/StepperMotorClass.h"
#include "Classes/limitSwitchClass.h"

#define BAUD_RATE 115200
#define COMMAND_COMPLETED 1
#define COMMAND_NOT_COMPLETED 0


uint8_t zAxisDirPin    = 9;
uint8_t zAxisStepPin   = 10;
uint8_t zAxisEnablePin = 11;
uint8_t zAxisLimitSwitchPin = 14; // Same as A0!

uint8_t gripperDirPin    = 5;
uint8_t gripperStepPin   = 6;
uint8_t gripperEnablePin = 7;
uint8_t gripperAxisLimitSwitchPin = 18; // Same as A4!

uint8_t soilSensorPin1 = 15;
uint8_t soilSensorPin2 = 16;
uint8_t soilSensorPin3 = 17;
uint8_t soilSensorPin4 = 20;
uint8_t soilSensorPin5 = 21;


stepperMotor zAxis(zAxisStepPin, zAxisDirPin, zAxisEnablePin, zAxisLimitSwitchPin);
stepperMotor Gripper(gripperStepPin, gripperDirPin, gripperEnablePin, gripperAxisLimitSwitchPin);

limitSwitch soilSensor1(soilSensorPin1);
limitSwitch soilSensor2(soilSensorPin2);
limitSwitch soilSensor3(soilSensorPin3);
limitSwitch soilSensor4(soilSensorPin4);
limitSwitch soilSensor5(soilSensorPin5);


String msg;
int distance;
int position;

int parseMessage(String msg);
void detectSoil();

void setup()
{
  Serial.begin(BAUD_RATE);
  zAxis.maxDistance = 150;
  zAxis.mmPerRev = 6;
  zAxis.initialize();

  Gripper.maxDistance = 20;
  Gripper.limitSwitchOffset = 0;
  Gripper.stepsPerRev = 200;
  Gripper.initialize();

  soilSensor1.initialize();
  soilSensor2.initialize();
  soilSensor3.initialize();
  soilSensor4.initialize();
  soilSensor5.initialize();

}

void loop() {
  // Recieve Message:
  // If message Recieved:

  while(Serial.available() > 0)
  {
    //Serial.println(COMMAND_NOT_COMPLETED);
    msg = Serial.readString();

    switch (msg[0]) {
      case 'H': //Home zAxis
        zAxis.home();
      break;

      case 'h': //Home Gripper
        Gripper.home();
      break;

      case 'z': //Move zAxis
        distance = parseMessage(msg);
        zAxis.moveDistance(distance);
      break;

      case 'g': //Move Gripper
        distance = parseMessage(msg);
        Gripper.moveDistance(distance);
      break;

      case 'D': //Move down zAxis
        zAxis.moveDown();
      break;
      case 'd': //Move down Gripper
        Gripper.moveDown();
      break;

      case 'P':
        position = parseMessage(msg);
        zAxis.moveTo(position);
      break;

      case 'p':
        position = parseMessage(msg);
        Gripper.moveTo(position);
      break;

      case 'c': //Check Soil Sesors
        detectSoil();
      break;

      case 's': //Prints out the current status
        zAxis.status();
        Gripper.status();
      break;

      default:
        Serial.println("Message not understood");
      break;
    }
    Serial.println(COMMAND_COMPLETED);
  }
}

int parseMessage(String msg)
{
  bool negativeNumber = 0;

  if(msg[1] == '-')
  {
    msg.remove(0, 2);
    negativeNumber = 1;
  }
  else
  {
    msg.remove(0, 1);
  }

  return negativeNumber == 1 ? (-1)*msg.toInt() : msg.toInt();
}

void detectSoil()
{
  String divisor = ",";
  Serial.println(soilSensor1.isPressed() + divisor + soilSensor2.isPressed() + divisor + soilSensor3.isPressed() + divisor + soilSensor4.isPressed() + divisor + soilSensor5.isPressed());
}
