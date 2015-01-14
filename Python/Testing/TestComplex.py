import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from ADT import *
from ADTComplex import *

#L = ADT([4,6,2],[1,1,1])
L = ADT([6,8,2,4],[-1,1,-1,1])
K = ADTComplex(L)
K.draw_graph()