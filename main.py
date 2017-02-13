import threading
from threading import Lock
from threading import Thread
from time import sleep
cv = threading.Condition()
control = 0


def wheel1():
    global control
    while True:
        cv.acquire()
        if control == 1:
            
            sleep(0.3)
            print ("Thread: ",control)
            control = 0
        cv.notifyAll()
        cv.release()

def wheel2():
    global control
    while True:
        cv.acquire()
        if control == 2:
            
            sleep(0.3)
            print ("Thread: ",control)
            control = 0
        cv.notifyAll()
        cv.release()

def wheel3():
    global control
    while True:
        cv.acquire()
        if control == 3:
            sleep(0.3)
            print ("Thread: ",control)
            control = 0
        cv.notifyAll()
        cv.release()       

def wheel4():
    global control
    while True:
        cv.acquire()
        if control == 4:
            sleep(0.3)
            print("Thread: ",control)
            control = 0
        cv.notifyAll()
        cv.release()    

def menu():
    global control
    while True:
         if control == 0:   
            print("Which wheel would you like to check: \na) Wheel 1b) Thread 2\nc) Wheel 3\nd) Wheel 4")
            answer = input("Enter: ")
            if (answer == "a"):
                control = 1
            elif (answer == "b"):
                control = 2
            elif (answer == "c"):
                control = 3
            elif (answer == "d"):
                control = 4
            else:
                print ("Please enter a valid entry (a,b,c,d)")
                control = 0

t1 = Thread(target=wheel1,args=())
t2 = Thread(target=wheel2,args=())
t3 = Thread(target=wheel3,args=())
t4 = Thread(target=wheel4,args=())
t5 = Thread(target=menu,args=())
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()



