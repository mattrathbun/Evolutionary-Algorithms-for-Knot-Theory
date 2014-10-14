import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ADT

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
K1 = K.copy()
K1.R2Up(1, "L", [3, 4])
print K1.to_list()
# Should be ([8, 6, -4, -2], [-1, -1, 1, 1])
if K1 != ADT.ADT([8, 6, -4, -2], [-1, -1, 1, 1]):
	raise TypeError("This isn't the right result!")
print '\n'
	
K2 = K.copy()
bool = K2.R2Up(1, "L", [4, 3])
print bool
# Should be False
if bool:
	raise TypeError("This isn't the right result!")
print '\n'

K3 = K.copy()
bool = K3.R2Up(1, "R", [2, 3])
print bool
# Should be False
if bool:
	raise TypeError("This isn't the right result!")
print '\n'

K4 = K.copy()
K4.R2Up(1, "R", [3, 2])
print K4.to_list()
# Should be ([8, 6, -2, -4], [-1, -1, 1, 1])
if K4 != ADT.ADT([8, 6, -2, -4], [-1, -1, 1, 1]):
	raise TypeError("This isn't the right result!")
print '\n'
	
K5 = K.copy()
for i in [[2, 3], [3, 2]]:
	bool = K5.R2Up(2, "R", i)
	print bool
	# Should be False
	if bool:
		raise TypeError("This isn't the right result!")
print '\n'

L = ADT.ADT([-6, 8, -10, -2, -4], [-1, 1, -1, -1, -1])
L.R2Up(10, "R", [6, 5])
print L.to_list()
# Should be ([-8, 10, -12, -14, -2, -4, 6], [-1, 1, -1, -1, -1, -1, 1])
if L != ADT.ADT([-8, 10, -12, -14, -2, -4, 6], [-1, 1, -1, -1, -1, -1, 1]):
	raise TypeError("This isn't the right result!")
print '\n'
	