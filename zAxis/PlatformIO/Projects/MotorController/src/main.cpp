#include <Arduino.h>
#include "L9110HController.h"

#define PULSES_PER_REV 517
#define MAX_VOLTAGE 6


uint8_t IA = 9;
uint8_t IB = 6;

uint8_t C1 = 2;
uint8_t C2 = 5;

volatile int encoderCounter = 0;

L9110H motor(IA, IB);

uint8_t loopUpdateFrequency = 20;
unsigned long currentMillis;
unsigned long previousMillis = 0;

int reference = 100;

void isr1(void);
void PIOutputFeedback(float reference, float velocity);
void PIErrorFeedback(float reference, float velocity);
float currentVelocity(void);
float radToRPM(float velocity);
float checkSaturation(float voltage);


void setup()
{
  Serial.begin(9600);
  // Set PWM frequency to 31372.55 Hz
  TCCR2B = TCCR2B & B11111000 | B00000001;

  motor.initialize();

  pinMode(C1, INPUT);
  pinMode(C2, INPUT);

  attachInterrupt(digitalPinToInterrupt(C1), isr1, RISING);
}

void loop()
{
  currentMillis = millis();
  if(currentMillis-previousMillis >= 1000/loopUpdateFrequency)
  {
    float velocity = currentVelocity();
    PIOutputFeedback(reference, velocity);
    Serial.print("Ref: ");
    Serial.print("\t");
    Serial.print(reference);
    Serial.print("\t");
    Serial.print("Velocity: ");
    Serial.print("\t");
    Serial.print(velocity);
    Serial.print("\t");
    Serial.print("Error: ");
    Serial.println(reference - velocity);


    previousMillis = currentMillis;
  }
}

void PIErrorFeedback(float reference, float velocity)
{
  float Kp = 1;
  float KI = 10;
  float KD = 0;

  float error = reference - velocity;

  
  u = checkSaturation(u);
  motor.drive(u);

  oldReference = reference;
  oldVelocity = velocity;
  oldControlSignal = u;
}

void PIOutputFeedback(float reference, float velocity)
{
  static float oldReference = 0;
  static float oldVelocity  = 0;
  static float oldControlSignal = 0;

  float a = 0.2327;
  float b = -0.181;
  float c = -1;
  float d = 0.117;
  float e = -0.06528;

  float u = a * reference + b * oldReference - (d * velocity + e * oldVelocity) - c * oldControlSignal;

    // Saturation:
  u = checkSaturation(u);

  motor.drive(u);


  oldReference = reference;
  oldVelocity = velocity;
  oldControlSignal = u;

}

float checkSaturation(float voltage)
{
  if (voltage > MAX_VOLTAGE) return MAX_VOLTAGE;
  if (voltage < -MAX_VOLTAGE) return -MAX_VOLTAGE;

  return voltage;
}

float currentVelocity(void)
{
  static int previousEncoderCounter = 0;
  float velocity = 2*PI*(encoderCounter - previousEncoderCounter)/(PULSES_PER_REV/loopUpdateFrequency);
  previousEncoderCounter = encoderCounter;
  return radToRPM(velocity);
}

float radToRPM(float velocity)
{
  return velocity * 30/PI;
}
void isr1(void)
{
  bitRead(PIND, C2) ? encoderCounter++ : encoderCounter--;
}
