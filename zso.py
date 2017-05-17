#!/usr/bin/env python3.4

from math import *
import random
from statistics import variance

dimensionsNum = 1
searchRange = 10 # could be use to initialization only or to making walk range in iterations (dependent on knowledge about a position of best fitness or not)
thresholdVal = 2.5 # could be dependent on average fitness
HordeSize = 100
WalkingDeadSpeed = 0.05 # could be dependent on searchRange
ApocalipseIteration = 100


# main function
def main():

    global thresholdVal, HordeSize, WalkingDeadSpeed
    zombieHorde = initZombies(HordeSize)

    print("'fun' function:")
    bestFitness, bestZombie = executeZSO(zombieHorde, fun, thresholdVal, WalkingDeadSpeed, ApocalipseIteration)
    print("Best fitness: ", bestFitness)
    print("Location: ", bestZombie['location'])

# temporary function
def fun(x):
    return sqrt(0.5*abs(x))*cos(x)+sqrt(abs(x))

# basic functions
def bent_cigar(*xs):
    return x[0]**2 + (10**6)*sum(tuple((x**2 for x in xs[1:])))

def rosenbrock(*xs):
    return sum(tuple(100*(x[i]**2-x[i+1])**2 + (x[i]-1)**2 for i in range(len(xs)-1)))

def rastrigin(*xs):
    return sum(tuple(x[i]**2 - 10*cos(2*pi*x[i]) + 10 for i in range(len(xs)))) 

def zakharov(*xs):
    return sum(tuple(x**2 for x in xs)) + (0.5*sum(tuple(x for x in xs)))**2 + (0.5*sum(tuple(x for x in xs)))**4

# shifted and rotated functions
def shifted_and_rotated_bent_cigar(*xs): # No. 1, optimum = 100
    pass

def shifted_and_rotated_rosenbrock(*xs): # No. 4, optimum = 400
    pass

def shifted_and_rotated_rastrigin(*xs): # No. 5, optimum = 500
    pass

def shifted_and_rotated_zakharov(*xs): # No. 3, optimum = 300
    pass

def shiftFunction(x_list, o_list): # return shifted x list, o_list - shifted global optimum list
    new_x_list = []
    for i in range(len(x_list)):
        new_x_list.append(x_list[i]-o_list[i])
    return new_x_list

def rotateFunc(x_list, M): # return rotated x list, M - rotation matrix
    new_x_list = [0 for _ in range(len(x_list))]
    for i in range(len(x_list)):
        for j in range(len(x_list)):
            new_x_list[i] += x_list[j]*M[i*len(x_list)+j]
    return new_x_list

# zombie horde initialization
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

# algorithm's execution
def executeZSO(zombiesVec, fitnessFunc, thresholdVal, speed, generationsNum):

    # zombies hunt for humans
    global dimensionsNum
    bestFitness = fitnessFunc(*zombiesVec[0]['location'])
    bestZombie = None

    for _ in range(generationsNum):

        dirVariance = [variance(z["direction"][dim] for z in zombiesVec) for dim in range(dimensionsNum)]

        for zombie in zombiesVec:

            for i in range(dimensionsNum):
                zombie["location"][i] += zombie["direction"][i]*dirVariance[i]*speed

            fitnessVal = fitnessFunc(*zombie["location"])
            bestFitness = fitnessVal if fitnessVal < bestFitness else bestFitness
            bestZombie = zombie if fitnessVal == bestFitness else bestZombie

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

    return bestFitness, bestZombie

	
if __name__ == "__main__":
    main()
