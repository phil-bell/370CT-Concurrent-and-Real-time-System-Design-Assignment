import threading
from threading import Lock
from threading import Thread
from time import sleep
from sys import exit
lock = threading.Condition()
control = 0
currentX = 1
currentY = 1

def mapCreate(w,h):
    mapToOut = [[0 for i in range(w)] for j in range(h)]
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


def mainControl(marsMap):
    global control
    while True:
        lock.acquire()
        print ("Main Control")
        sleep(0.1)
        control = 1
        lock.notifyAll()
        lock.release()

"""
Wheel positions:
1-4
2*5
3-6
currentX & currentY are the center of the rover
"""
def wheel1(marsMap):
    global control
    while True:
        lock.acquire()

        wheelX = currentX+1
        wheelY = currentY+1 
        print(mapCheck(marsMap,wheelX,wheelY))

        if (control == 1):
            sleep(0.1)
            control = 2
            print("Wheel: ",control)
            
        lock.notifyAll()
        lock.release()

def wheel2(marsMap):
    global control
    while True:
        lock.acquire() 
        sleep(0.1)
        control = 2
        print ("Wheel: ",control)
        lock.notifyAll()
        lock.release()

def wheel3(marsMap):
    global control
    while True:
        lock.acquire() 
        sleep(0.1)
        control = 3
        print("Wheel: ",control)
        lock.notifyAll()
        lock.release()       

def wheel4(marsMap):
    global control
    while True:
        lock.acquire() 
        sleep(0.1)
        print("Wheel: ",control)
        control = 4
        lock.notifyAll()
        lock.release()    

def wheel5(marsMap):
    global control
    while True:
        lock.acquire() 
        sleep(0.1)
        control = 5
        print("Wheel: ",control)
        lock.notifyAll()
        lock.release()  

def wheel6(marsMap):
    global control
    while True:
        lock.acquire() 
        sleep(0.1)
        control = 6
        print("Wheel: ",control)
        lock.notifyAll()
        lock.release()  

def menu(marsMap):
    global control
    lock.acquire() 

    print("Which wheel would you like to check: \n1) Wheel 1\n2) Wheel 2\n3) Wheel 3\n4) Wheel 4\n5) Exit")
    answer = int(input("Enter: "))
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

marsMap = mapCreate(10,10)
print (marsMap)

t1 = Thread(target=mainControl,args=(marsMap,))
t2 = Thread(target=wheel1,args=(marsMap,))
t3 = Thread(target=wheel2,args=(marsMap,))
t4 = Thread(target=wheel3,args=(marsMap,))
t5 = Thread(target=wheel4,args=(marsMap,))
t6 = Thread(target=menu,args=(marsMap,))
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
#t6.start()
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
#t6.join()



