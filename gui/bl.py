#import evdev
from evdev import InputDevice, categorize, ecodes

#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event2')

#prints out device info at start
print(gamepad)

#evdev takes care of polling the controller in a loop
def testButtonCodes():
    for event in gamepad.read_loop():
        print(categorize(event))

#star(left) = 158
#select(right) =315
#rb=311
#rt
#
aBtn = 304
bBtn = 305
yBtn = 308
xBtn = 307
up = 115
down = 114
left = 165
right = 163
playpause = 164
def readXboxInput():
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_KEY:
            # print(ecodes)
            if event.value == 1:
                if event.code == aBtn:
                    print("A")
                elif event.code == bBtn:
                    print("B")
                elif event.code == playpause:
                    print("Play/Pause")
                elif event.code == up:
                    print("up")
                elif event.code == down:
                    print("down")
                elif event.code == left:
                    print("left")
                elif event.code == right:
                    print("right")
                elif event.code == yBtn:
                    print("Y")
                elif event.code == xBtn:
                    print("X")
        elif event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            #print(absevent.event)
            print(ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value)
            a = (ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value)           
            #print(a[1])
            if a[0] == "ABS_BRAKE":
                print("Brake")
            elif a[0] == "ABS_GAS":
                print("Gas")
            elif a[0] == "ABS_HAT0X" and a[1] == -1:
                print("Hat0 Left")
            elif a[0] == "ABS_HAT0X" and a[1] == 1:
                print("Hat0 Right")

            elif a[0] == "ABS_HAT0Y" and a[1] == -1:
                print("Hat0 UP")
            elif a[0] == "ABS_HAT0Y" and a[1] == 1:
                print("Hat0 Down")
                
readXboxInput()