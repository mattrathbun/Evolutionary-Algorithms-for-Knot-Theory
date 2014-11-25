import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ADT, ADTOp

def testR2Up(diagram, arc, side, target, expected=None):
	print "The diagram before the move is: ", diagram.to_list()
	print "Attempting to perform an R2Up move at arc {}, on side {}, with target {}".format(arc, side, target)
	diagram.R2Up(arc, side, target)
	print "The result is: ", diagram.to_list()
	if not diagram.isrealisable():
		raise TypeError("R2Up move is not producing a valid diagram!")
	if expected != None:
		if not diagram.sameDiagram(expected):
			print "The result should be: ", expected.to_list()
			raise TypeError("R2Up move is not producing the expected diagram!")
	print '\n'
			
K = ADT.ADT([2], [-1])
for i in [1,2]:
	for j in ["L", "R"]:
		for k in [[1, 2], [2, 1]]:
			bool = K.R2Up(i, j, k)
			print bool
			# Should be False
			if bool:
				raise TypeError("Shouldn't be able to perform this move!")
print '\n'

K = ADT.ADT([], [])
for j in ["L", "R"]:
	for k in [[], [1, 1], [1, 2]]:
		bool = K.R2Up(1, j, k)
		print bool
		if bool:
			raise TypeError("Shouldn't be able to perform this move!")
print '\n'
 			
K = ADT.ADT([4, -2], [-1, 1])
testR2Up(K, 1, "L", [3, 4], ADT.ADT([8, 6, -4, -2], [-1, -1, 1, 1]))
# Should be ([8, 6, -4, -2], [-1, -1, 1, 1])
print '\n'

K = ADT.ADT([4, -2], [-1, 1])
bool = K.R2Up(1, "L", [4, 3])
print bool
# Should be False
if bool:
	raise TypeError("This isn't the right result!")
print '\n'

K = ADT.ADT([4, -2], [-1, 1])
bool = K.R2Up(1, "R", [2, 3])
print bool
# Should be False
if bool:
	raise TypeError("This isn't the right result!")
print '\n'


K = ADT.ADT([4, -2], [-1, 1])
testR2Up(K, 1, "R", [3, 2], ADT.ADT([8, 6, -2, -4], [-1, -1, 1, 1]))
# Should be ([8, 6, -2, -4], [-1, -1, 1, 1])

# K4 = K.copy()
# K4.R2Up(1, "R", [3, 2])
# print K4.to_list()
# # Should be ([8, 6, -2, -4], [-1, -1, 1, 1])
# if K4 != ADT.ADT([8, 6, -2, -4], [-1, -1, 1, 1]):
# 	raise TypeError("This isn't the right result!")
# print '\n'
	

K = ADT.ADT([4, -2], [-1, 1])

for i in [[2, 3], [3, 2]]:
	bool = K.R2Up(2, "R", i)
	print bool
	# Should be False
	if bool:
		raise TypeError("This isn't the right result!")
print '\n'

L = ADT.ADT([-6, 8, -10, -2, -4], [-1, 1, -1, -1, -1])
testR2Up(L, 10, "R", [6, 5], ADT.ADT([-8, 10, -12, -14, -2, -4, 6], [-1, 1, -1, -1, -1, -1, 1]))
# Should be ([-8, 10, -12, -14, -2, -4, 6], [-1, 1, -1, -1, -1, -1, 1])

# L.R2Up(10, "R", [6, 5])
# print L.to_list()
# # Should be ([-8, 10, -12, -14, -2, -4, 6], [-1, 1, -1, -1, -1, -1, 1])
# if L != ADT.ADT([-8, 10, -12, -14, -2, -4, 6], [-1, 1, -1, -1, -1, -1, 1]):
# 	raise TypeError("This isn't the right result!")
# print '\n'

K = ADT.ADT([6, 8, 2, 4], [-1, 1, -1, 1])


L = K.copy()
testR2Up(L, 1, "R", [5, 4], ADT.ADT([10, 8, 12, -2, 4, 6], [-1, -1, 1, 1, -1, 1]))
# Should be [10, 8, 12, -2, 4, 6], [-1, -1, 1, 1, -1, 1]

