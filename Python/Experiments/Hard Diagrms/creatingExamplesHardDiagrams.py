import os, sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpPopulation, ADTOpPopulationSets, Fit
import AllDiagrams
from datetime import datetime
import random

AllDiagrams.init()

up = input("How many up moves should be performed? ")
down = input("How many down moves should be performed? ")

storageFile = "Up"+str(up)+"Down"+str(down)

def createCandidateExample():
    K = ADT.ADT([], [])
    ups = 0
    upSequence = []
    while ups < up:
        M = ADTOp.simpleCoarseRandomOp(upMoveBias=1, horizontalMoveBias=1, downMoveBias=0, CCBias=0)
        if M.getDirection() == "U":
            ups += 1
        upSequence.append(M)
    for M in upSequence:
        print "Performing up move: ", M.toString()
        M.apply(K)
        print "K has become: ", K.to_string()
    downs = 0
    while downs < down:
        simpleFinePossibleMoves = K.simpleFinePossibleMoves()
        simpleFinePossibleDownMoves = [i for i in simpleFinePossibleMoves if i.getDirection() == "D"]
        if len(simpleFinePossibleDownMoves) == 0:
            print "simpleFinePossibleMoves: \n"
            for i in simpleFinePossibleMoves:
                print i.toString()
            raise TypeError("There should be down moves here.")
        random.choice(simpleFinePossibleDownMoves).apply(K)
        downs += 1
    return K