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

  _mmPerStep = (float)mmPerRev/stepsPerRev;
}

void stepperMotor::moveUp()
{
  moveDistance(-((int)_currentPosition - limitSwitchOffset));
}

void stepperMotor::moveDown()
{
  moveDistance(maxDistance - (int)_currentPosition);
}


void stepperMotor::moveDistance(int distance)
{
  if(!_initialHoming)
  {
    Serial.println("The Home is not homed!");
    return;
  }

  distance >= 0 ? _moveCCW() : _moveCW();

  _numberOfSteps = _distanceToSteps(abs(distance));

  _A4988.enableMotor(true);
  for(int i = 0; i < _numberOfSteps; i++)
  {
    _updateCurrentPosition(distance);
      if(_withinBoundaries())
      {
        _A4988.step();
      }
      else
      {
        break;
      }
  }

  _A4988.enableMotor(false);
}

void stepperMotor::home()
{
  _initialHoming = 1; 
  _moveCW();
  _A4988.enableMotor(true);
  while(_limitSwitch.isPressed() == false)
    {
      _A4988.step();
    }
  _A4988.enableMotor(false);
  _currentPosition = 0;
  delay(500);

  moveDistance(limitSwitchOffset);
}


void stepperMotor::_updateCurrentPosition(int distance)
{
   distance >= 0 ? _currentPosition+= _mmPerStep : _currentPosition -= _mmPerStep;
}

void stepperMotor::holdingTorque(bool state)
{
  state == true ? _A4988.enableMotor(true) : _A4988.enableMotor(false);
}

int stepperMotor::_distanceToSteps(int distance)
{
  return (int)distance/_mmPerStep;
}

bool stepperMotor::_withinBoundaries()
{
  if(_currentPosition >= (float)maxDistance)
  {
    _currentPosition = (float)maxDistance; // Resolves an issue that the machine takes one step to much
    return 0;
  }else if(_limitSwitch.isPressed() && _dir == CLOCKWISE)
  {
    _currentPosition = 0.0;
    return 0;
  }
  else{
    return 1;
  }
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
  Serial.print("Lower Position:");
  Serial.print("\t");
  Serial.print("\t");
  Serial.print("\t");
  Serial.print(maxDistance);
  Serial.println(" mm.");
  Serial.print("Maximum allowed position:");
  Serial.print("\t");
  Serial.print(maxDistance);
  Serial.println(" mm.");
}

void stepperMotor::_moveCW()
{
  _A4988.direction(CLOCKWISE);
  _dir = CLOCKWISE;
}

void stepperMotor::_moveCCW()
{
  _A4988.direction(COUNTERCLOCKWISE);
  _dir = COUNTERCLOCKWISE;
}
