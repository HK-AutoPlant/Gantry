#include <Arduino.h>
#include "Classes/StepperMotorClass.h"
#include "Classes/limitSwitchClass.h"

#define BAUD_RATE 115200

uint8_t dirPin    = 8;
uint8_t stepPin   = 9;
uint8_t enablePin = 10;
uint8_t limitSwitchPin = 11;

stepperMotor zAxis(stepPin, dirPin, enablePin, limitSwitchPin);

String msg;
int distance;
int parseMessage(String msg);

void setup()
{
  Serial.begin(BAUD_RATE);
  zAxis.initialize();
}

void loop() {
  // Recieve Message:
  // If message Recieved:


  if(Serial.available() > 0)
  {
    msg = Serial.readString();

    switch (msg[0]) {
      case 'H':
        zAxis.home();
        Serial.println("z-Axis homed.");
      break;

      case 'z':
        distance = parseMessage(msg);
        zAxis.moveDistance(distance);

        Serial.print("z-Axis moved ");
        Serial.print(distance);
        Serial.println(" mm");

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
