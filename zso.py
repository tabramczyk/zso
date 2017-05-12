#!/usr/bin/env python3.4

from math import *
import random
from statistics import variance

dimensionsNum = 1
searchRange = 1. # could be use to initialization only or to making walk range in iterations (dependent on knowledge about a position of best fitness or not)
thresholdVal = 2.5 # could be dependent on average fitness
HordeSize = 100
WalkingDeadSpeed = 0.01 # could be dependent on searchRange
ApocalipseIteration = 100


def main():
    global thresholdVal, HordeSize, WalkingDeadSpeed
    zombieHorde = initZombies(HordeSize)
    print(executeZSO(zombieHorde, fun, thresholdVal, WalkingDeadSpeed, ApocalipseIteration))

def fun(x):
    return sqrt(0.5*abs(x))*cos(x)+sqrt(abs(x))
    # return x*sin(10.*3.14159*x)+1.

def initZombies(n): # initialize n zombies
    global dimensionsNum, searchRange
    zombieHorde = []
    for i in range(n):
        zombie = {}
        location = [random.uniform(-searchRange,searchRange) for i in range(dimensionsNum)]
        direction = [random.uniform(-1,1) for i in range(dimensionsNum)]
        zombie.setdefault("location", location)
        zombie.setdefault("direction", direction)
        zombie.setdefault("is_human", False)
        zombieHorde.append(zombie)
    return zombieHorde	

def distance(locA, locB):
    return sqrt(sum(tuple((locB[i]-locA[i])**2 for i in range(len(locA)))))

def executeZSO(zombiesVec, fitnessFunc, thresholdVal, speed, generationsNum):
    # zombies hunt for humans
    global dimensionsNum
    bestFitness = fitnessFunc(*(dimensionsNum*[0.0]))
    for _ in range(generationsNum):
        dirVariance = [variance(z["direction"][dim] for z in zombiesVec) for dim in range(dimensionsNum)]
        for zombie in zombiesVec:
            for i in range(dimensionsNum):
                zombie["location"][i] += zombie["direction"][i]*dirVariance[i]*speed
            fitnessVal = fitnessFunc(*zombie["location"])
            bestFitness = fitnessVal if fitnessVal > bestFitness else bestFitness
            # search exploitation mode (human)
            if fitnessVal < thresholdVal: 
                zombie["is_human"] = True
                # gradient ascent search of local neighborhood
                if len(tuple(filter(lambda z: (not z["is_human"]) and (distance(z["location"], zombie["location"]) < speed), zombiesVec))):
                    # bitten by zombie
                    zombie["is_human"] = False
            else:
                humans = tuple(z for z in zombiesVec if z["is_human"])
                if len(humans):
                    # find closest human h
                    closestHuman = min(humans, key=lambda h: distance(h["location"], zombie["location"]))
                    dirVecLen = distance(closestHuman["location"], zombie["location"])
                    if dirVecLen == 0:  # temporary divbyzero-repair
                        dirVecLen = 0.01*speed 
                    for i in range(dimensionsNum):
                        zombie["direction"][i] = (closestHuman["direction"][i]-zombie["direction"][i]) / dirVecLen * speed
    return bestFitness

if __name__ == "__main__":
    main()
