from Class.MotorClass import stepperMotor
import time

zAxisMotor = stepperMotor(3, 5, 7, 11);

zAxisMotor.step(400);
time.sleep(1);
zAxisMotor.step(-400)
