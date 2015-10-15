import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from ADT import *
from ADTComplex import *
#L = ADT([2],[1])
L = ADT([4,6,2],[-1,-1,-1])
#L = ADT([4,6,8,2],[-1,1,-1,1])
#L = ADT([4,8,10,2,6],[-1,-1,-1,-1,-1])
K = ADTComplex(L)

print "Nodes: %4d" % (K.n_nodes)
for i in range(1,K.n_nodes+1):
    print i, K.valency(i), K.flower(i)    
