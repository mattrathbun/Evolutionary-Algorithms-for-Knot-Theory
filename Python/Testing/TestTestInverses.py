import os, sys, TestInverses, ADT, ADTOp
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

K = ADT.ADT([], [])

m = K.finePossibleMoves()
for i in m:
	print "Here is a move: ", i.toString()
	inv = TestInverses.findInverse(K, i)
	print "Here is its inverse: ", inv.toString()
	L = K.copy()
	i.apply(L)
	print "After applying the original move, the result is: ", L.to_string()
	inv.apply(L)
	print "And after applying the inverse: ", L.to_string()