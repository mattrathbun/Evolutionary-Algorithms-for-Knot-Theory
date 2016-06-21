import os, sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpPopulation, ADTOpPopulationSets, Fit
import AllDiagrams
from datetime import datetime
import random

AllDiagrams.init()


def createCandidateExample(height=5, drop=1):

    code = random.choice([[2], [-2]])
    orient = random.choice([[1], [-1]])
    K = ADT.ADT(code, orient)
    upSequence = []
    L = K.copy()
#    ups = 0
    while L.number_crossings() < height:
        M = ADTOp.simpleCoarseRandomOp(upMoveBias=1, horizontalMoveBias=1, downMoveBias=0, CCBias=0)
#        if M.getDirection() == "U":
#            ups += 1
#            print "ups is {}".format(ups)
#        upSequence.append(M)
        print "Applying {} to {}.".format(M.toString(), L.to_string())
        M.apply(L)
        print "K has become: ", L.to_string()
    print "K has been built up, and now has {} crossings.".format(L.number_crossings())
    dropped = 0
    all_possible_moves = L.finePossibleMoves()
    all_possible_down_or_horizontal_moves = [move for move in all_possible_moves if move.direction in ["D", "H"]]
    while dropped < drop and len(all_possible_down_or_horizontal_moves) > 0:
        simple_possible_down_or_horizontal_moves = [move for move in L.simpleFinePossibleMoves() if move.direction in ["D", "H"]]
        while len(simple_possible_down_or_horizontal_moves) == 0:
            L.shiftLabel()
            simple_possible_down_or_horizontal_moves = [move for move in L.simpleFinePossibleMoves() if move.direction in ["D", "H"]]
        M = random.choice(simple_possible_down_or_horizontal_moves)
        print "Applying {} to {}.".format(M.toString(), L.to_string())
        M.apply(L)
        if M.getDirection() == "D":
            dropped += 1
            print "drops is {}".format(dropped)
        print "Now, K has become: ", L.to_string()
        possible_moves = L.simpleFinePossibleMoves()
        possible_down_or_horizontal_moves = [move for move in possible_moves if move.direction in ["D", "H"]]
    print "K has been dropped down, and now has {} crossings.".format(L.number_crossings())

    all_possible_moves = L.finePossibleMoves()
    all_possible_down_or_horizontal_moves = [move for move in all_possible_moves if move.direction in ["D", "H"]]
    if len(all_possible_down_or_horizontal_moves) > 0:
        print "This is not a hard diagram."
        return False, L
    else:
        print "THIS IS A HARD DIAGRAM!"
        print L.to_string()
        return True, L


#storageFile = "CandidateUp"+str(up)+"Down"+str(down)
storageFile = "SimpleHardDiagrams"
 
 
#height = input("How far up should we climb (in crossings)? ")
#drop = input("How far down should we drop? ")

while True:
    p = random.randint(10,30)
    q = random.randint(2,p/2)
    success, L = createCandidateExample(p, q)
    print success
    print L.to_string()
    if success and L.number_crossings() > 3:
        myfile = open(storageFile, 'a')
        myfile.write(str(L.to_string()))
        myfile.write('\n')
        myfile.close()



# current = 0
# while current < num:
#     current += 1
#     L = createCandidateExample()
#     myfile = open(storageFile, 'a')
#     myfile.write(str(L.to_string()))
#     myfile.write('\n')
#     myfile.close()
