import threading
import random
import sys
import logging
from threading import Lock
from threading import Thread
from time import sleep
lock = threading.Condition() #thread condition var
control = 0 #global control value
currentX = 1 #global for X position of the rover
currentY = 1 #global for Y position of the rover
logging.basicConfig(filename='rover.log',format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)


"""
Makes the map that the rover moves around, it is a 2 dimentional list (Matrix).
Must be passed:
    * desired width of map
    * Desired height of map
"""
def mapCreate(w,h):
    mapToOut = [[0 for i in range(w)] for j in range(h)]
    for i in range(0,40):
        genX = random.randint(0,9)
        genY = random.randint(0,9)
        if mapToOut[genX][genY] == 0:
            mapToOut[genX][genY] = random.randint(1,3)
    mapToOut[genX][genY] = 4
    return mapToOut


"""
What each number represents in the marMap:
    0 = normal ground
    1 = rock (blocked)
    2 = hole (freewheeling)
    3 = sand (sinking)
    4 = water (Mission Success)
Must be passed:
    * The mar map
    * The wheels X coordinate
    * The wheels Y coordinate
"""
def mapCheck(marsMap,wheelX,wheelY):
    if marsMap[wheelX][wheelY] == 0:
        return "clear"
    elif marsMap[wheelX][wheelY] == 1:
        return "rock"
    elif marsMap[wheelX][wheelY] == 2:
        return "hole"
    elif marsMap[wheelX][wheelY] == 3:
        return "sands"
    elif marsMap[wheelX][wheelY] == 4:
        return "water"
    else:
        return "Out of boundaries"
    return 0

"""
Get the current location of all the wheels and puts them in an
2d dict to be returned.
Must be passed:
    * The mars map 2d list
"""
def getWheelLoc(marsMap):
    wheels = {
        "x": {0:currentX - 1, 1:currentX - 1, 2:currentX - 1, 3:currentX + 1, 4:currentX + 1, 5:currentX + 1},
        "y": {0:currentY - 1, 1:currentY, 2:currentY + 1, 3:currentY - 1, 4:currentY, 5:currentY + 1}
    }

    return wheels


"""
Checks if the rover is stuck and needs to ask for help.
Must be passed:
    * The mars map 2d list
"""
def stuckTester(marsMap):
    logging.info("-- Checking if rover is stuck")
    print ("Checking...")
    
    wheels = getWheelLoc(marsMap)

    if (mapCheck(marsMap, wheels['x'][0], wheels['y'][0]) == "rock" and mapCheck(marsMap, wheels['x'][2], wheels['y'][2]) == "rock"):
        return "blocked by rocks"
    elif (mapCheck(marsMap, wheels['x'][0], wheels['y'][0]) == "hole" and mapCheck(marsMap, wheels['x'][2], wheels['y'][2]) == "hole"):
        return "stuck in hole"
    elif (mapCheck(marsMap, wheels['x'][0], wheels['y'][0]) == "sand" and mapCheck(marsMap, wheels['x'][2], wheels['y'][2]) == "sand"):
        return "stuck in sand"
    return False

"""
Main control thread that manages rover movement. Uses
the global vars currentX and currentY
Must be passed:
    * The mars map 2d list
"""
def mainControl(marsMap):
    global control
    global currentX
    global currentY
    direction = 0 #0=east, 1=west
    while True:
        lock.acquire()

        print ("Rover locaton X:",currentX,"Y:",currentY)
        logging.info("-- Rover locaton X:"+str(currentX)+"Y:"+str(currentY))

        if (stuckTester(marsMap) != False):
            logging.warning(" -- Rover is stuck awaiting help")
            print ("Rover is stuck awaiting help...")
            if stuckTester(marsMap) == "blocked by rocks":
                print ("Rover problem:", stuckTester(marsMap))
                answer = input("What should I do: ")
                if (answer == "stop"):
                    logging.info("-- User has told rover to stop")
                    logging.info("-- Stopping")
                    print("Stopping...")
                    exit()
                elif (answer == "move"):
                    logging.info("-- User has told rover to adjust route")
                    print ("Adjusting route")
                    currentY += 1
            elif stuckTester(marsMap) == "stuck in hole":
                print ("Rover problem:", stuckTester(marsMap))
                answer = input("What should I do: ")
                if (answer == "stop"):
                    logging.info("-- User has told rover to stop")
                    logging.info("-- Stopping")
                    print("Stopping...")
                    exit()
                elif (answer == "move"):
                    logging.info("-- User has told rover to adjust route")
                    print("Adjusting route")
                    currentY += 1
            elif stuckTester(marsMap) == "stuck in sand":
                print ("Rover problem:", stuckTester(marsMap))
                answer = input("What should I do: ")
                if (answer == "stop"):
                    logging.info("-- User has told rover to stop")
                    logging.info("-- Stopping")
                    print ("Stopping...")
                    exit()
                elif (answer == "move"):
                    logging.info("-- User has told rover to adjust route")
                    print("Adjusting route")
                    currentY += 1

        if (currentX == 8 and currentY == 8):
            logging.info("-- Finished route")
            logging.info("-- Stopping")
            print("Finshed route, Stopping...")
            exit()
        if (direction == 0):
            if currentX < 8:
                currentX += 1
            else:
                currentY += 1
                direction = 1
        elif (direction == 1):
            if currentX > 1:
                currentX -= 1
            else:
                currentY += 1
                direction = 0

        control = 1

        lock.notifyAll()
        lock.release()
        sleep(2)

