#include <Arduino.h>
#include "Classes/StepperMotorClass.h"
#include "Classes/limitSwitchClass.h"

#define BAUD_RATE 115200

uint8_t zAxisDirPin    = 9;
uint8_t zAxisStepPin   = 10;
uint8_t zAxisEnablePin = 11;
uint8_t zAxisLimitSwitchPin = 14; // Same as A0!

uint8_t gripperDirPin    = 10;
uint8_t gripperStepPin   = 11;
uint8_t gripperEnablePin = 12;
uint8_t gripperAxisLimitSwitchPin = 19; // Same as A6!

uint8_t soilSensor1 = 18;


stepperMotor zAxis(zAxisStepPin, zAxisDirPin, zAxisEnablePin, zAxisLimitSwitchPin);
stepperMotor Gripper(gripperStepPin, gripperDirPin, gripperEnablePin, gripperAxisLimitSwitchPin);

limitSwitch soilSensor(soilSensor1);

String msg;
int distance;
int parseMessage(String msg);

void setup()
{
  Serial.begin(BAUD_RATE);
  zAxis.initialize();
  zAxis.maxDistance = 150;

  Gripper.initialize();
  Gripper.maxDistance = 7.3;
  Gripper.stepsPerRev = 300;

}

void loop() {
  // Recieve Message:
  // If message Recieved:

  while(Serial.available() > 0)
  {
    msg = Serial.readString();

    switch (msg[0]) {
      case 'H': //Home
        zAxis.home();
      break;

      case 'z': //zMove
        distance = parseMessage(msg);
        zAxis.moveDistance(distance);
      break;

      case 'D': //moveDown
        zAxis.moveDown();
      break;

      case 'G':
        Gripper.moveDown();
        Gripper.holdingTorque(true); // Might not be necessary!
      break;

      case 'c':
        soilSensor.isPressed() ? Serial.println("Soil detected") : Serial.println("Soild not detected");
      break;

      case 'r':
        Gripper.home();
      break;
      default:
        Serial.println("Message not understood");
      break;
    }
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
