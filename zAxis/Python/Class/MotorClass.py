import RPi.GPIO as GPIO
import time, math


GPIO.setwarnings(False);

class stepperMotor():
    def __init__(self, stepPin, dirPin, enablePin, limitswitchPin):
        self._A4988 = self.A4988(stepPin, dirPin, enablePin);
        self._limitSwitch = self.limitSwitch(limitswitchPin);

        self.maxDistance = 500;
        self.minDistance = 0;

        self.currentPosition = 0;

    def home(self):
        print("Homing the motor");
        self._A4988.wakeUp();
        self._A4988.moveCW();

        while(self._limitSwitch.isPressed() is False):
            self._A4988.step();

        self._A4988.sleep();

        print("Motor at home position");
        self.currentPosition = 0;

    def move(self, distance):
        if(distance >= 0):
            self._A4988.moveCW();
        else:
            self._A4988.moveCCW();

        self.currentPosition += distance;

        if(self.currentPosition < self.minDistance or self.currentPosition > self.maxDistance == True):
            print("Out of bounds!")
            self.currentPosition -= distance;
        else:
            self.moveSteps(abs(distance));
            print("Everything OK!")

        print("Current Position: ", self.currentPosition);


    def moveUp(self):
        print("Move to predefined position")
    def moveDown(self):
        print("Move to predefined position")

    def distanceToSteps(self, distance):
        # 2mm per varv!
        dm = 0.01;
        leadAngle = distance;
        return distance;

    def moveSteps(self, steps):
        print("Moving motor", steps, "number of steps");
        self._A4988.wakeUp();
        for i in range(steps):
            self._A4988.step();

        self._A4988.sleep();

    def withinBoundaries(self):
        if(self.currentPosition < self.minDistance or self.currentPosition > self.maxDistance):
            return False;
        else:
            return True;


    class A4988():

            def __init__(self, stepPin, dirPin, enablePin):
                    self.stepPin = stepPin;
                    self.dirPin = dirPin;
                    self.enablePin = enablePin;
                    self.initPins();
                    self.sleep();

            def initPins(self):
                    GPIO.setmode(GPIO.BOARD);
                    GPIO.setup(self.stepPin, GPIO.OUT);
                    GPIO.setup(self.dirPin, GPIO.OUT);
                    GPIO.setup(self.enablePin, GPIO.OUT);

            def moveCW(self):
                GPIO.output(self.dirPin, GPIO.LOW);

            def moveCCW(self):
                GPIO.output(self.dirPin, GPIO.HIGH);

            def sleep(self):
                    GPIO.output(self.enablePin, GPIO.HIGH);

            def wakeUp(self):
                    GPIO.output(self.enablePin, GPIO.LOW);

            def step(self):

                    sleepTime = 0.001; # 1 ms sleeptime

                    GPIO.output(self.stepPin, GPIO.HIGH);
                    time.sleep(sleepTime);
                    GPIO.output(self.stepPin, GPIO.LOW);
                    time.sleep(sleepTime);


    class limitSwitch():
            def __init__(self, switchPin):
                    self.switchPin = switchPin;
                    self.initPins();

            def initPins(self):
                    GPIO.setmode(GPIO.BOARD);
                    GPIO.setup(self.switchPin, GPIO.IN);

            def isPressed(self):
                    if(GPIO.input(self.switchPin) == GPIO.LOW):
                            return True;
                    else:
                            return False;
