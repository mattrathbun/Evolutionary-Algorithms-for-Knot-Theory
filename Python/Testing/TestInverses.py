import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ADT
import ADTOp


def findInverse(diagram, op):
    print "findInverse is being called right now."
    K = diagram.copy()
    n = K.number_crossings()
    number = op.getNumber()
    direction = op.getDirection()
    if direction == "U":
        reverse = "D"
    elif direction == "D":
        reverse = "U"
    elif direction == "H":
        reverse = "H"
    if op.apply(K):
        print "op.apply(K) seemed to work"
        if K.number_crossings() <= 1 and op.getNumber() == 2:
            print "Returning not None."
            return ADTOp.ADTOp(2, "U")
        if K.number_crossings() == 0 and op.getNumber() == 1:
            print "Returning not None."
            return ADTOp.ADTOp(1, "U")
        possible_moves = K.finePossibleMoves()
        for move in possible_moves:
            print "Checking {} in possible_moves".format(move.toString())
            if move.getNumber() == number and move.getDirection() == reverse:
                Ktemp = K.copy()
                move.apply(Ktemp)
                if diagram.sameDiagram(Ktemp):
                    print "move is not None, I think."
                    return move
        print "Done cycling through possible_moves"
        if op.getNumber() == 2 and op.getDirection() == "D":
            print "Doing final check to see if we had an 'irreverisble' R2Down move"
            arc = op.getData()['arc']
            for s in ["L", "R"]:
                for i in [1, -1]:
                    if len(diagram.regions(diagram.wrap(arc + i), s)) == 1:
                        print "Returning not None."
                        return ADTOp.ADTOp('1 & 1', "U")
            print "Nothing got returned."
        print "Nothing is being returned."
    else:
        print "About to return None in TestInverses function findInverse"
        return None



# K = ADT.ADT([2,-6,-4,-8],[1,-1,1,-1])
# M = ADTOp.ADTOp(3, 'H', {'arc': 8, 'side':'L'})
# 
# N = findInverse(K, M)
# print N.toString()

