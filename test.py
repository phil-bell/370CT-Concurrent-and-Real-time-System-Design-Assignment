import time
import random
import os

def mapCreate(w,h):
    mapToOut = [[0 for i in range(w)] for j in range(h)]
    for i in range(0,40):
        genX = random.randint(0,9)
        genY = random.randint(0,9)
        if mapToOut[genX][genY] == 0:
            mapToOut[genX][genY] = random.randint(1,3)
    mapToOut[genX][genY] = 4
    return mapToOut

while True:
    os.system("cls")
    print ("\n".join("".join(str(row)) for row in mapCreate(10,10)))
    time.sleep(1)