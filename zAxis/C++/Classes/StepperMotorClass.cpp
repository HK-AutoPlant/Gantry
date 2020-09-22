#include "Arduino.h"
#include "SteppermotorClass.h"

#define CLOCKWISE 1
#define COUNTERCLOCKWISE 0


stepperMotor::stepperMotor(uint8_t stepPin, uint8_t dirPin, uint8_t enablePin, uint8_t limitSwitchPin)
: _A4988(stepPin, dirPin, enablePin), _limitSwitch(limitSwitchPin){}

void stepperMotor::initialize()
{
  _A4988.initialize();
  _limitSwitch.initialize();
}

void stepperMotor::moveUp()
{

}

void stepperMotor::moveDown()
{

}


void stepperMotor::moveDistance(int distance)
{

  distance >= 0 ? _moveCW() : _moveCCW();

  _numberOfSteps = _distanceToSteps(abs(distance));

  _A4988.enableMotor(true);

  for(int i = 0; i < _numberOfSteps; i++)
  {
    _A4988.step();
    distance >= 0 ? _currentPosition+= _mmPerStep : _currentPosition-= _mmPerStep;
  }
  _A4988.enableMotor(false);
}

void stepperMotor::home()
{
  _moveCCW();
  _A4988.enableMotor(true);
  while(_limitSwitch.isPressed() == false)
    _A4988.step();

  _currentPosition = 0;

  moveDistance(limitSwitchOffset);
}

void stepperMotor::holdingTorque(bool state)
{
  state == true ? _A4988.enableMotor(true) : _A4988.enableMotor(false);
}

int stepperMotor::_distanceToSteps(int distance)
{
  return (int)distance/_mmPerStep;
}

void stepperMotor::status()
{
  Serial.println("----- Current Status -----");
  Serial.print("Current Position:");
  Serial.print("\t");
  Serial.print("\t");
  Serial.print(_currentPosition);
  Serial.println(" mm.");
  Serial.print("Limit switch Offset:");
  Serial.print("\t");
  Serial.print("\t");
  Serial.print(limitSwitchOffset);
  Serial.println(" mm.");
  Serial.print("Upper Position:");
  Serial.print("\t");
  Serial.print("\t");
  Serial.print("\t");
  Serial.print(upperPosition);
  Serial.println(" mm.");
  Serial.print("Lower Position:");
  Serial.print("\t");
  Serial.print("\t");
  Serial.print("\t");
  Serial.print(lowerPosition);
  Serial.println(" mm.");
  Serial.print("Maximum allowed position:");
  Serial.print("\t");
  Serial.print(maxDistance);
  Serial.println(" mm.");
}

void stepperMotor::_moveCW()
{
  _A4988.direction(CLOCKWISE);
}

void stepperMotor::_moveCCW()
{
  _A4988.direction(!CLOCKWISE);
}
