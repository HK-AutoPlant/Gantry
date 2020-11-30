#include "Arduino.h"
#include "L9110HController.h"
#include "Math.h"

#define MAXVOLTAGE 6

L9110H::L9110H(uint8_t IA, uint8_t IB)
{
  _IA = IA;
  _IB = IB;
}

void L9110H::initialize()
{
  pinMode(_IA, OUTPUT);
  pinMode(_IB, OUTPUT);
  stop();
}

void L9110H::drive(float voltage)
{

  _voltage = _voltageToPWM(fabs(voltage));
  if(voltage > 0) _forward(_voltage);
  else if(voltage < 0) _backward(_voltage);
  else stop();
}

float L9110H::_voltageToPWM(float voltage)
{
  return voltage/MAXVOLTAGE * 255;
}


void L9110H::_forward(uint8_t PWM)
{
  digitalWrite(_IB, LOW);
  analogWrite(_IA, PWM);
}

void L9110H::_backward(uint8_t PWM)
{
  digitalWrite(_IB, HIGH);
  analogWrite(_IA, 1-PWM);
}

void L9110H::stop()
{
  digitalWrite(_IA, LOW);
  digitalWrite(_IB, LOW);
}
