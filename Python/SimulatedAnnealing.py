#import os, sys
#lib_path = os.path.abspath('../')
#sys.path.append(lib_path)
import ADT, ADTOp, ADTOpList, AllDiagrams
from math import *
from random import *

K = ADT.ADT([4,8,12,2,14,6,10], [1, 1, 1, 1, -1, 1, -1])
Kname = "7_6"

print "%s : %s\n" % (Kname, K.to_string())

AllDiagrams.init()

temperature = 1
k_param = 1.0
n = 2

while True:
    move = ADTOp.simpleCoarseRandomOp()
    L = K.copy()
    if move.apply(L):
        wildness = L.number_crossings() - K.number_crossings()
        energy_change = K.TOK_energy(2.0) - L.TOK_energy(2.0)
        print "wildness: %d" % wildness
        if (energy_change<temperature): 
            K = L.copy()
        else:
            if random() < (1.0/(1.0+exp(energy_change/(k_param*temperature)))):
                K = L.copy()
    print "%s \n".format(K.to_string())
    n = n+1
    temperature = temperature/log(n)

    
