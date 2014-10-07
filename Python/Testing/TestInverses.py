import ADTLink, ADTOp

def findInverse(diagram, op):
    K = diagram.copy()
    if op.apply(K):
        possible_moves = K.finePossibleMoves()
        for move in possible_moves:
#            print "Trying {}".format(move.getFullType())
            Ktemp = K.copy()
            move.apply(Ktemp)
            if diagram == Ktemp:
                print "These two moves are inverses."
                return op, move
        print "This move has no inverse."
        return op
    else:
    	print "This move does nothing to this diagram."
    	
L = ADTLink.ADTLink([-12, 14, -16, -22, -20, -6, 2, -4, -18, -10, 8], [-1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1])
for i in range(100):
    M = ADTOp.fineRandomOp(L)
    findInverse(L, M)