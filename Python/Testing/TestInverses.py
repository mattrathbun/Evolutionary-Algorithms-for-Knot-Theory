import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ADT, ADTOp

def findInverse(diagram, op):
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
        possible_moves = K.finePossibleMoves()
        for move in possible_moves:
        	if move.getNumber == number and move.getDirection == reverse:
        		Ktemp = K.copy()
        		move.apply(Ktemp)
        		if diagram.sameDiagram(Ktemp):
        			print "FOUND IT!"
        			retrun [True, move]
#        			return move
        print "Original diagram: ", diagram.to_string()
        print "Origingal move: ", op.toString()
        print "After move has been applied: ", K.to_string()
        print "Possible moves on the result: "
        for i in possible_moves:
        	print i.toString()
        print "*"*30
        print "n = ", n
        print "The move we are trying to invert is: ", op.toString()
#        return [False, n, op.toString()]
        raise TypeError("No inverse found.")
    else:
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
##for i in range(100):
##    M = ADTOp.fineRandomOp(L)
##    findInverse(L, M)