import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ADT

print "################################################"
K = ADT.ADT([6, 8, 2, 4], [-1, 1, -1, 1])

print "Here's K before the R2UpPlus move:"
print K.to_list()
print "\n"

L = K.copy()
print "Here's an attempt at an R2UpPlus move on 1 to the right at [5, 4]"
# L.R2UpPlus(1, 'r', [5, 4])
L.R2Up(1, 'r', [5, 4])
## L = ([10, 8, 12, -2, 4, 6], [-1, -1, 1, 1, -1, 1])
print L.to_list()
print "\n"

L = K.copy()
print "Here's an attempt at an R2UpPlus move on 2 to the right at [4, 5]"
# L.R2UpPlus(2, 'r', [4, 5])
L.R2Up(2, 'r', [4, 5])
## L = ([10, 8, 12, -4, 2, 6], [-1, -1, 1, 1, -1, 1])
print L.to_list()
print "\n"

L = K.copy()
print "Here's an attempt at an R2UpPlus move on 2 to the right at [8, 7]"
# L.R2UpPlus(2, 'r', [8, 7])
L.R2Up(2, 'r', [8, 7])
## L = ([8, 10, 12, 2, 6, -4], [-1, 1, 1, -1, 1, -1])
print L.to_list()
print "\n"

L = K.copy()
print "Here's an attempt at an R2UpPlus move on 2 to the right at [7, 8]"
# L.R2UpPlus(2, 'r', [7, 8])
L.R2Up(2, 'r', [7, 8])
## L = ([6, 8, 2, 4], [-1, 1, -1, 1])
print L.to_list()
print "\n"

L = K.copy()
print "Here's an attempt at an R2UpPlus move on 6 to the right at [4, 3]"
# L.R2UpPlus(6, 'r', [4, 3])
L.R2Up(6, 'r', [4, 3])
## L = ([8, 12, -10, 2, 4, 6], [-1, 1, -1, -1, 1, 1])
print L.to_list()
print "\n"

L = K.copy()
print "Here's an attempt at an R2UpPlus move on 6 to the right at [8, 1]"
# L.R2UpPlus(6, 'r', [8, 1])
L.R2Up(6, 'r', [8, 1])
## L = ([6, 10, 2, 12, 4, -8], [-1, 1, -1, -1, 1, 1])
print L.to_list()
print "\n"

L = K.copy()
print "Here's an attempt at an R2UpPlus move on 3 to the right at [7, 8]"
# L.R2UpPlus(3, 'r', [7, 8])
L.R2Up(3, 'r', [7, 8])
## L = ([8, 12, 10, 2, 6, -4], [-1, 1, 1, -1, 1, -1])
print L.to_list()
print "\n"

L = K.copy()
print "Here's an attempt at an R2UpPlus move on 7 to the left at [3, 2]"
# L.R2UpPlus(7, 'l', [3, 2])
L.R2Up(7, 'l', [3, 2])
## L = ([8, -10, 12, 2, 6, 4], [-1, -1, 1, -1, 1, 1])
print L.to_list()
print "\n"

L = K.copy()
print "Here's an attempt at an R2UpPlus move on 7 to the right at [3, 4]"
# L.R2UpPlus(7, 'r', [3, 4])
L.R2Up(7, 'r', [3, 4])
## L = ([8, 12, -10, 2, 6, 4], [-1, 1, -1, -1, 1, 1])
print L.to_list()
print "\n"

print "################################################"

L = K.copy()
print "Here's an attempt at an R2UpPlus move on 8 to the left at [6, 5]"
L.R2Up(8, 'l', [6, 5])
## L = ([8, 10, 2, -12, 4, 6], [-1, 1, -1, 1, 1, -1])
print L.to_list()
print "\n"

L = K.copy()
print "Here's an attempt at an R2UpPlus move on 8 to the right at [4, 3]"
L.R2Up(8, 'r', [4, 3])
## L = ([8, 10, -12, 2, 6, 4], [-1, 1, -1, -1, 1, 1])
print L.to_list()
print "\n"

L = K.copy()
print "Here's an attempt at an R2UpPlus move on 8 to the right at [3, 4]"
L.R2Up(8, 'r', [3, 4])
## L = ([6, 8, 2, 4], [-1, 1, -1, 1])
print L.to_list()
print "\n"

#N = ADT.ADT([], [])

#print N.R2Up(1, 'l', [1,2])
#print N.to_list()
## This returns an error.

N = ADT.ADT([2], [-1])

print "Here's N before the R2UpPlus move:"
print N.to_list()
print "\n"

L = N.copy()
print "Here's an attempt at an R2UpPlus move on 1 to the left at [1, 2]"
L.R2Up(1, 'l', [1, 2])
## L = ([2], [-1])
print L.to_list()
print "\n"

L = N.copy()
print "Here's an attempt at an R2UpPlus move on 1 to the left at [2, 1]"
L.R2Up(1, 'l', [2, 1])
## L = ([2], [-1])
print L.to_list()
print "\n"

L = N.copy()
print "Here's an attempt at an R2UpPlus move on 1 to the right at [1, 2]"
print L.regions(1, 'r')
L.R2Up(1, 'r', [1, 2])
## L = ([4, 6, -2], [-1, -1, 1])
print L.to_list()
print "\n"


# for i in range(1, 8):
# 	for j in range(1, 7):
# 		L = K.copy()
# 		M = K.copy()
# 		print "Attempting R2UpPlus move at {} on the left to {}".format(i, [j, j+1])
# 		L.R2UpPlus(i, 'l', [j, j+1])
# 		print L.to_list()
# 		print "Attempting R2UpPlus move at {} on the right to {}".format(i, [j, j+1])
# 		M.R2UpPlus(i, 'r', [j, j+1])
	
#K.R2UpPlus(4, 'l', [8, 7])
#print "Here's K after the R2UpPlus move:"
#print K.to_list()


#K = ADT.ADT([-8, -14, 12, -2, -10, -4, 6], [-1, 1, -1, -1, -1, 1, -1])

#K.R2UpPlus(8, 'l', [10, 11])
#print K.to_list()