import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOpPopulation
from datetime import datetime

print "Starting script."
start = datetime.now()

#K = ADT.ADT([6, -2, -10, -14, 4, 12, 8, 16], [-1, -1, 1, 1, -1, 1, -1, -1])
K = ADT.ADT([-4, -18, -22, -14, -6, -20, -8, -10, -2, -12, -16], [1, 1, 1, -1, 1, -1, -1, 1, 1, -1, 1])
#K = ADT.ADT([




def fit(ol):
    print "Starting fit function." 
    startfit = datetime.now()
    d, min_ol = ol.apply(K)
    if d.number_crossings() < 3:
        bonus = 10000
    else:
        bonus = 1
    ccCount = ol.ccCount()
    print "Finishing fit function. Took: ", datetime.now() - startfit
    return 1.0 + bonus/(d.number_crossings()**3.0 + ccCount + 1.0)
    #return 1.0 + bonus/(d.number_crossings()**5.0 + ccCount + 1.0)

pop = ADTOpPopulation.Population(10,30,5, model='randtail')

print "pop.size() = %d\n" % (pop.size())

ol = pop.toList()
for l in ol:
    print [op.toString() for op in l.toList()]

for i in range(0,10):
    pop.iterate(fit)

ol = pop.toList()
for l in ol:
    print [op.toString() for op in l.toList()]

print "Finished script. Took: ", datetime.now() - start