# print "Here's an attempt at an R2Up move on 1 to the right at [5, 4]"
# # L.R2UpPlus(1, 'r', [5, 4])
# L.R2Up(1, 'r', [5, 4])
# ## L = ([10, 8, 12, -2, 4, 6], [-1, -1, 1, 1, -1, 1])
# print L.to_list()
# if L != ADT.ADT([10, 8, 12, -2, 4, 6], [-1, -1, 1, 1, -1, 1]):
# 	raise TypeError("Not the right result!")
# print "\n"

 
L = K.copy()
testR2Up(L, 2, "R", [4, 5], ADT.ADT([10, 8, 12, -4, 2, 6], [-1, -1, 1, 1, -1, 1]))
# Should be [10, 8, 12, -4, 2, 6], [-1, -1, 1, 1, -1, 1]

# print "Here's an attempt at an R2Up move on 2 to the right at [4, 5]"
# L.R2Up(2, 'r', [4, 5])
# print L.to_list()
# if L != ADT.ADT([10, 8, 12, -4, 2, 6], [-1, -1, 1, 1, -1, 1]):
# 	raise TypeError("Not the right result!")
# print "\n"


L = K.copy()
testR2Up(L, 2, "R", [8, 7], ADT.ADT([8, 10, 12, 2, 6, -4], [-1, 1, 1, -1, 1, -1]))
# Should be [8, 10, 12, 2, 6, -4], [-1, 1, 1, -1, 1, -1]

# print "Here's an attempt at an R2Up move on 2 to the right at [8, 7]"
# # L.R2UpPlus(2, 'r', [8, 7])
# L.R2Up(2, 'r', [8, 7])
# ## L = ([8, 10, 12, 2, 6, -4], [-1, 1, 1, -1, 1, -1])
# print L.to_list()
# if L != ADT.ADT([8, 10, 12, 2, 6, -4], [-1, 1, 1, -1, 1, -1]):
# 	raise TypeError("Not the right result!")
# print "\n"

 
L = K.copy()
testR2Up(L, 2, "R", [7, 8], ADT.ADT([6, 8, 2, 4], [-1, 1, -1, 1]))
# Should be [6, 8, 2, 4], [-1, 1, -1, 1]

# print "Here's an attempt at an R2Up move on 2 to the right at [7, 8]"
# # L.R2UpPlus(2, 'r', [7, 8])
# L.R2Up(2, 'r', [7, 8])
# ## L = ([6, 8, 2, 4], [-1, 1, -1, 1])
# print L.to_list()
# if L != ADT.ADT([6, 8, 2, 4], [-1, 1, -1, 1]):
# 	raise TypeError("Not the right result!")
# print "\n"

 
L = K.copy()
testR2Up(L, 6, "R", [4, 3], ADT.ADT([8, 12, -10, 2, 4, 6], [-1, 1, -1, -1, 1, 1]))
# Should be [8, 12, -10, 2, 4, 6], [-1, 1, -1, -1, 1, 1]

# print "Here's an attempt at an R2Up move on 6 to the right at [4, 3]"
# # L.R2UpPlus(6, 'r', [4, 3])
# L.R2Up(6, 'r', [4, 3])
# ## L = ([8, 12, -10, 2, 4, 6], [-1, 1, -1, -1, 1, 1])
# print L.to_list()
# if L != ADT.ADT([8, 12, -10, 2, 4, 6], [-1, 1, -1, -1, 1, 1]):
# 	raise TypeError("Not the right result!")
# print "\n"
# 

L = K.copy()
testR2Up(L, 6, "R", [8, 1], ADT.ADT([6, 10, 2, 12, 4, -8], [-1, 1, -1, -1, 1, 1]))
# Should be [6, 10, 2, 12, 4, -8], [-1, 1, -1, -1, 1, 1]

# print "Here's an attempt at an R2Up move on 6 to the right at [8, 1]"
# # L.R2UpPlus(6, 'r', [8, 1])
# L.R2Up(6, 'r', [8, 1])
# ## L = ([6, 10, 2, 12, 4, -8], [-1, 1, -1, -1, 1, 1])
# print L.to_list()
# if L != ADT.ADT([6, 10, 2, 12, 4, -8], [-1, 1, -1, -1, 1, 1]):
# 	raise TypeError("Not the right result!")
# print "\n"
 
L = K.copy()
testR2Up(L, 3, "R", [7, 8], ADT.ADT([8, 12, 10, 2, 6, -4], [-1, 1, 1, -1, 1, -1]))
# Should be [8, 12, 10, 2, 6, -4], [-1, 1, 1, -1, 1, -1]