## Most recent error:
# Just about to call findInverse on diagram ([20, -22, 4, -8, 14, -10, 12, -6, -16, 18, -2], [-1, 1, -1, -1, 1, 1, 1, -1, 1, 1, 1]), with move 3H(pos=20, side=R)
# findInverse is being called right now.
# Trying to apply move:  3H(pos=20, side=R)
# to diagram:  ('20, -22, 4, -8, 14, -10, 12, -6, -16, 18, -2', '-1, 1, -1, -1, 1, 1, 1, -1, 1, 1, 1')
# code:
# a/ap 20 1 1 -1
# b/bp 21 2 -1 1
# c/cp 22 3 -1 1
# op.apply(K) seemed to work
# Checking 1U(pos=1, side=L, sign=1) in possible_moves
# Checking 1U(pos=1, side=L, sign=-1) in possible_moves
# Checking 1U(pos=1, side=R, sign=1) in possible_moves
# Checking 1U(pos=1, side=R, sign=-1) in possible_moves
# Checking 1D(pos=1) in possible_moves
# Checking 2U(pos=1, side=L, target=[1, 22]) in possible_moves
# Checking 2U(pos=1, side=L, target=[21, 22]) in possible_moves
# Checking 2U(pos=1, side=L, target=[21, 20]) in possible_moves
# Checking 2U(pos=1, side=L, target=[3, 4]) in possible_moves
# Checking 2U(pos=1, side=L, target=[5, 6]) in possible_moves
# Checking 2U(pos=1, side=L, target=[15, 14]) in possible_moves
# Checking 2U(pos=1, side=L, target=[9, 10]) in possible_moves
# Checking 2U(pos=1, side=L, target=[11, 12]) in possible_moves
# Checking 2U(pos=1, side=L, target=[13, 12]) in possible_moves
# Checking 2U(pos=1, side=L, target=[13, 14]) in possible_moves
# Checking 2U(pos=1, side=L, target=[9, 8]) in possible_moves
# Checking 2U(pos=1, side=L, target=[7, 8]) in possible_moves
# Checking 2U(pos=1, side=L, target=[7, 6]) in possible_moves
# Checking 2U(pos=1, side=L, target=[15, 16]) in possible_moves
# Checking 2U(pos=1, side=L, target=[17, 18]) in possible_moves
# Checking 2U(pos=1, side=L, target=[19, 18]) in possible_moves
# Checking 2U(pos=1, side=L, target=[19, 20]) in possible_moves
# Checking 2U(pos=1, side=L, target=[3, 2]) in possible_moves
# Checking 1U(pos=2, side=L, sign=1) in possible_moves
# Checking 1U(pos=2, side=L, sign=-1) in possible_moves
# Checking 1U(pos=2, side=R, sign=1) in possible_moves
# Checking 1U(pos=2, side=R, sign=-1) in possible_moves
# Checking 2U(pos=2, side=L, target=[20, 21]) in possible_moves
# Checking 2U(pos=2, side=L, target=[22, 1]) in possible_moves
# Checking 2U(pos=2, side=R, target=[20, 19]) in possible_moves
# Checking 2U(pos=2, side=R, target=[18, 19]) in possible_moves
# Checking 2U(pos=2, side=R, target=[18, 17]) in possible_moves
# Checking 2U(pos=2, side=R, target=[16, 15]) in possible_moves
# Checking 2U(pos=2, side=R, target=[6, 7]) in possible_moves
# Checking 2U(pos=2, side=R, target=[8, 7]) in possible_moves
# Checking 2U(pos=2, side=R, target=[8, 9]) in possible_moves
# Checking 2U(pos=2, side=R, target=[14, 13]) in possible_moves
# Checking 2U(pos=2, side=R, target=[12, 13]) in possible_moves
# Checking 2U(pos=2, side=R, target=[12, 11]) in possible_moves
# Checking 2U(pos=2, side=R, target=[10, 9]) in possible_moves
# Checking 2U(pos=2, side=R, target=[14, 15]) in possible_moves
# Checking 2U(pos=2, side=R, target=[6, 5]) in possible_moves
# Checking 2U(pos=2, side=R, target=[4, 3]) in possible_moves
# Checking 2U(pos=2, side=R, target=[20, 21]) in possible_moves
# Checking 2U(pos=2, side=R, target=[22, 21]) in possible_moves
# Checking 2U(pos=2, side=R, target=[22, 1]) in possible_moves
# Checking 2U(pos=2, side=R, target=[2, 1]) in possible_moves
# Checking 1U(pos=3, side=L, sign=1) in possible_moves
# Checking 1U(pos=3, side=L, sign=-1) in possible_moves
# Checking 1U(pos=3, side=R, sign=1) in possible_moves
# Checking 1U(pos=3, side=R, sign=-1) in possible_moves
# Checking 2U(pos=3, side=L, target=[5, 6]) in possible_moves
# Checking 2U(pos=3, side=L, target=[15, 14]) in possible_moves
# Checking 2U(pos=3, side=L, target=[9, 10]) in possible_moves
# Checking 2U(pos=3, side=L, target=[11, 12]) in possible_moves
# Checking 2U(pos=3, side=L, target=[13, 12]) in possible_moves
# Checking 2U(pos=3, side=L, target=[13, 14]) in possible_moves
# Checking 2U(pos=3, side=L, target=[9, 8]) in possible_moves
# Checking 2U(pos=3, side=L, target=[7, 8]) in possible_moves
# Checking 2U(pos=3, side=L, target=[7, 6]) in possible_moves
# Checking 2U(pos=3, side=L, target=[15, 16]) in possible_moves
# Checking 2U(pos=3, side=L, target=[17, 18]) in possible_moves
# Checking 2U(pos=3, side=L, target=[19, 18]) in possible_moves
# Checking 2U(pos=3, side=L, target=[19, 20]) in possible_moves
# Checking 2U(pos=3, side=L, target=[3, 2]) in possible_moves
# Checking 2U(pos=3, side=L, target=[1, 2]) in possible_moves
# Checking 2U(pos=3, side=L, target=[1, 22]) in possible_moves
# Checking 2U(pos=3, side=L, target=[21, 22]) in possible_moves
# Checking 2U(pos=3, side=L, target=[21, 20]) in possible_moves
# Checking 2U(pos=3, side=R, target=[5, 4]) in possible_moves
# Checking 2U(pos=3, side=R, target=[5, 6]) in possible_moves
# Checking 2U(pos=3, side=R, target=[15, 16]) in possible_moves
# Checking 2U(pos=3, side=R, target=[17, 16]) in possible_moves
# Checking 2U(pos=3, side=R, target=[17, 18]) in possible_moves
# Checking 2U(pos=3, side=R, target=[19, 20]) in possible_moves
# Checking 1U(pos=4, side=L, sign=1) in possible_moves
# Checking 1U(pos=4, side=L, sign=-1) in possible_moves
# Checking 1U(pos=4, side=R, sign=1) in possible_moves
# Checking 1U(pos=4, side=R, sign=-1) in possible_moves
# Checking 1D(pos=4) in possible_moves
# Checking 2U(pos=4, side=L, target=[4, 3]) in possible_moves
# Checking 2U(pos=4, side=L, target=[20, 19]) in possible_moves
# Checking 2U(pos=4, side=L, target=[18, 17]) in possible_moves
# Checking 2U(pos=4, side=L, target=[16, 17]) in possible_moves
# Checking 2U(pos=4, side=L, target=[16, 15]) in possible_moves
# Checking 2U(pos=4, side=L, target=[6, 5]) in possible_moves
# Checking 1U(pos=5, side=L, sign=1) in possible_moves
# Checking 1U(pos=5, side=L, sign=-1) in possible_moves
# Checking 1U(pos=5, side=R, sign=1) in possible_moves
# Checking 1U(pos=5, side=R, sign=-1) in possible_moves
# Checking 2U(pos=5, side=L, target=[15, 14]) in possible_moves
# Checking 2U(pos=5, side=L, target=[9, 10]) in possible_moves
# Checking 2U(pos=5, side=L, target=[11, 12]) in possible_moves
# Checking 2U(pos=5, side=L, target=[13, 12]) in possible_moves
# Checking 2U(pos=5, side=L, target=[13, 14]) in possible_moves
# Checking 2U(pos=5, side=L, target=[9, 8]) in possible_moves
# Checking 2U(pos=5, side=L, target=[7, 8]) in possible_moves
# Checking 2U(pos=5, side=L, target=[7, 6]) in possible_moves
# Checking 2U(pos=5, side=L, target=[15, 16]) in possible_moves
# Checking 2U(pos=5, side=L, target=[17, 18]) in possible_moves
# Checking 2U(pos=5, side=L, target=[19, 18]) in possible_moves
# Checking 2U(pos=5, side=L, target=[19, 20]) in possible_moves
# Checking 2U(pos=5, side=L, target=[3, 2]) in possible_moves
# Checking 2U(pos=5, side=L, target=[1, 2]) in possible_moves
# Checking 2U(pos=5, side=L, target=[1, 22]) in possible_moves
# Checking 2U(pos=5, side=L, target=[21, 22]) in possible_moves
# Checking 2U(pos=5, side=L, target=[21, 20]) in possible_moves
# Checking 2U(pos=5, side=L, target=[3, 4]) in possible_moves
# Checking 2U(pos=5, side=R, target=[15, 16]) in possible_moves
# Checking 2U(pos=5, side=R, target=[17, 16]) in possible_moves
# Checking 2U(pos=5, side=R, target=[17, 18]) in possible_moves
# Checking 2U(pos=5, side=R, target=[19, 20]) in possible_moves
# Checking 2U(pos=5, side=R, target=[3, 4]) in possible_moves
# Checking 2U(pos=5, side=R, target=[5, 4]) in possible_moves
# Checking 1U(pos=6, side=L, sign=1) in possible_moves
# Checking 1U(pos=6, side=L, sign=-1) in possible_moves
# Checking 1U(pos=6, side=R, sign=1) in possible_moves
# Checking 1U(pos=6, side=R, sign=-1) in possible_moves
# Checking 2U(pos=6, side=L, target=[8, 9]) in possible_moves
# Checking 2U(pos=6, side=L, target=[14, 15]) in possible_moves
# Checking 2U(pos=6, side=R, target=[8, 7]) in possible_moves
# Checking 2U(pos=6, side=R, target=[8, 9]) in possible_moves
# Checking 2U(pos=6, side=R, target=[14, 13]) in possible_moves
# Checking 2U(pos=6, side=R, target=[12, 13]) in possible_moves
# Checking 2U(pos=6, side=R, target=[12, 11]) in possible_moves
# Checking 2U(pos=6, side=R, target=[10, 9]) in possible_moves
# Checking 2U(pos=6, side=R, target=[14, 15]) in possible_moves
# Checking 2U(pos=6, side=R, target=[6, 5]) in possible_moves
# Checking 2U(pos=6, side=R, target=[4, 3]) in possible_moves
# Checking 2U(pos=6, side=R, target=[20, 21]) in possible_moves
# Checking 2U(pos=6, side=R, target=[22, 21]) in possible_moves
# Checking 2U(pos=6, side=R, target=[22, 1]) in possible_moves
# Checking 2U(pos=6, side=R, target=[2, 1]) in possible_moves
# Checking 2U(pos=6, side=R, target=[2, 3]) in possible_moves
# Checking 2U(pos=6, side=R, target=[20, 19]) in possible_moves
# Checking 2U(pos=6, side=R, target=[18, 19]) in possible_moves
# Checking 2U(pos=6, side=R, target=[18, 17]) in possible_moves
# Checking 2U(pos=6, side=R, target=[16, 15]) in possible_moves
# Checking 1U(pos=7, side=L, sign=1) in possible_moves
# Checking 1U(pos=7, side=L, sign=-1) in possible_moves
# Checking 1U(pos=7, side=R, sign=1) in possible_moves
# Checking 1U(pos=7, side=R, sign=-1) in possible_moves
# Checking 1D(pos=7) in possible_moves
# Checking 2U(pos=7, side=L, target=[7, 6]) in possible_moves
# Checking 2U(pos=7, side=L, target=[15, 16]) in possible_moves
# Checking 2U(pos=7, side=L, target=[17, 18]) in possible_moves
# Checking 2U(pos=7, side=L, target=[19, 18]) in possible_moves
# Checking 2U(pos=7, side=L, target=[19, 20]) in possible_moves
# Checking 2U(pos=7, side=L, target=[3, 2]) in possible_moves
# Checking 2U(pos=7, side=L, target=[1, 2]) in possible_moves
# Checking 2U(pos=7, side=L, target=[1, 22]) in possible_moves
# Checking 2U(pos=7, side=L, target=[21, 22]) in possible_moves
# Checking 2U(pos=7, side=L, target=[21, 20]) in possible_moves
# Checking 2U(pos=7, side=L, target=[3, 4]) in possible_moves
# Checking 2U(pos=7, side=L, target=[5, 6]) in possible_moves
# Checking 2U(pos=7, side=L, target=[15, 14]) in possible_moves
# Checking 2U(pos=7, side=L, target=[9, 10]) in possible_moves
# Checking 2U(pos=7, side=L, target=[11, 12]) in possible_moves
# Checking 2U(pos=7, side=L, target=[13, 12]) in possible_moves
# Checking 2U(pos=7, side=L, target=[13, 14]) in possible_moves
# Checking 2U(pos=7, side=L, target=[9, 8]) in possible_moves
# Checking 1U(pos=8, side=L, sign=1) in possible_moves
# Checking 1U(pos=8, side=L, sign=-1) in possible_moves
# Checking 1U(pos=8, side=R, sign=1) in possible_moves
# Checking 1U(pos=8, side=R, sign=-1) in possible_moves
# Checking 2U(pos=8, side=L, target=[14, 15]) in possible_moves
# Checking 2U(pos=8, side=L, target=[6, 7]) in possible_moves
# Checking 2U(pos=8, side=R, target=[14, 13]) in possible_moves
# Checking 2U(pos=8, side=R, target=[12, 13]) in possible_moves
# Checking 2U(pos=8, side=R, target=[12, 11]) in possible_moves
# Checking 2U(pos=8, side=R, target=[10, 9]) in possible_moves
# Checking 2U(pos=8, side=R, target=[14, 15]) in possible_moves
# Checking 2U(pos=8, side=R, target=[6, 5]) in possible_moves
# Checking 2U(pos=8, side=R, target=[4, 3]) in possible_moves
# Checking 2U(pos=8, side=R, target=[20, 21]) in possible_moves
# Checking 2U(pos=8, side=R, target=[22, 21]) in possible_moves
# Checking 2U(pos=8, side=R, target=[22, 1]) in possible_moves
# Checking 2U(pos=8, side=R, target=[2, 1]) in possible_moves
# Checking 2U(pos=8, side=R, target=[2, 3]) in possible_moves
# Checking 2U(pos=8, side=R, target=[20, 19]) in possible_moves
# Checking 2U(pos=8, side=R, target=[18, 19]) in possible_moves
# Checking 2U(pos=8, side=R, target=[18, 17]) in possible_moves
# Checking 2U(pos=8, side=R, target=[16, 15]) in possible_moves
# Checking 2U(pos=8, side=R, target=[6, 7]) in possible_moves
# Checking 2U(pos=8, side=R, target=[8, 7]) in possible_moves
# Checking 3H(pos=8, side=L) in possible_moves
# Trying to apply move:  3H(pos=8, side=L)
# to diagram:  ('2, 20, 4, -8, 14, -10, 12, -6, -16, 18, -22', '1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1')
# cannot do R3 from that position: not a triangle
# Checking 1U(pos=9, side=L, sign=1) in possible_moves
# Checking 1U(pos=9, side=L, sign=-1) in possible_moves
# Checking 1U(pos=9, side=R, sign=1) in possible_moves
# Checking 1U(pos=9, side=R, sign=-1) in possible_moves
# Checking 2U(pos=9, side=L, target=[11, 12]) in possible_moves
# Checking 2U(pos=9, side=L, target=[13, 12]) in possible_moves
# Checking 2U(pos=9, side=L, target=[13, 14]) in possible_moves
# Checking 2U(pos=9, side=L, target=[9, 8]) in possible_moves
# Checking 2U(pos=9, side=L, target=[7, 8]) in possible_moves
# Checking 2U(pos=9, side=L, target=[7, 6]) in possible_moves
# Checking 2U(pos=9, side=L, target=[15, 16]) in possible_moves
# Checking 2U(pos=9, side=L, target=[17, 18]) in possible_moves
# Checking 2U(pos=9, side=L, target=[19, 18]) in possible_moves
# Checking 2U(pos=9, side=L, target=[19, 20]) in possible_moves
# Checking 2U(pos=9, side=L, target=[3, 2]) in possible_moves
# Checking 2U(pos=9, side=L, target=[1, 2]) in possible_moves
# Checking 2U(pos=9, side=L, target=[1, 22]) in possible_moves
# Checking 2U(pos=9, side=L, target=[21, 22]) in possible_moves
# Checking 2U(pos=9, side=L, target=[21, 20]) in possible_moves
# Checking 2U(pos=9, side=L, target=[3, 4]) in possible_moves
# Checking 2U(pos=9, side=L, target=[5, 6]) in possible_moves
# Checking 2U(pos=9, side=L, target=[15, 14]) in possible_moves
# Checking 2U(pos=9, side=R, target=[11, 10]) in possible_moves
# Checking 2U(pos=9, side=R, target=[11, 12]) in possible_moves
# Checking 2U(pos=9, side=R, target=[13, 14]) in possible_moves
# Checking 1U(pos=10, side=L, sign=1) in possible_moves
# Checking 1U(pos=10, side=L, sign=-1) in possible_moves
# Checking 1U(pos=10, side=R, sign=1) in possible_moves
# Checking 1U(pos=10, side=R, sign=-1) in possible_moves
# Checking 1D(pos=10) in possible_moves
# Checking 2U(pos=10, side=L, target=[10, 9]) in possible_moves
# Checking 2U(pos=10, side=L, target=[14, 13]) in possible_moves
# Checking 2U(pos=10, side=L, target=[12, 11]) in possible_moves
# Checking 1U(pos=11, side=L, sign=1) in possible_moves
# Checking 1U(pos=11, side=L, sign=-1) in possible_moves
# Checking 1U(pos=11, side=R, sign=1) in possible_moves
# Checking 1U(pos=11, side=R, sign=-1) in possible_moves
# Checking 2U(pos=11, side=L, target=[13, 12]) in possible_moves
# Checking 2U(pos=11, side=L, target=[13, 14]) in possible_moves
# Checking 2U(pos=11, side=L, target=[9, 8]) in possible_moves
# Checking 2U(pos=11, side=L, target=[7, 8]) in possible_moves
# Checking 2U(pos=11, side=L, target=[7, 6]) in possible_moves
# Checking 2U(pos=11, side=L, target=[15, 16]) in possible_moves
# Checking 2U(pos=11, side=L, target=[17, 18]) in possible_moves
# Checking 2U(pos=11, side=L, target=[19, 18]) in possible_moves
# Checking 2U(pos=11, side=L, target=[19, 20]) in possible_moves
# Checking 2U(pos=11, side=L, target=[3, 2]) in possible_moves
# Checking 2U(pos=11, side=L, target=[1, 2]) in possible_moves
# Checking 2U(pos=11, side=L, target=[1, 22]) in possible_moves
# Checking 2U(pos=11, side=L, target=[21, 22]) in possible_moves
# Checking 2U(pos=11, side=L, target=[21, 20]) in possible_moves
# Checking 2U(pos=11, side=L, target=[3, 4]) in possible_moves
# Checking 2U(pos=11, side=L, target=[5, 6]) in possible_moves
# Checking 2U(pos=11, side=L, target=[15, 14]) in possible_moves
# Checking 2U(pos=11, side=L, target=[9, 10]) in possible_moves
# Checking 2U(pos=11, side=R, target=[13, 14]) in possible_moves
# Checking 2U(pos=11, side=R, target=[9, 10]) in possible_moves
# Checking 2U(pos=11, side=R, target=[11, 10]) in possible_moves
# Checking 1U(pos=12, side=L, sign=1) in possible_moves
# Checking 1U(pos=12, side=L, sign=-1) in possible_moves
# Checking 1U(pos=12, side=R, sign=1) in possible_moves
# Checking 1U(pos=12, side=R, sign=-1) in possible_moves
# Checking 1D(pos=12) in possible_moves
# Checking 2U(pos=12, side=R, target=[12, 11]) in possible_moves
# Checking 2U(pos=12, side=R, target=[10, 9]) in possible_moves
# Checking 2U(pos=12, side=R, target=[14, 15]) in possible_moves
# Checking 2U(pos=12, side=R, target=[6, 5]) in possible_moves
# Checking 2U(pos=12, side=R, target=[4, 3]) in possible_moves
# Checking 2U(pos=12, side=R, target=[20, 21]) in possible_moves
# Checking 2U(pos=12, side=R, target=[22, 21]) in possible_moves
# Checking 2U(pos=12, side=R, target=[22, 1]) in possible_moves
# Checking 2U(pos=12, side=R, target=[2, 1]) in possible_moves
# Checking 2U(pos=12, side=R, target=[2, 3]) in possible_moves
# Checking 2U(pos=12, side=R, target=[20, 19]) in possible_moves
# Checking 2U(pos=12, side=R, target=[18, 19]) in possible_moves
# Checking 2U(pos=12, side=R, target=[18, 17]) in possible_moves
# Checking 2U(pos=12, side=R, target=[16, 15]) in possible_moves
# Checking 2U(pos=12, side=R, target=[6, 7]) in possible_moves
# Checking 2U(pos=12, side=R, target=[8, 7]) in possible_moves
# Checking 2U(pos=12, side=R, target=[8, 9]) in possible_moves
# Checking 2U(pos=12, side=R, target=[14, 13]) in possible_moves
# Checking 1U(pos=13, side=L, sign=1) in possible_moves
# Checking 1U(pos=13, side=L, sign=-1) in possible_moves
# Checking 1U(pos=13, side=R, sign=1) in possible_moves
# Checking 1U(pos=13, side=R, sign=-1) in possible_moves
# Checking 2U(pos=13, side=L, target=[9, 8]) in possible_moves
# Checking 2U(pos=13, side=L, target=[7, 8]) in possible_moves
# Checking 2U(pos=13, side=L, target=[7, 6]) in possible_moves
# Checking 2U(pos=13, side=L, target=[15, 16]) in possible_moves
# Checking 2U(pos=13, side=L, target=[17, 18]) in possible_moves
# Checking 2U(pos=13, side=L, target=[19, 18]) in possible_moves
# Checking 2U(pos=13, side=L, target=[19, 20]) in possible_moves
# Checking 2U(pos=13, side=L, target=[3, 2]) in possible_moves
# Checking 2U(pos=13, side=L, target=[1, 2]) in possible_moves
# Checking 2U(pos=13, side=L, target=[1, 22]) in possible_moves
# Checking 2U(pos=13, side=L, target=[21, 22]) in possible_moves
# Checking 2U(pos=13, side=L, target=[21, 20]) in possible_moves
# Checking 2U(pos=13, side=L, target=[3, 4]) in possible_moves
# Checking 2U(pos=13, side=L, target=[5, 6]) in possible_moves
# Checking 2U(pos=13, side=L, target=[15, 14]) in possible_moves
# Checking 2U(pos=13, side=L, target=[9, 10]) in possible_moves
# Checking 2U(pos=13, side=L, target=[11, 12]) in possible_moves
# Checking 2U(pos=13, side=L, target=[13, 12]) in possible_moves
# Checking 2U(pos=13, side=R, target=[9, 10]) in possible_moves
# Checking 2U(pos=13, side=R, target=[11, 10]) in possible_moves
# Checking 2U(pos=13, side=R, target=[11, 12]) in possible_moves
# Checking 1U(pos=14, side=L, sign=1) in possible_moves
# Checking 1U(pos=14, side=L, sign=-1) in possible_moves
# Checking 1U(pos=14, side=R, sign=1) in possible_moves
# Checking 1U(pos=14, side=R, sign=-1) in possible_moves
# Checking 2U(pos=14, side=L, target=[6, 7]) in possible_moves
# Checking 2U(pos=14, side=L, target=[8, 9]) in possible_moves
# Checking 2U(pos=14, side=R, target=[6, 5]) in possible_moves
# Checking 2U(pos=14, side=R, target=[4, 3]) in possible_moves
# Checking 2U(pos=14, side=R, target=[20, 21]) in possible_moves
# Checking 2U(pos=14, side=R, target=[22, 21]) in possible_moves
# Checking 2U(pos=14, side=R, target=[22, 1]) in possible_moves
# Checking 2U(pos=14, side=R, target=[2, 1]) in possible_moves
# Checking 2U(pos=14, side=R, target=[2, 3]) in possible_moves
# Checking 2U(pos=14, side=R, target=[20, 19]) in possible_moves
# Checking 2U(pos=14, side=R, target=[18, 19]) in possible_moves
# Checking 2U(pos=14, side=R, target=[18, 17]) in possible_moves
# Checking 2U(pos=14, side=R, target=[16, 15]) in possible_moves
# Checking 2U(pos=14, side=R, target=[6, 7]) in possible_moves
# Checking 2U(pos=14, side=R, target=[8, 7]) in possible_moves
# Checking 2U(pos=14, side=R, target=[8, 9]) in possible_moves
# Checking 2U(pos=14, side=R, target=[14, 13]) in possible_moves
# Checking 2U(pos=14, side=R, target=[12, 13]) in possible_moves
# Checking 2U(pos=14, side=R, target=[12, 11]) in possible_moves
# Checking 2U(pos=14, side=R, target=[10, 9]) in possible_moves
# Checking 3H(pos=14, side=L) in possible_moves
# Trying to apply move:  3H(pos=14, side=L)
# to diagram:  ('2, 20, 4, -8, 14, -10, 12, -6, -16, 18, -22', '1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1')
# cannot do R3 from that position: not a triangle
# Checking 1U(pos=15, side=L, sign=1) in possible_moves
# Checking 1U(pos=15, side=L, sign=-1) in possible_moves
# Checking 1U(pos=15, side=R, sign=1) in possible_moves
# Checking 1U(pos=15, side=R, sign=-1) in possible_moves
# Checking 2U(pos=15, side=L, target=[17, 18]) in possible_moves
# Checking 2U(pos=15, side=L, target=[19, 18]) in possible_moves
# Checking 2U(pos=15, side=L, target=[19, 20]) in possible_moves
# Checking 2U(pos=15, side=L, target=[3, 2]) in possible_moves
# Checking 2U(pos=15, side=L, target=[1, 2]) in possible_moves
# Checking 2U(pos=15, side=L, target=[1, 22]) in possible_moves
# Checking 2U(pos=15, side=L, target=[21, 22]) in possible_moves
# Checking 2U(pos=15, side=L, target=[21, 20]) in possible_moves
# Checking 2U(pos=15, side=L, target=[3, 4]) in possible_moves
# Checking 2U(pos=15, side=L, target=[5, 6]) in possible_moves
# Checking 2U(pos=15, side=L, target=[15, 14]) in possible_moves
# Checking 2U(pos=15, side=L, target=[9, 10]) in possible_moves
# Checking 2U(pos=15, side=L, target=[11, 12]) in possible_moves
# Checking 2U(pos=15, side=L, target=[13, 12]) in possible_moves
# Checking 2U(pos=15, side=L, target=[13, 14]) in possible_moves
# Checking 2U(pos=15, side=L, target=[9, 8]) in possible_moves
# Checking 2U(pos=15, side=L, target=[7, 8]) in possible_moves
# Checking 2U(pos=15, side=L, target=[7, 6]) in possible_moves
# Checking 2U(pos=15, side=R, target=[17, 16]) in possible_moves
# Checking 2U(pos=15, side=R, target=[17, 18]) in possible_moves
# Checking 2U(pos=15, side=R, target=[19, 20]) in possible_moves
# Checking 2U(pos=15, side=R, target=[3, 4]) in possible_moves
# Checking 2U(pos=15, side=R, target=[5, 4]) in possible_moves
# Checking 2U(pos=15, side=R, target=[5, 6]) in possible_moves
# Checking 1U(pos=16, side=L, sign=1) in possible_moves
# Checking 1U(pos=16, side=L, sign=-1) in possible_moves
# Checking 1U(pos=16, side=R, sign=1) in possible_moves
# Checking 1U(pos=16, side=R, sign=-1) in possible_moves
# Checking 1D(pos=16) in possible_moves
# Checking 2U(pos=16, side=L, target=[16, 15]) in possible_moves
# Checking 2U(pos=16, side=L, target=[6, 5]) in possible_moves
# Checking 2U(pos=16, side=L, target=[4, 5]) in possible_moves
# Checking 2U(pos=16, side=L, target=[4, 3]) in possible_moves
# Checking 2U(pos=16, side=L, target=[20, 19]) in possible_moves
# Checking 2U(pos=16, side=L, target=[18, 17]) in possible_moves
# Checking 1U(pos=17, side=L, sign=1) in possible_moves
# Checking 1U(pos=17, side=L, sign=-1) in possible_moves
# Checking 1U(pos=17, side=R, sign=1) in possible_moves
# Checking 1U(pos=17, side=R, sign=-1) in possible_moves
# Checking 2U(pos=17, side=L, target=[19, 18]) in possible_moves
# Checking 2U(pos=17, side=L, target=[19, 20]) in possible_moves
# Checking 2U(pos=17, side=L, target=[3, 2]) in possible_moves
# Checking 2U(pos=17, side=L, target=[1, 2]) in possible_moves
# Checking 2U(pos=17, side=L, target=[1, 22]) in possible_moves
# Checking 2U(pos=17, side=L, target=[21, 22]) in possible_moves
# Checking 2U(pos=17, side=L, target=[21, 20]) in possible_moves
# Checking 2U(pos=17, side=L, target=[3, 4]) in possible_moves
# Checking 2U(pos=17, side=L, target=[5, 6]) in possible_moves
# Checking 2U(pos=17, side=L, target=[15, 14]) in possible_moves
# Checking 2U(pos=17, side=L, target=[9, 10]) in possible_moves
# Checking 2U(pos=17, side=L, target=[11, 12]) in possible_moves
# Checking 2U(pos=17, side=L, target=[13, 12]) in possible_moves
# Checking 2U(pos=17, side=L, target=[13, 14]) in possible_moves
# Checking 2U(pos=17, side=L, target=[9, 8]) in possible_moves
# Checking 2U(pos=17, side=L, target=[7, 8]) in possible_moves
# Checking 2U(pos=17, side=L, target=[7, 6]) in possible_moves
# Checking 2U(pos=17, side=L, target=[15, 16]) in possible_moves
# Checking 2U(pos=17, side=R, target=[19, 20]) in possible_moves
# Checking 2U(pos=17, side=R, target=[3, 4]) in possible_moves
# Checking 2U(pos=17, side=R, target=[5, 4]) in possible_moves
# Checking 2U(pos=17, side=R, target=[5, 6]) in possible_moves
# Checking 2U(pos=17, side=R, target=[15, 16]) in possible_moves
# Checking 2U(pos=17, side=R, target=[17, 16]) in possible_moves
# Checking 1U(pos=18, side=L, sign=1) in possible_moves
# Checking 1U(pos=18, side=L, sign=-1) in possible_moves
# Checking 1U(pos=18, side=R, sign=1) in possible_moves
# Checking 1U(pos=18, side=R, sign=-1) in possible_moves
# Checking 1D(pos=18) in possible_moves
# Checking 2U(pos=18, side=R, target=[18, 17]) in possible_moves
# Checking 2U(pos=18, side=R, target=[16, 15]) in possible_moves
# Checking 2U(pos=18, side=R, target=[6, 7]) in possible_moves
# Checking 2U(pos=18, side=R, target=[8, 7]) in possible_moves
# Checking 2U(pos=18, side=R, target=[8, 9]) in possible_moves
# Checking 2U(pos=18, side=R, target=[14, 13]) in possible_moves
# Checking 2U(pos=18, side=R, target=[12, 13]) in possible_moves
# Checking 2U(pos=18, side=R, target=[12, 11]) in possible_moves
# Checking 2U(pos=18, side=R, target=[10, 9]) in possible_moves
# Checking 2U(pos=18, side=R, target=[14, 15]) in possible_moves
# Checking 2U(pos=18, side=R, target=[6, 5]) in possible_moves
# Checking 2U(pos=18, side=R, target=[4, 3]) in possible_moves
# Checking 2U(pos=18, side=R, target=[20, 21]) in possible_moves
# Checking 2U(pos=18, side=R, target=[22, 21]) in possible_moves
# Checking 2U(pos=18, side=R, target=[22, 1]) in possible_moves
# Checking 2U(pos=18, side=R, target=[2, 1]) in possible_moves
# Checking 2U(pos=18, side=R, target=[2, 3]) in possible_moves
# Checking 2U(pos=18, side=R, target=[20, 19]) in possible_moves
# Checking 1U(pos=19, side=L, sign=1) in possible_moves
# Checking 1U(pos=19, side=L, sign=-1) in possible_moves
# Checking 1U(pos=19, side=R, sign=1) in possible_moves
# Checking 1U(pos=19, side=R, sign=-1) in possible_moves
# Checking 2U(pos=19, side=L, target=[3, 2]) in possible_moves
# Checking 2U(pos=19, side=L, target=[1, 2]) in possible_moves
# Checking 2U(pos=19, side=L, target=[1, 22]) in possible_moves
# Checking 2U(pos=19, side=L, target=[21, 22]) in possible_moves
# Checking 2U(pos=19, side=L, target=[21, 20]) in possible_moves
# Checking 2U(pos=19, side=L, target=[3, 4]) in possible_moves
# Checking 2U(pos=19, side=L, target=[5, 6]) in possible_moves
# Checking 2U(pos=19, side=L, target=[15, 14]) in possible_moves
# Checking 2U(pos=19, side=L, target=[9, 10]) in possible_moves
# Checking 2U(pos=19, side=L, target=[11, 12]) in possible_moves
# Checking 2U(pos=19, side=L, target=[13, 12]) in possible_moves
# Checking 2U(pos=19, side=L, target=[13, 14]) in possible_moves
# Checking 2U(pos=19, side=L, target=[9, 8]) in possible_moves
# Checking 2U(pos=19, side=L, target=[7, 8]) in possible_moves
# Checking 2U(pos=19, side=L, target=[7, 6]) in possible_moves
# Checking 2U(pos=19, side=L, target=[15, 16]) in possible_moves
# Checking 2U(pos=19, side=L, target=[17, 18]) in possible_moves
# Checking 2U(pos=19, side=L, target=[19, 18]) in possible_moves
# Checking 2U(pos=19, side=R, target=[3, 4]) in possible_moves
# Checking 2U(pos=19, side=R, target=[5, 4]) in possible_moves
# Checking 2U(pos=19, side=R, target=[5, 6]) in possible_moves
# Checking 2U(pos=19, side=R, target=[15, 16]) in possible_moves
# Checking 2U(pos=19, side=R, target=[17, 16]) in possible_moves
# Checking 2U(pos=19, side=R, target=[17, 18]) in possible_moves
# Checking 1U(pos=20, side=L, sign=1) in possible_moves
# Checking 1U(pos=20, side=L, sign=-1) in possible_moves
# Checking 1U(pos=20, side=R, sign=1) in possible_moves
# Checking 1U(pos=20, side=R, sign=-1) in possible_moves
# Checking 2U(pos=20, side=L, target=[22, 1]) in possible_moves
# Checking 2U(pos=20, side=L, target=[2, 3]) in possible_moves
# Checking 2U(pos=20, side=R, target=[22, 21]) in possible_moves
# Checking 2U(pos=20, side=R, target=[22, 1]) in possible_moves
# Checking 2U(pos=20, side=R, target=[2, 1]) in possible_moves
# Checking 2U(pos=20, side=R, target=[2, 3]) in possible_moves
# Checking 2U(pos=20, side=R, target=[20, 19]) in possible_moves
# Checking 2U(pos=20, side=R, target=[18, 19]) in possible_moves
# Checking 2U(pos=20, side=R, target=[18, 17]) in possible_moves
# Checking 2U(pos=20, side=R, target=[16, 15]) in possible_moves
# Checking 2U(pos=20, side=R, target=[6, 7]) in possible_moves
# Checking 2U(pos=20, side=R, target=[8, 7]) in possible_moves
# Checking 2U(pos=20, side=R, target=[8, 9]) in possible_moves
# Checking 2U(pos=20, side=R, target=[14, 13]) in possible_moves
# Checking 2U(pos=20, side=R, target=[12, 13]) in possible_moves
# Checking 2U(pos=20, side=R, target=[12, 11]) in possible_moves
# Checking 2U(pos=20, side=R, target=[10, 9]) in possible_moves
# Checking 2U(pos=20, side=R, target=[14, 15]) in possible_moves
# Checking 2U(pos=20, side=R, target=[6, 5]) in possible_moves
# Checking 2U(pos=20, side=R, target=[4, 3]) in possible_moves
# Checking 3H(pos=20, side=L) in possible_moves
# Trying to apply move:  3H(pos=20, side=L)
# to diagram:  ('2, 20, 4, -8, 14, -10, 12, -6, -16, 18, -22', '1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1')
# cannot do R3 from that position: not a triangle
# Checking 1U(pos=21, side=L, sign=1) in possible_moves
# Checking 1U(pos=21, side=L, sign=-1) in possible_moves
# Checking 1U(pos=21, side=R, sign=1) in possible_moves
# Checking 1U(pos=21, side=R, sign=-1) in possible_moves
# Checking 1D(pos=21) in possible_moves
# Checking 2U(pos=21, side=L, target=[21, 20]) in possible_moves
# Checking 2U(pos=21, side=L, target=[3, 4]) in possible_moves
# Checking 2U(pos=21, side=L, target=[5, 6]) in possible_moves
# Checking 2U(pos=21, side=L, target=[15, 14]) in possible_moves
# Checking 2U(pos=21, side=L, target=[9, 10]) in possible_moves
# Checking 2U(pos=21, side=L, target=[11, 12]) in possible_moves
# Checking 2U(pos=21, side=L, target=[13, 12]) in possible_moves
# Checking 2U(pos=21, side=L, target=[13, 14]) in possible_moves
# Checking 2U(pos=21, side=L, target=[9, 8]) in possible_moves
# Checking 2U(pos=21, side=L, target=[7, 8]) in possible_moves
# Checking 2U(pos=21, side=L, target=[7, 6]) in possible_moves
# Checking 2U(pos=21, side=L, target=[15, 16]) in possible_moves
# Checking 2U(pos=21, side=L, target=[17, 18]) in possible_moves
# Checking 2U(pos=21, side=L, target=[19, 18]) in possible_moves
# Checking 2U(pos=21, side=L, target=[19, 20]) in possible_moves
# Checking 2U(pos=21, side=L, target=[3, 2]) in possible_moves
# Checking 2U(pos=21, side=L, target=[1, 2]) in possible_moves
# Checking 2U(pos=21, side=L, target=[1, 22]) in possible_moves
# Checking 1U(pos=22, side=L, sign=1) in possible_moves
# Checking 1U(pos=22, side=L, sign=-1) in possible_moves
# Checking 1U(pos=22, side=R, sign=1) in possible_moves
# Checking 1U(pos=22, side=R, sign=-1) in possible_moves
# Checking 2U(pos=22, side=L, target=[2, 3]) in possible_moves
# Checking 2U(pos=22, side=L, target=[20, 21]) in possible_moves
# Checking 2U(pos=22, side=R, target=[2, 1]) in possible_moves
# Checking 2U(pos=22, side=R, target=[2, 3]) in possible_moves
# Checking 2U(pos=22, side=R, target=[20, 19]) in possible_moves
# Checking 2U(pos=22, side=R, target=[18, 19]) in possible_moves
# Checking 2U(pos=22, side=R, target=[18, 17]) in possible_moves
# Checking 2U(pos=22, side=R, target=[16, 15]) in possible_moves
# Checking 2U(pos=22, side=R, target=[6, 7]) in possible_moves
# Checking 2U(pos=22, side=R, target=[8, 7]) in possible_moves
# Checking 2U(pos=22, side=R, target=[8, 9]) in possible_moves
# Checking 2U(pos=22, side=R, target=[14, 13]) in possible_moves
# Checking 2U(pos=22, side=R, target=[12, 13]) in possible_moves
# Checking 2U(pos=22, side=R, target=[12, 11]) in possible_moves
# Checking 2U(pos=22, side=R, target=[10, 9]) in possible_moves
# Checking 2U(pos=22, side=R, target=[14, 15]) in possible_moves
# Checking 2U(pos=22, side=R, target=[6, 5]) in possible_moves
# Checking 2U(pos=22, side=R, target=[4, 3]) in possible_moves
# Checking 2U(pos=22, side=R, target=[20, 21]) in possible_moves
# Checking 2U(pos=22, side=R, target=[22, 21]) in possible_moves
# Checking 3H(pos=22, side=L) in possible_moves
# Trying to apply move:  3H(pos=22, side=L)
# to diagram:  ('2, 20, 4, -8, 14, -10, 12, -6, -16, 18, -22', '1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1')
# cannot do R3 from that position: not a triangle
# Done cycling through possible_moves
# Nothing is being returned.
# Traceback (most recent call last):
#   File "TestSystem.py", line 28, in <module>
#     raise TypeError("findInverse should never have been called.")
# TypeError: findInverse should never have been called.
