#ifndef A4988Class_h
#define A4988Class_h

#include "Arduino.h"

class A4988
{
  public:
    A4988(uint8_t stepPin, uint8_t dirPin, uint8_t enablePin);
    void initialize();
    void step();
    void direction(bool dir);
    void enableMotor(bool state);

  private:
    uint8_t _stepPin;
    uint8_t _dirPin;
    uint8_t _enablePin;
    float pulseDelay = 600; // [us]
};

#endif
