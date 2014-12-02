import os, sys, TestInverses
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ADT, ADTOp, ADTOpList, ADTOpPopulation

n = 40


K = ADT.ADT([],[])

path = [K]
sequence = []
inverses = []
moves = ADTOpList.randomOpList(n, n, upBias=5, downBias=5).toList()
print "We have a list of moves."
for i in moves:
	print i.toString()
for i in moves:
	L = K.copy()
	M = K.copy()
	if i.apply(L):
		sequence.append(i)
		path.append(L)
		print "Just about to call findInverse on diagram {}, with move {}".format(M.to_list(), i.toString())
		inv = TestInverses.findInverse(M, i)
		if inv == None:
			raise TypeError("findInverse should never have been called.")
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

print 'Inverses: '
for i in inverses:
	print i
	print i.toString()
	print '\n'
	
print len(path), len(sequence), len(inverses)

# print 'Inverses:'
# for i in inverses:
# 	if i.getattr(self, "toString", False):
# 		print i.toString()
# 		print '\n'
# 	else:
# 		print ' '
# 		print '\n'
# print '\n'