# print "Here's an attempt at an R2Up move on 3 to the right at [7, 8]"
# # L.R2UpPlus(3, 'r', [7, 8])
# L.R2Up(3, 'r', [7, 8])
# ## L = ([8, 12, 10, 2, 6, -4], [-1, 1, 1, -1, 1, -1])
# print L.to_list()
# if L != ADT.ADT([8, 12, 10, 2, 6, -4], [-1, 1, 1, -1, 1, -1]):
# 	raise TypeError("Not the right result!")
# print "\n"
 
L = K.copy()
testR2Up(L, 7, "L", [3, 2], ADT.ADT([8, -10, 12, 2, 6, 4], [-1, -1, 1, -1, 1, 1]))
# Should be [8, -10, 12, 2, 6, 4], [-1, -1, 1, -1, 1, 1]

# print "Here's an attempt at an R2Up move on 7 to the left at [3, 2]"
# # L.R2UpPlus(7, 'l', [3, 2])
# L.R2Up(7, 'l', [3, 2])
# ## L = ([8, -10, 12, 2, 6, 4], [-1, -1, 1, -1, 1, 1])
# print L.to_list()
# if L != ADT.ADT([8, -10, 12, 2, 6, 4], [-1, -1, 1, -1, 1, 1]):
# 	raise TypeError("Not the right result!")
# print "\n"
 
L = K.copy()
testR2Up(L, 7, "R", [3, 4], ADT.ADT([8, 12, -10, 2, 6, 4], [-1, 1, -1, -1, 1, 1]))
# Should be [8, 12, -10, 2, 6, 4], [-1, 1, -1, -1, 1, 1]

# print "Here's an attempt at an R2Up move on 7 to the right at [3, 4]"
# # L.R2UpPlus(7, 'r', [3, 4])
# L.R2Up(7, 'r', [3, 4])
# ## L = ([8, 12, -10, 2, 6, 4], [-1, 1, -1, -1, 1, 1])
# print L.to_list()
# if L != ADT.ADT([8, 12, -10, 2, 6, 4], [-1, 1, -1, -1, 1, 1]):
# 	raise TypeError("Not the right result!")
# print "\n"
 
L = K.copy()
testR2Up(L, 8, "L", [6, 5], ADT.ADT([8, 10, 2, -12, 4, 6], [-1, 1, -1, 1, 1, -1]))
# Should be [8, 10, 2, -12, 4, 6], [-1, 1, -1, 1, 1, -1]

# print "Here's an attempt at an R2Up move on 8 to the left at [6, 5]"
# L.R2Up(8, 'l', [6, 5])
# ## L = ([8, 10, 2, -12, 4, 6], [-1, 1, -1, 1, 1, -1])
# print L.to_list()
# if L != ADT.ADT([8, 10, 2, -12, 4, 6], [-1, 1, -1, 1, 1, -1]):
# 	raise TypeError("Not the right result!")
# print "\n"
 
L = K.copy()
testR2Up(L, 8, "R", [4, 3], ADT.ADT([8, 10, -12, 2, 6, 4], [-1, 1, -1, -1, 1, 1]))
# Should be [8, 10, -12, 2, 6, 4], [-1, 1, -1, -1, 1, 1]

# print "Here's an attempt at an R2Up move on 8 to the right at [4, 3]"
# L.R2Up(8, 'r', [4, 3])
# ## L = ([8, 10, -12, 2, 6, 4], [-1, 1, -1, -1, 1, 1])
# print L.to_list()
# if L != ADT.ADT([8, 10, -12, 2, 6, 4], [-1, 1, -1, -1, 1, 1]):
# 	raise TypeError("Not the right result!")
# print "\n"
 
L = K.copy()
testR2Up(L, 8, "R", [3, 4], ADT.ADT([6, 8, 2, 4], [-1, 1, -1, 1]))
# Should be [6, 8, 2, 4], [-1, 1, -1, 1]

# print "Here's an attempt at an R2Up move on 8 to the right at [3, 4]"
# L.R2Up(8, 'r', [3, 4])
# ## L = ([6, 8, 2, 4], [-1, 1, -1, 1])
# print L.to_list()
# if L != ADT.ADT([6, 8, 2, 4], [-1, 1, -1, 1]):
# 	raise TypeError("Not the right result!")
# print "\n"
  
N = ADT.ADT([2], [-1])
 
L = N.copy()
testR2Up(L, 1, "L", [1, 2], ADT.ADT([2], [-1]))
# Should be [2], [-1]

# print "Here's an attempt at an R2Up move on 1 to the left at [1, 2]"
# L.R2Up(1, 'l', [1, 2])
# ## L = ([2], [-1])
# print L.to_list()
# if L != ADT.ADT([2], [-1]):
# 	raise TypeError("Not the right result!")
# print "\n"
 
