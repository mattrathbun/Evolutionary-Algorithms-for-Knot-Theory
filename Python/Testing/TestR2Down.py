import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ADT

K = ADT.ADT([6, -8, -10, 12, 4, 2], [-1, -1, -1, -1, 1, 1])
print "K is:"
print K.to_list() 
print "\n"

print "Performing R2Down(4):"
print K.R2Down(4)
# Should be True
print K.to_list()
# Should be: [4, -6, 8, 2], [-1, -1, -1, 1]
if K != ADT.ADT([4, -6, 8, 2], [-1, -1, -1, 1]):
	raise TypeError("Not the right result!") 
print "\n"

print "Performing R2Down(4):"
print K.R2Down(4)
# Should be False
print K.to_list()
if K != ADT.ADT([4, -6, 8, 2], [-1, -1, -1, 1]):
	raise TypeError("Not the right result!") 
print "\n"

print "Now, performing R2Down(2):"
print K.R2Down(2)
# Should be True
print K.to_list()
# Should be: [2, 4], [-1, -1]
if K!= ADT.ADT([2, 4], [-1, -1]):
	raise TypeError("Not the right result!")
print "\n"

L = ADT.ADT([-12, 14, -16, -22, -20, -6, 2, -4, -18, -10, 8], [-1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1])
L1 = L.copy()
L2 = L.copy()
print "L_1 and L_2 are:"
print L.to_list()
print "\n"

# Note: This tests behavior at position 1.
print "Performing R2Down(1) to L_1:"
print L1.R2Down(1)
# Should be True
print L1.to_list()
# Should be: [10, -12, -18, -16, -4, -2, -14, -8, 6], [1, -1, 1, 1, -1, -1, 1, 1, -1]
if L1 != ADT.ADT([10, -12, -18, -16, -4, -2, -14, -8, 6], [1, -1, 1, 1, -1, -1, 1, 1, -1]):
	raise TypeError("Not the right result!")
print "\n"

print "Performing R2Down(12) to L_2:"
print L2.R2Down(12)
# Should be True
print L2.to_list()
# Should be: [10, -12, -18, -16, -4, -2, -14, -8, 6], [1, -1, 1, 1, -1, -1, 1, 1, -1]
if L2 != ADT.ADT([10, -12, -18, -16, -4, -2, -14, -8, 6], [1, -1, 1, 1, -1, -1, 1, 1, -1]):
	raise TypeError("Not the right result!")
print "\n"

print "Are L_1 and L_2 equal after these moves?"
print L1 == L2
# Should be True
print "\n"

print "L is {}".format(L.to_list())
print "Performing R2Down(10)"
print L.R2Down(10)
# Should be False
print L.to_list()
# Should be [-12, 14, -16, -22, -20, -6, 2, -4, -18, -10, 8], [-1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1]
if L != ADT.ADT([-12, 14, -16, -22, -20, -6, 2, -4, -18, -10, 8], [-1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1]):
	raise TypeError("Not the right result!")
print "\n"

print "Performing R2Down(9)"
print L.R2Down(9)
# Should be False
print L.to_list()
if L != ADT.ADT([-12, 14, -16, -22, -20, -6, 2, -4, -18, -10, 8], [-1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1]):
	raise TypeError("Not the right result!")
print "\n"

print "Testing L={} for all locations of R2Down moves".format(L.to_list())
moves = []
for i in range(1, 22):
	Ltest = L.copy()
	if Ltest.R2Down(i):
		moves.append(i)
print moves
# Should be [1, 3, 7, 8, 12, 14, 20, 21]
if moves != [1, 3, 7, 8, 12, 14, 20, 21]:
	raise TypeError("Not the right result!")
print "\n"
		
M = ADT.ADT([2, -4], [1, -1])
print "M is:"
print M.to_list()
print "\n"

print "Performing R2Down(4)"
print M.R2Down(4)
print M.to_list()
# Should be [], []
if M != ADT.ADT([], []):
	raise TypeError("Not the right result!")
print "\n"

N = ADT.ADT([6, 4, -8, -2], [-1, -1, 1, 1])
print "N is:"
print N.to_list()
print "\n"

print "Performing R2Down(8)"
print N.R2Down(8)
print N.to_list()
# Should be [-2, 4], [1, -1]
if N != ADT.ADT([-2, 4], [1, -1]):
	raise TypeError("Not the right result!")
print "\n"

K = ADT.ADT([6, -8, 2, 4], [1, 1, 1, -1])
print "K is:"
print K.to_list()
print "\n"

print "Performing R2Down(7)"
print K.R2Down(7)
print K.to_list()
# Should be [4, 2], [1, 1]
if K != ADT.ADT([4, 2], [1, 1]):
	raise TypeError("Not the right result!")
print "\n"

L = ADT.ADT([4, -6, -8, -2], [1, 1, -1, 1])
L1 = L.copy()
L2 = L.copy()
print "L1 and L2 are:"
print L.to_list()
print "\n"

print "Performing R2Down(4) to L1"
print L1.R2Down(4)
print L1.to_list()
# Should be [-2, -4], [1, 1]
if L1 != ADT.ADT([-2, -4], [1, 1]):
	raise TypeError("Not the right result!")
print "\n"

print "Performing R2Down(8) to L2"
print L2.R2Down(8)
print L2.to_list()
# Should be [-2, -4], [1, 1]
if L2 != ADT.ADT([-2, -4], [1, 1]):
	raise TypeError("Not the right result!")
print "\n"
	
M = ADT.ADT([6, 8, -2, 4], [-1, 1, 1, 1])
print "M is:"
print M.to_list()
print "\n"

print "Performing R2Down(1)"
print M.R2Down(1)
print M.to_list()
# Should be [4, 2], [1, 1]
if M != ADT.ADT([4, 2], [1, 1]):
	raise TypeError("Not the right result!")
print "\n"

N = ADT.ADT([-4, 6, -8, -2], [1, 1, 1, -1])
print "N is:"
print N.to_list()
print "\n"

print "Performing R2Down(6)"
print N.R2Down(6)
# Should be [-2, -4], [1, 1]
print N.to_list()
if N != ADT.ADT([-2, -4], [1, 1]):
	raise TypeError("Not the right result!")
print "\n"

K = ADT.ADT([-4, 6, -2], [-1, 1, -1])
print "K is:"
print K.to_list()
print "\n"

print "Performing R2Down(6)"
print K.R2Down(6)
#Should be [-2], [-1]
print K.to_list()
if K != ADT.ADT([-2], [-1]):
	raise TypeError("Not the right result!")
print "\n"


