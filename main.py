import threading
import random
from threading import Lock
from threading import Thread
from time import sleep
from sys import exit
lock = threading.Condition() #thread condition var
control = 0 #global control value
currentX = 1 #global for X position of the rover
currentY = 1 #global for Y position of the rover

"""
makes the map that the rover moves around, it is a 2 dimentional list (Matrix).
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
0 = normal ground
1 = rock (blocked)
2 = hole (freewheeling)
3 = sand (sinking)
4 = water (Mission Success)
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
Main control thread that manages rover movement. Uses
the global vars currentX and currentY
"""
def mainControl(marsMap):
    global control
    while True:
        lock.acquire()

        print ("Rover locaton X:",currentX,"Y:",currentY)

        control = 1

        lock.notifyAll()
        lock.release()
        sleep(1)

"""
Wheel positions:
1-4
2*5
3-6
CurrentX & currentY are the center of the rover.
[0][0] is top left not botton left!
Must be passed the map, number of the wheel and the 
location of the wheel in relation center of the rover.
"""
def wheel1(marsMap,num,modX,modY):
    global control
    wheelLifted = 0 #represents if the wheel is lifted or not. 0 = on the ground, 1 = raised off the ground (used when over a rock)
    wheelTractn = 0 #represents if the wheel should spin or not. 0 = no spin, 1 = spin (used when over a hole)
    wheelTorque = 0 #represents if the wheel needs low or high torque. 0 = low torque, 1 = high torque (used when on sand)
    while True:
        lock.acquire()

        wheelX = currentX+modX
        wheelY = currentY+modY 
        mapResult = mapCheck(marsMap,wheelX,wheelY)

        print("X:",wheelX,"Y:",wheelY,"Wheel",num,":",mapResult)
        
        if (mapResult == "clear"):
            wheelLifted = 0 
            wheelTractn = 1
            wheelTorque = 1
        elif (mapResult == "rock"):
            wheelLifted = 1
            wheelTractn = 1
            wheelTorque = 1
        elif (mapResult == "hole"):
            wheelLifted = 0
            wheelTractn = 0
            wheelTorque = 0
        elif (mapResult == "sand"):
            wheelLifted = 0
            wheelTractn = 1
            wheelTorque = 0
        elif (mapResult == "water"):
            wheelLifted = 1 
            wheelTractn = 0
            wheelTorque = 0
            

        lock.notifyAll()
        lock.release()
        sleep(1)


"""
menu for testing each wheel (not currently implemented)
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
        raise SystemExit()
    else:
        print ("Please enter a valid entry (a,b,c,d)")
    control = 0
    lock.release()

marsMap = mapCreate(10,10) #calls the mapCreate function to make the map
for i in marsMap:
    print (i)

t1 = Thread(target=mainControl,args=(marsMap,))
t2 = Thread(target=wheel1,args=(marsMap,1,-1,-1,)) #wheel1
t3 = Thread(target=wheel1,args=(marsMap,2,-1,0,)) #wheel2
t4 = Thread(target=wheel1,args=(marsMap,3,-1,1,)) #wheel3
t5 = Thread(target=wheel1,args=(marsMap,4,1,-1,)) #wheel4
t6 = Thread(target=wheel1,args=(marsMap,5,1,0,)) #wheel5
t7 = Thread(target=wheel1,args=(marsMap,6,1,1,)) #wheel6
t8 = Thread(target=menu,args=(marsMap,))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()



"""def wheel2(marsMap):
    global control
    while True:
        lock.acquire()

        wheelX = currentX-1
        wheelY = currentY

        print("Wheel 2:",mapCheck(marsMap,wheelX,wheelY))

        lock.notifyAll()
        lock.release()
        sleep(0.5)

def wheel3(marsMap):
    global control
    while True:
        lock.acquire()

        wheelX = currentX-1
        wheelY = currentY+1 

        print("Wheel 3:",mapCheck(marsMap,wheelX,wheelY))

        lock.notifyAll()
        lock.release()
        sleep(0.5)

def wheel4(marsMap):
    global control
    while True:
        lock.acquire()

        wheelX = currentX+1
        wheelY = currentY-1 

        print("Wheel 4:",mapCheck(marsMap,wheelX,wheelY))

        lock.notifyAll()
        lock.release()
        sleep(0.5)
  

def wheel5(marsMap):
    global control
    while True:
        lock.acquire()

        wheelX = currentX+1
        wheelY = currentY

        print("Wheel 5:",mapCheck(marsMap,wheelX,wheelY))

        lock.notifyAll()
        lock.release()
        sleep(0.5)

def wheel6(marsMap):
    global control
    while True:
        lock.acquire()

        wheelX = currentX+1
        wheelY = currentY+1 

        print("Wheel 6:",mapCheck(marsMap,wheelX,wheelY))

        lock.notifyAll()
        lock.release()
        sleep(0.5)
"""