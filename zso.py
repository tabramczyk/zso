#!/usr/bin/env python3.4

from math import *
import random
from statistics import variance

dimensionsNum = 10
searchRange = 100 # could be use to initialization only or to making walk range in iterations (dependent on knowledge about a position of best fitness or not)
thresholdVal = None # could be dependent on average fitness
HordeSize = 100
WalkingDeadSpeed = 1.5 # could be dependent on searchRange 
ApocalipseIteration = 100000

# main function
def main():

    global thresholdVal, HordeSize, WalkingDeadSpeed
    zombieHorde = initZombies(HordeSize)

    o1, M1 = loadShiftAndRotationData("shuffle_data_1_D10.txt", "M_1_D10.txt")
    # print(o1)
    # print(M1)
    o3, M3 = loadShiftAndRotationData("shuffle_data_3_D10.txt", "M_3_D10.txt")
    # print(o3)
    # print(M3)
    o4, M4 = loadShiftAndRotationData("shuffle_data_4_D10.txt", "M_4_D10.txt")
    # print(o4)
    # print(M4)
    o5, M5 = loadShiftAndRotationData("shuffle_data_5_D10.txt", "M_5_D10.txt")
    # print(o5)
    # print(M5)

    # print("'fun' function:")
    # bestFitness, bestZombie = executeZSO(zombieHorde, fun, None, None, 0, thresholdVal, WalkingDeadSpeed)
    # print("Best fitness: ", bestFitness)
    # print("Location: ", bestZombie['location'])

    # print("'shifted and rotated bent cigar' function:")
    # bestFitness, bestZombie = executeZSO(zombieHorde, shifted_and_rotated_bent_cigar, o1, M1, 100, thresholdVal, WalkingDeadSpeed)
    # print("Best fitness: ", bestFitness)
    # print("Location: ", bestZombie['location'])

    # print("'shifted and rotated rosenbrock' function:")
    # bestFitness, bestZombie = executeZSO(zombieHorde, shifted_and_rotated_rosenbrock, o4, M4, 400, thresholdVal, WalkingDeadSpeed)
    # print("Best fitness: ", bestFitness)
    # print("Location: ", bestZombie['location'])

    # print("'shifted and rotated rastrigin' function:")
    # bestFitness, bestZombie = executeZSO(zombieHorde, shifted_and_rotated_rastrigin, o5, M5, 500, thresholdVal, WalkingDeadSpeed)
    # print("Best fitness: ", bestFitness)
    # print("Location: ", bestZombie['location'])

    print("'shifted and rotated zakharov' function:")
    bestFitness, bestZombie = executeZSO(zombieHorde, shifted_and_rotated_zakharov, o3, M3, 300, thresholdVal, WalkingDeadSpeed)
    print("Best fitness: ", bestFitness)
    print("Location: ", bestZombie['location'])

# temporary function
def fun(x, os=None, M=None, F_best=None):
    return sqrt(0.5*abs(x[0]))*cos(x[0])+sqrt(abs(x[0]))

# basic functions
def bent_cigar(xs):
    return xs[0]**2 + (10**6)*sum(tuple((x**2 for x in xs[1:])))

def rosenbrock(xs):
    return sum(tuple(100*(x[i]**2-x[i+1])**2 + (x[i]-1)**2 for i in range(len(xs)-1)))

def rastrigin(xs):
    return sum(tuple(xs[i]**2 - 10*cos(2*pi*xs[i]) + 10 for i in range(len(xs)))) 

def zakharov(xs):
    return sum(tuple(x**2 for x in xs)) + (0.5*sum(tuple(x for x in xs)))**2 + (0.5*sum(tuple(x for x in xs)))**4

# shifted and rotated functions
def shifted_and_rotated_bent_cigar(xs, os, M, F_best=100): # No. 1, optimum = 100
    return bent_cigar(rotateFunc(shiftFunc(xs, os), M)) + F_best

def shifted_and_rotated_rosenbrock(xs, os, M, F_best=400): # No. 4, optimum = 400
    return rosenbrock(tuple(map(lambda y: y+1, rotateFunc(tuple(map(lambda x: 0.02048*x, shiftFunc(xs, os))), M)))) + F_best

def shifted_and_rotated_rastrigin(xs, os, M, F_best=500): # No. 5, optimum = 500
    return rastrigin(rotateFunc(shiftFunc(xs, os), M)) + F_best

def shifted_and_rotated_zakharov(xs, os, M, F_best=300): # No. 3, optimum = 300
    return zakharov(rotateFunc(shiftFunc(xs, os), M)) + F_best

def shiftFunc(x_list, o_list): # return shifted x list, o_list - shifted global optimum list
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

def loadShiftAndRotationData(shiftFilePath, rotationFilePath):
    with open(shiftFilePath) as sf, open(rotationFilePath) as rf:
        o_list = [float(s) for s in sf.readline().split("	")]
        r_matrix = list(map(lambda s: float(s), tuple(filter(lambda s: s!='', rf.read().split(" ")))))
        # r_matrix = list(
            # map(
            #    lambda str_row: list(map(lambda s: float(s), str_row)), 
            #    tuple(map(lambda row_str: tuple(filter(lambda s: s!='', row_str.split(" "))), rf.readlines()))
            # ))
    return o_list, r_matrix
	
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
def executeZSO(zombiesVec, fitnessFunc, os, M, F_best, thresholdVal, speed):

    # zombies hunt for humans
    global dimensionsNum, ApocalipseIteration
    bestFitness = fitnessFunc(zombiesVec[0]['location'], os, M)
    worstFitness = fitnessFunc(zombiesVec[0]['location'], os, M)
    bestZombie = None
    generationsNum = 0

    while generationsNum < ApocalipseIteration and abs(bestFitness-F_best) >= 1e-8:

        generationsNum += 1
        print(generationsNum, bestFitness, F_best, abs(bestFitness-F_best))

        dirVariance = [variance(z["direction"][dim] for z in zombiesVec) for dim in range(dimensionsNum)]

        for zombie in zombiesVec:
            # print(zombie['location'])
            for i in range(dimensionsNum):
                zombie["location"][i] += zombie["direction"][i]*dirVariance[i]*speed
                # if not (searchRange > zombie["location"][i] > -searchRange):
                # zombie["location"][i] = -zombie["location"][i]

            fitnessVal = fitnessFunc(zombie["location"], os, M)
            bestFitness = fitnessVal if fitnessVal < bestFitness else bestFitness
            bestZombie = zombie if fitnessVal == bestFitness else bestZombie

            # search exploitation mode (human)
            #alpha = 0.5
            # thresholdVal = (1+alpha) * (sum(tuple((fitnessFunc(z["location"], os, M)) for z in zombiesVec)) / len(zombiesVec))
            thresholdVal = (bestFitness + worstFitness) / 2
            if fitnessVal < thresholdVal: 
                #print("xd 1")
                zombie["is_human"] = True
                # gradient ascent search of local neighborhood
                if len(tuple(filter(lambda z: (not z["is_human"]) and (distance(z["location"], zombie["location"]) < speed), zombiesVec))):
                    # bitten by zombie
                    zombie["is_human"] = False
                    #print("xd 1.1")
            else:
                #print("xd 2")
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
