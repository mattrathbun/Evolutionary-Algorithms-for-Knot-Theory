import ADTLink, ADTOp

L = ADTLink.ADTLink([-12, 14, -16, -22, -20, -6, 2, -4, -18, -10, 8], [-1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1])

print L.finePossibleMoves()
#print L.possibleR2Down()
# Should be [1, 3, 7, 8, 12, 14, 20, 21]	
