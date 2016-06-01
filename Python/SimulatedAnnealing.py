#import os, sys
#lib_path = os.path.abspath('../')
#sys.path.append(lib_path)
import ADT, ADTOp, ADTOpList, AllDiagrams

K = ADT.ADT([4,8,12,2,14,6,10], [1, 1, 1, 1, -1, 1, -1])
Kname = "7_6"

print "%s : %s\n" % (Kname, K.to_string())

AllDiagrams.init()

temperature = 2
k_param = 1.0
n = 0

while True:
    move = ADTOp.simpleCoarseRandomOp()
    L = K.copy()
    if move.apply(L):
        wildness = K.number_crossings() - L.number_crossings()
        energy_change = K.energy() - L.energy()
        print "wildness: %n"
        if (energy_change<temperature): 
            K = L
        else:
            if random.random() < (1.0/(1.0+exp(energy_change/k_param*temperature))):
                K = L
    print "%s \n" % K.to_string()
    temperature = temperature/log1p(n)
    n = n+1
    
