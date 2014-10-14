import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ADT

K = ADT.ADT([6, 12, 8, 2, 10, -4], [-1, -1, -1, -1, 1, 1])
L = ADT.ADT([-6, 10, -12, -4, -8, -2], [-1, 1, -1, -1, 1, -1])
print K.sameDiagram(L)
# Should be True
if not K.sameDiagram(L):
	raise TypeError("These are different diagrams!")
	
M = ADT.ADT([10, 6, 12, 8, -2, 4], [-1, -1, -1, 1, 1, -1])
print K.sameDiagram(M)
# Should be True
if not K.sameDiagram(M):
	raise TypeError("These are different diagrams!")
	
n = K.number_crossings()
around = K.copy()
for i in range(2*n):
	around = around.shiftLabel()
	print K.sameDiagram(around)
	# Should be True
	if not K.sameDiagram(around):
		raise TypeError("These are different diagrams!")
		
N = ADT.ADT([6, 12, 8, 2, 10, -4], [-1, -1, -1, -1, 1, -1])
print K.sameDiagram(N)
# Should be False
if K.sameDiagram(N):
	raise TypeError("These shouldn't be the same diagram!")