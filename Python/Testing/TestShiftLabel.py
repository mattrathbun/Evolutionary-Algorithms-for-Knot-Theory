import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ADT

K = ADT.ADT([6, 12, 8, 2, 10, -4], [-1, -1, -1, -1, 1, 1])
L = K.shiftLabel()
print L.to_list()
# Should be ([-6, 10, -12, -4, -8, -2], [-1, 1, -1, -1, 1, -1])
if L != ADT.ADT([-6, 10, -12, -4, -8, -2], [-1, 1, -1, -1, 1, -1]):
	raise TypeError("This is a different diagram!")
	
M = L.shiftLabel()
print M.to_list()
# Should be ([10, 6, 12, 8, -2, 4], [-1, -1, -1, 1, 1, -1])
if M != ADT.ADT([10, 6, 12, 8, -2, 4], [-1, -1, -1, 1, 1, -1]):
	raise TypeError("This is a different diagram!")
	
n = K.number_crossings()
around = K.copy()
for i in range(2*n):
	around = around.shiftLabel()
# Should be K again.
if around != K:
	raise TypeError("This is a different diagram!")
else:
	print "Back to where we started."
	
K = ADT.ADT([2], [-1])
L = K.shiftLabel()
print L.to_list()
# Should be ([-2], [-1])
if L != ADT.ADT([-2], [-1]):
	raise TypeError("This is a different diagram!")
	
K = ADT.ADT([], [])
L = K.shiftLabel()
print L.to_list()
# Should be ([], [])
if L != ADT.ADT([], []):
	raise TypeError("This is a different diagram!")
