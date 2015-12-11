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
num = input("How many examples do you want? ")
stallCap = 10

#storageFile = "CandidateUp"+str(up)+"Down"+str(down)
storageFile = "dump"

def createCandidateExample():
    code = random.choice([[2], [-2]])
    orient = random.choice([[1], [-1]])
    K = ADT.ADT(code, orient)
    ups = 0
    upSequence = []
    while ups < up:
        M = ADTOp.simpleCoarseRandomOp(upMoveBias=1, horizontalMoveBias=1, downMoveBias=0, CCBias=0)
        if M.getDirection() == "U":
            ups += 1
        upSequence.append(M)
        print "Length of upSequence: ", len(upSequence)
#    for M in upSequence:
    for i in range(len(upSequence)):
        print "Performing up move: ", M.toString()
        print i
        M.apply(K)
        print "K has become: ", K.to_string()
        
    downs = 0
    stalled = 0
    while (downs, stalled) < (down, stallCap):
        simpleFinePossibleMoves = K.simpleFinePossibleMoves()
        simpleFinePossibleDownOrHorizontalMoves = [i for i in simpleFinePossibleMoves if i.getDirection() in ["D", "H"]]
        if len(simpleFinePossibleDownOrHorizontalMoves) == 0:
            print "K is: ", K.to_string()
            print "simpleFinePossibleMoves: \n"
            for i in simpleFinePossibleMoves:
                print i.toString()
            raise TypeError("There should be moves here.")
        M = random.choice(simpleFinePossibleDownOrHorizontalMoves)
        if M.getDirection() == "D":
            downs += 1
            stalled = 0
        else:
            stalled += 1
        M.apply(K)
        print "Now, going down, K has become: ", K.to_string()
    return K
    

current = 0
while current < num:
    current += 1
    L = createCandidateExample()
    myfile = open(storageFile, 'a')
    myfile.write(str(L.to_string()))
    myfile.write('\n')
    myfile.close()
