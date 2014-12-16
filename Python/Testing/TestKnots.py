import sage
import os, sys, TestInverses
lib_path = os.path.abspath('../../../../')
sys.path.append(lib_path)

import ADT, ADTOp, ADTOpList, ADTOpPopulation, ADTtoGC, knots


K = ADT.ADT([-4, -2, -8, -6, -12, 10], [-1, -1, -1, -1, 1, -1])

print ADTtoGC.ADTtoGC(K)
