import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ADT

K = ADT.ADT([-6,10,12,-2,4,-8],[1,1,-1,1,1,1])
#print K.isrealisable()
#print K.to_list()
#print "\n"

#for i in range(1,12):
#    print i,K.right(i),K.doubleRight(i)

print "#############################################################"
print "#### Colin's Original example"
print "#############################################################"

print K.to_list()
print" " 
K.R3(8,'r')
print" "
print "We get    ",K.to_list()
print "Should get ([-6, -8, 12, -2, 10, -4], [1, 1, -1, 1, 1, 1])."

print " "
print "#############################################################"
print "#### Colin's Original example shuffled round"
print "#############################################################"

K = ADT.ADT([8,-12,-10,2,4,-6],[1,1,1,1,-1,1])
print K.to_list()
print" " 
K.R3(12,'r')
print" "
print "We get    ",K.to_list()
#print "Should get ([-6, -8, 12, -2, 10, -4], [1, 1, -1, 1, 1, 1])."

print " "
print "#############################################################"
print "#### Matt's example with the orientation at 3/10 changed to -ve"
print "#############################################################"

K = ADT.ADT([-6, -10, 12, -2, 4, -8], [1, -1, -1, 1, 1, 1])

print K.to_list()
K.R3(8, 'R')
print "We get    ",K.to_list()
print "Should get ([-6, -8, 12, -2, 10, -4], [1, 1, -1, 1, 1, -1])."

print "#############################################################"

print " "
print "#############################################################"
print "#### This code should not be realizable."
print "#############################################################"

K = ADT.ADT([-6, -10, 12, -2, -4, -8], [1, -1, -1, 1, 1, 1])
print K.isrealisable()
print "Should be False."

print "########## Here's where trouble starts!!! ##########"

K = ADT.ADT([-8, -10, -2, -12, 4, 6], [1, -1, 1, 1, 1, -1])
print "Start with K: ", K.to_string()
print "Then perform an R3 move at position 5 on the right."
K.R3(5, "R")
## Should be [-8, 6, -10, -12, 4, 2], [1, 1, -1, 1, 1, -1]
print K.to_string()
## Produces [-8, 6, -10, -12, 4, -2], [1, -1, 1, 1, 1, -1]
if not K.isrealisable():
	raise TypeError("R3 move is not producing a valid diagram!")
	
	
L = ADT.ADT([6, 10, 4, -8, -2, -14, 12], [-1, -1, -1, -1, 1, 1, 1])
print "Start with L: ", L.to_string()
print "Then perform an R3 move at position 1 on the right."
L.R3(1, "R")
## Should be [8, 10, 4, -2, 6, -14, 12], [1, -1, -1, -1, -1, 1, 1]
print L.to_string()
## Produces [8, 10, 4, -2, -6, -14, 12], [-1, -1, -1, 1, -1, 1, 1]
if not L.isrealisable():
	raise TypeError("R3 move is not producing a valid diagram!")
	
M = ADT.ADT([4, -2], [1, 1])
print "Start with M: ", M.to_string()
print "Then perform an R3 move at position 1 on the left."
M.R3(1, "L")
## Should be ....
print M.to_string()
## Produces [-2, -2], [1, 1]
if not M.isrealisable():
	raise TypeError("R3 move is not producing a valid diagram!")
