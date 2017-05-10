#!/usr/bin/env python3.4

from math import *
import random
from statistics import variance

funParameters = 1
searchRange = 30

def main():
    print(initZombies(2))

def fun(x):
    return sqrt(0.5*abs(x))*cos(x)+sqrt(abs(x))

def initZombies(n): # initialize n zombies
    global funParameters, searchRange
    zombieHorde = []
    for i in range(n):
        zombie = {}
        location = [random.uniform(-searchRange,searchRange) for i in range(funParameters)]
        direction = [random.uniform(-1,1) for i in range(funParameters)]
        zombie.setdefault("location", location)
        zombie.setdefault("direction", direction)
        zombie.setdefault("is_human", False)
        zombieHorde.append(zombie)
    return zombieHorde	

def distance(locA, locB):
    return sqrt(sum(tuple((locB[i]-locA[i])**2 for i in range(len(locA)))))

def executeZSO(zombiesVec, fitnessFunc, dimensionsNum, thresholdVal, speedVec, generationsNum):
    # zombies hunt for humans
    for _ in range(generationsNum):
        dirVariance = [variance(z["direction"][dim] for z in zombiesVec) for dim in range(dimensionsNum)]
        for zombie in zombiesVec:
            for i in range(dimensionsNum):
                zombie["location"][i] += zombie["location"][i] + zombie["direction"][i]*dirVariance[i]*speedVec[i]
            fitnessVal = fitnessFunc(*zombie["location"])
            # search exploitation mode (human)
            if fitnessVal > thresholdVal: 
                zombie["is_human"] = True
                # gradient ascent search of local neighborhood
                speedVecLen = sqrt(sum(tuple(speed[i]*speed[i] for i in range(dimensionsNum))))
                if len(tuple(filter(lambda z: (not z["is_human"]) and (distance(z["location"],zombie["location"])<speedVecLen), zombies))):
                    # bitten by zombie
                    z["is_human"] = False

if __name__ == "__main__":
    main()
