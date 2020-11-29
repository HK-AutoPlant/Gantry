#include "Arduino.h"
#include "limitSwitchClass.h"

limitSwitch::limitSwitch(uint8_t limitSwitchPin)
{
  _limitSwitchPin = limitSwitchPin;
}

void limitSwitch::initialize()
{
  pinMode(_limitSwitchPin, INPUT);
}

bool limitSwitch::isPressed()
{
  if(digitalRead(_limitSwitchPin) == LOW )
    return true;
  else
    return false;
}