L = N.copy()
testR2Up(L, 1, "L", [2, 1], ADT.ADT([2], [-1]))
# Should be [2], [-1]

# print "Here's an attempt at an R2Up move on 1 to the left at [2, 1]"
# L.R2Up(1, 'l', [2, 1])
# ## L = ([2], [-1])
# print L.to_list()
# if L != ADT.ADT([2], [-1]):
# 	raise TypeError("Not the right result!")
# print "\n"
 
L = N.copy()
testR2Up(L, 1, "R", [1, 2], ADT.ADT([2], [-1]))
# Should be [2], [-1]

# print "Here's an attempt at an R2Up move on 1 to the right at [1, 2]"
# print L.regions(1, 'r')
# L.R2Up(1, 'r', [1, 2])
# ## L = ([2], [-1])
# print L.to_list()
# if L != ADT.ADT([2], [-1]):
# 	raise TypeError("Not the right result!")
# print "\n"

#print "####### Problems start HERE!!! ############"

def testR2Problem(diagram, arc, side, target):
	print "Here's the diagram before the R2Up move: ", diagram.to_string()
	print "Here's an attempt at an R2Up move on {} to the {} at {}".format(arc, side, target)
	diagram.R2Up(arc, side, target)
	print K.to_string()
	if not diagram.isrealisable():
		raise TypeError("R2Up move is not producing a valid diagram!")

K = ADT.ADT([-4, 12, 6, -2, 10, -8, -14], [-1, 1, 1, -1, 1, -1, -1])
testR2Up(K, 3, "L", [1, 14], ADT.ADT([-6, 14, 18, 8, -2, 12, -10, -16, -4], [-1, 1, 1, 1, -1, 1, -1, -1, -1]))
# Should be [-6, 14, 18, 8, -2, 12, -10, -16, -4], [-1, 1, 1, 1, -1, 1, -1, -1, -1]

# print "Here's K before the R2Up move: "
# print K.to_string()
# print "Here's an attempt at an R2Up move on 3 to the left at [1, 14]" 
# K.R2Up(3, "L", [1, 14])
# ## Should be: [-6, 14, 18, 8, -2, 12, -10, -16, -4], [-1, 1, 1, 1, -1, 1, -1, -1, -1]
# print K.to_string()
# ## Produces: [-8, 16, 10, 2, -4, 14, -12, -18, -6], [-1, 1, 1, 1, -1, 1, -1, -1, -1]
# if not K.isrealisable():
# 	raise TypeError("R2Up move is not producing a valid diagram!")

	
L = ADT.ADT([-4, -2], [-1, 1])
testR2Up(L, 1, "L", [1, 4], ADT.ADT([-6, 8, -4, -2], [-1, 1, 1, -1]))
# Should be [-6, 8, -4, -2], [-1, 1, 1, -1]

# print "Here's L before the R2Up move: "
# print L.to_string()
# print "Here's an attempt at an R2Up move on 1 to the left at [1, 4]"
# L.R2Up(1, "L", [1, 4])
# ## Should be: [-6, 8, -4, -2], [-1, 1, 1, -1]
# print L.to_string()
# ## Produces: [-8, -6, 2, -4], [-1, 1, 1, -1]
# if not L.isrealisable():
# 	raise TypeError("R2Up move is not producing a valid diagram!")

M = ADT.ADT([-6, 8, 2, -4], [-1, -1, 1, 1])
testR2Up(M, 3, "R", [1, 8])
## !!!!! Should test by hand. UNKNOWN what the result should be.

# print "Here's M before the R2Up move: "
# print M.to_string()
# print "Here's an attempt at an R2Up move on 3 to the right at [1,8]"
# M.R2Up(3, "R", [1,8])
# ## Should be: [
# print M.to_string()
# ## Produces: [-10, 12, 4, 2, -8, -6], [-1, -1, 1, -1, 1, 1]
# if not M.isrealisable():
# 	raise TypeError("R2Up move is not producing a valid diagram!")


K = ADT.ADT([4, -6, 2], [1, -1, 1])
testR2Up(K, 3, "L", [1, 6])
## !!!!! Should test by hand. UNKNOWN what the result should be.

# testR2Problem(K, 3, "L", [1,6])
# ## Should be: ...
# ## Produces: [8, -10, 4, 2, -6], [1, -1, 1, 1, -1]