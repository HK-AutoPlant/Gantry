#include <Arduino.h>

#define SENSE_PIN A0

int numberOfAverages = 100;
//int moisture;

//CalibratedValue:
int soil = -210;
int water = 210;

int getMoistureLevel(void);

void setup() {
  Serial.begin(9600);
  pinMode(SENSE_PIN, INPUT);
}

void loop() {
  //for(int i = 0; i < numberOfAverages; i++)
  //{
  //  moisture += analogRead(SENSE_PIN);
//  }
//  Serial.println(moisture/numberOfAverages);
//  moisture = 0;
  int a = getMoistureLevel();
  Serial.println(a);

  delay(1000);
}

int getMoistureLevel(void)
{
  int moisture = 0;
  for(int i = 0; i < numberOfAverages; i++)
  {
    moisture += analogRead(SENSE_PIN);
    delay(1);
  }
  return moisture/numberOfAverages;
}
