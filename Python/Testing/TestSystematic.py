import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ADT, ADTOp, ADTOpList

l = ADTOpList.randomOpList(10, 1)
for i in l:
	print i