import os, sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpPopulation, ADTOpPopulationSets, Fit
import AllDiagrams
from datetime import datetime
import random

AllDiagrams.init()

storageFile = "SimpleHardDiagramsMessy"

def fetchDownHorizontalMoves(knot):
    all_possible_moves = knot.finePossibleMoves()
    return [move for move in all_possible_moves if move.direction in ["D", "H"]]
    
def fetchDownMoves(knot):
    all_possible_moves = knot.finePossibleMoves()
    return [move for move in all_possible_moves if move.direction in ["D"]]
    
def resultDownHorizontalMoves(knot):
    all_possible_down_or_horizontal_moves = fetchDownHorizontalMoves(knot)
    results = []
    for move in all_possible_down_or_horizontal_moves:
        K = knot.copy()
        if move.apply(K):
            results.append(K)
    return results

def cascadeDownResults(knot):
    K = knot.copy()
    print "Investigating diagrams with {} crossings. \n".format(K.number_crossings())
    below = resultDownMoves(K)
    if below == []:
        return K
    elif K.number_crossings() < 9:
        return K
    else:
        for L in below:
            print "There are {} diagrams below the current diagram. \n".format(len(below))
            return cascadeDownResults(L)

def resultDownMoves(knot):
    all_possible_down_moves = fetchDownMoves(knot)
    results = []
    for move in all_possible_down_moves:
        K = knot.copy()
        if move.apply(K):
            results.append(K)
    return results

def createCandidateExample(height=15, drop=1):
    candidates = []
    hardUnknotCount = 0
    code = random.choice([[2], [-2]])
    orient = random.choice([[1], [-1]])
    top = ADT.ADT(code, orient)
    upSequence = []
#    ups = 0
    print "Starting to increase complexity. \n"
    while top.number_crossings() < height:
        M = ADTOp.simpleCoarseRandomOp(upMoveBias=2, horizontalMoveBias=3, downMoveBias=1, CCBias=0)
#        if M.getDirection() == "U":
#            ups += 1
#            print "ups is {}".format(ups)
#        upSequence.append(M)
#        print "Applying {} to {}.".format(M.toString(), L.to_string())
        M.apply(top)
        print "Top Knot has {} crossings. \n".format(top.number_crossings())
#        print "K has become: ", L.to_string()
#    print "K has been built up, and now has {} crossings.".format(L.number_crossings())
    dropped = 0
    L = top.copy()
    for i in range(drop):
        dropped = resultDownHorizontalMoves(L)
    initial_counter = 1
    for diag in dropped:
        print "Checking {} out of {}.".format(initial_counter, len(dropped))
        initial_counter += 1
        candidates.append(cascadeDownResults(diag))
    print "There are {} candidates for hard unknot diagrams.\n".format(len(candidates))
#     for d in candidates:
#         print d.to_string()
    print "Now checking for False Positives.\n"
    hard_diagrams = [d for d in candidates if d.number_crossings() > 9]
    l = len(hard_diagrams)
    print "Found {} hard unknot diagrams.".format(l)
    if l > 0:
        myfile = open(storageFile, 'a')
        for d in hard_diagrams:
            myfile.write(str(d.to_string()))
            myfile.write('\n')
        myfile.close()
        # reductions = fetchDownMoves(diag)
#         if len(reductions) == 0:
#             hardUnknotCount += 1
#             myfile = open(storageFile, 'a')
#             myfile.write(str(diag.to_string()))
#             myfile.write('\n')
#             myfile.close()
#         else:
#             print "Has a reduction. \n"
#             print reductions[0].toString()
#     print "Found {} hard unknot diagrams.".format(hardUnknotCount)

iterations = 10000
for i in range(iterations):
    p = random.randint(10, 30)
    print "On iteration {} of {}.\n".format(i, iterations)
    createCandidateExample(height=p, drop=1) 
        
#     all_possible_moves = peak.finePossibleMoves()
#     all_possible_down_or_horizontal_moves = [move for move in all_possible_moves if move.direction in ["D", "H"]]
#     for move in all_possible_down_or_horizontal_moves:
#         L
#     while dropped < drop and len(all_possible_down_or_horizontal_moves) > 0:
#         simple_possible_down_or_horizontal_moves = [move for move in L.simpleFinePossibleMoves() if move.direction in ["D", "H"]]
#         while len(simple_possible_down_or_horizontal_moves) == 0:
#             L.shiftLabel()
#             simple_possible_down_or_horizontal_moves = [move for move in L.simpleFinePossibleMoves() if move.direction in ["D", "H"]]
#         M = random.choice(simple_possible_down_or_horizontal_moves)
#         print "Applying {} to {}.".format(M.toString(), L.to_string())
#         M.apply(L)
#         if M.getDirection() == "D":
#             dropped += 1
#             print "drops is {}".format(dropped)
#         print "Now, K has become: ", L.to_string()
#         possible_moves = L.simpleFinePossibleMoves()
#         possible_down_or_horizontal_moves = [move for move in possible_moves if move.direction in ["D", "H"]]
#     print "K has been dropped down, and now has {} crossings.".format(L.number_crossings())
# 
#     all_possible_moves = L.finePossibleMoves()
#     all_possible_down_or_horizontal_moves = [move for move in all_possible_moves if move.direction in ["D", "H"]]
#     if len(all_possible_down_or_horizontal_moves) > 0:
#         print "This is not a hard diagram."
#         return False, L
#     else:
#         print "THIS IS A HARD DIAGRAM!"
#         print L.to_string()
#         return True, L


#storageFile = "CandidateUp"+str(up)+"Down"+str(down)

 
 
#height = input("How far up should we climb (in crossings)? ")
#drop = input("How far down should we drop? ")

# while True:
#     p = random.randint(10,30)
#     q = random.randint(2,p/2)
#     success, L = createCandidateExample(p, q)
#     print success
#     print L.to_string()
#     if success and L.number_crossings() > 3:
#         myfile = open(storageFile, 'a')
#         myfile.write(str(L.to_string()))
#         myfile.write('\n')
#         myfile.close()



# current = 0
# while current < num:
#     current += 1
#     L = createCandidateExample()
#     myfile = open(storageFile, 'a')
#     myfile.write(str(L.to_string()))
#     myfile.write('\n')
#     myfile.close()
