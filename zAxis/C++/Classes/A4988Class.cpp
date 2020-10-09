#include "Arduino.h"
#include "A4988Class.h"

#define CLOCKWISE 1

A4988::A4988(uint8_t stepPin, uint8_t dirPin, uint8_t enablePin)
{
  _stepPin = stepPin;
  _dirPin = dirPin;
  _enablePin = enablePin;
}

void A4988::initialize()
{
  pinMode(_stepPin, OUTPUT);
  pinMode(_dirPin, OUTPUT);
  pinMode(_enablePin, OUTPUT);

  digitalWrite(_stepPin, LOW);
  digitalWrite(_dirPin, LOW);
  digitalWrite(_enablePin, HIGH);

}

void A4988::step()
{
  digitalWrite(_stepPin, HIGH);
  delayMicroseconds(pulseDelay);
  digitalWrite(_stepPin, LOW);
  delayMicroseconds(pulseDelay);
}

void A4988::direction(bool dir)
{
  dir == CLOCKWISE ? digitalWrite(_dirPin, HIGH) : digitalWrite(_dirPin, LOW);
}

void A4988::enableMotor(bool state)
{
  state == true ? digitalWrite(_enablePin, LOW) : digitalWrite(_enablePin, HIGH);
}
