#!/usr/bin/env python3.4

from math import *
import random

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
        zombieHorde.append(zombie)
    return zombieHorde

if __name__ == "__main__":
    main()
