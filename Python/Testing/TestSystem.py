import os, sys, TestInverses
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ADT, ADTOp, ADTOpList, ADTOpPopulation

n = 100

K = ADT.ADT([],[])

path = [K]
sequence = []
inverses = []
moves = ADTOpList.randomOpList(n, n).toList()
for i in moves:
	L = K.copy()
	M = K.copy()
	if i.apply(L):
		sequence.append(i)
		path.append(L)
		inv = TestInverses.findInverse(M, i)
		inverses.append(inv)
		K = L

print '\n'*10
print '*'*30
print "Here is the result:"
print '\n'

print 'Path:'
for i in path:
	print i.to_string()
	print '\n'
print '\n'

print 'Sequence:'
for i in sequence:
	print i.toString()
	print '\n'
print '\n'

print 'Inverses:'
for i in inverses:
	if i.getattr(self, "toString", False):
		print i.toString()
		print '\n'
	else:
		print ' '
		print '\n'
print '\n'

