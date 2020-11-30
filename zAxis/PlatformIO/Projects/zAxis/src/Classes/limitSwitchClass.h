#ifndef limitSwitchClass_H
#define limitSwitchClass_H

#include "Arduino.h"

class limitSwitch
{
  public:
    limitSwitch(uint8_t limitSwitchPin);
    void initialize();
    bool isPressed();

  private:
    uint8_t _limitSwitchPin;

};

#endif
