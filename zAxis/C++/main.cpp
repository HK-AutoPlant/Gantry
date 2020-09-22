#include <Arduino.h>
#include "Classes/StepperMotorClass.h"
#include "Classes/limitSwitchClass.h"

uint8_t stepPin   = 3;
uint8_t dirPin    = 4;
uint8_t enablePin = 5;
uint8_t limitSwitchPin = 2;

stepperMotor zAxis(stepPin, dirPin, enablePin, limitSwitchPin);





void setup()
{
  Serial.begin(9600);
  zAxis.initialize();

  zAxis.home();

  zAxis.status();

  zAxis.moveDistance(10);

  zAxis.status();

  zAxis.moveDistance(-15);

  zAxis.status();



}

void loop() {

}