"""
Wheel positions:
0-3
1*4
2-5
CurrentX & currentY are the center of the rover.
[0][0] is top left not botton left!
Must be passed:
    * The mars map 2d list
    * Number of the wheel.
    * Modification value for X coordinate
    * Modification value for Y coordinate
"""
def wheel(marsMap,num,modX,modY):
    global control

    file = open ("rover.txt","w")

    wheelLifted = 0 #represents if the wheel is lifted or not. 0 = on the ground, 1 = raised off the ground (used when over a rock)
    wheelTractn = 0 #represents if the wheel should spin or not. 0 = no spin, 1 = spin (used when over a hole)
    wheelTorque = 0 #represents if the wheel needs low or high torque. 0 = low torque, 1 = high torque (used when on sand)
    while True:
        lock.acquire()

        wheelX = currentX+modX
        wheelY = currentY+modY 
        mapResult = mapCheck(marsMap,wheelX,wheelY)

        #print("X:",wheelX,"Y:",wheelY,"Wheel",num,":",mapResult)

        if (mapResult == "clear"):
            wheelLifted = 0 
            wheelTractn = 1
            wheelTorque = 1
            #print ("Normal operation wheel:",num)
        elif (mapResult == "rock"):
            wheelLifted = 1
            wheelTractn = 1
            wheelTorque = 1
            print ("Raising wheel:",num)
            logging.info("-- Raising wheel:"+str(num))
        elif (mapResult == "hole"):
            wheelLifted = 0
            wheelTractn = 0
            wheelTorque = 0
            print ("Stopping wheel:",num,)
            logging.info("-- Stopping wheel:"+str(num))
        elif (mapResult == "sand"):
            wheelLifted = 0
            wheelTractn = 1
            wheelTorque = 0
            print ("Lowering torque wheel:",num)
            logging.info("-- Lowering torque wheel:"+str(num))

        elif (mapResult == "water"):
            wheelLifted = 1 
            wheelTractn = 0
            wheelTorque = 0
            print ("Raising and stopping wheel:",num)
            logging.info("-- Raising and stropping wheel:"+str(num))


        lock.notifyAll()
        lock.release()
        sleep(1)


"""
Menu for testing each wheel (not currently implemented)
Must be passed:
    * The mars map 2d list 
"""
def menu(marsMap):
    global control
    lock.acquire() 

    print("Which wheel would you like to check:\n1) Wheel 1\n2) Wheel 2\n3) Wheel 3\n4) Wheel 4\n5) Exit")
    answer = int(input("Enter:"))
    #print (type(answer))
    if (answer == 1):
        print ("1111")
        control = 1
        print (control)
    elif (answer == 2):
        control = 2
    elif (answer == 3):
         control = 3
    elif (answer == 4):
        control = 4
    elif (answer == 5):
        raise exit()
    else:
        print ("Please enter a valid entry (a,b,c,d)")
    control = 0
    lock.release()

marsMap = mapCreate(10,10) #calls the mapCreate function to make the map
for i in marsMap:
    print (i)

t1 = Thread(target=mainControl,args=(marsMap,))
t2 = Thread(target=wheel,args=(marsMap,0,-1,-1,)) #wheel
t3 = Thread(target=wheel,args=(marsMap,1,-1,0,)) #wheel2
t4 = Thread(target=wheel,args=(marsMap,2,-1,1,)) #wheel3
t5 = Thread(target=wheel,args=(marsMap,3,1,-1,)) #wheel4
t6 = Thread(target=wheel,args=(marsMap,4,1,0,)) #wheel5
t7 = Thread(target=wheel,args=(marsMap,5,1,1,)) #wheel6
t8 = Thread(target=menu,args=(marsMap,))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
