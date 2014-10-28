import os, sys, TestInverses, ADT, ADTOp, ADTOpList
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

# K = ADT.ADT([], [])
# 
# m = K.finePossibleMoves()
# for i in m:
# 	print "Here is a move: ", i.toString()
# 	inv = TestInverses.findInverse(K, i)
# 	print "Here is its inverse: ", inv.toString()
# 	L = K.copy()
# 	i.apply(L)
# 	print "After applying the original move, the result is: ", L.to_string()
# 	inv.apply(L)
# 	print "And after applying the inverse: ", L.to_string()


# k = 1000000000
# n = 15
# 
# K = ADT.ADT([],[])
# 
# Errors = []
# 
# path = [K]
# moves = ADTOpList.randomOpList(n, n).toList()
# for i in moves:
# 	L = K.copy()
# 	M = K.copy()
# 	if i.apply(L):
# 		result = TestInverses.findInverse(M, i)
# 		if not result[0]:
# 			Errors.append([result[1], result[2]])
# 			if result[1] > 4:
# 				print "#"*30
# 				print "This is a big one."
# 				print "original: ", K.to_string()
# 				print "move: ", i.toString()
# 				break
# 		K = L
# 		
# print Errors
# 


original = ADT.ADT([6, 2, -10, 4, 8], [1, -1, -1, 1, -1])
print "Original diagram: ", original.to_string()
move = ADTOp.ADTOp(2, "D", {'arc':10})
print "Move to invert: ", move.toString()
print '\n'

K = original.copy()

print "Applying the move to the diagram results in:"
move.apply(K)
K.to_string()
# K = [6, 2, 4], [-1, -1, 1]
print '\n'

inverse = ADTOp.ADTOp(2, "U", {'arc':1, 'side':"L", 'target':[5,4]})
print "The inverse move should is: ", inverse.toString()
print '\n'

print "We apply the inverse move to this new diagram, and get:"
inverse.apply(K)
K.to_string()
# K = [10, 8, 4, -2, 6], [-1, 1, -1, -1, 1]
print '\n'

print "Do these represent the same diagram?"
original.sameDiagram(K)
print original.sameDiagram(K)
# True
print '\n'

print "However, there seems to be a problem with the findInverse code:"
TestInverses.findInverse(original, move)
# WHY DOESN'T THIS WORK?
print '\n'
print '\n'
print '\n'