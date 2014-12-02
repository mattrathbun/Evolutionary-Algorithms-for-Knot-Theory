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
                    #        			print "FOUND IT!"
                    #        			return [True, move]
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
#         print "*"*30
#         print "Error!!"
#         print "n = ", n
#         print "The move we are trying to invert is: ", op.toString()
#         return [False, diagram.to_list(), n, op.toString()]
#         raise TypeError("No inverse found.")
    else:
        print "About to return None in TestInverses function findInverse"
        return None
#    else:
#    	return None
#                print "These two moves are inverses."
#                return op, move
#        print "This move has no inverse."
#        return op
#    else:
#    	print "This move does nothing to this diagram."
#    	return op
#		return None

##L = ADT.ADT([-12, 14, -16, -22, -20, -6, 2, -4, -18, -10, 8], [-1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1])
# for i in range(100):
##    M = ADTOp.fineRandomOp(L)
##    findInverse(L, M)
