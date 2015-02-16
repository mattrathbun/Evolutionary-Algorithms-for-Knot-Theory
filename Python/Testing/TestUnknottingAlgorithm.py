import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOpPopulation

#K = ADT.ADT([6, -2, -10, -14, 4, 12, 8, 16], [-1, -1, 1, 1, -1, 1, -1, -1])
K = ADT.ADT([-4, -18, -22, -14, -6, -20, -8, -10, -2, -12, -16], [1, 1, 1, -1, 1, -1, -1, 1, 1, -1, 1])
#K = ADT.ADT([




def fit(ol):
    d, min_ol = ol.apply(K)
    if d.number_crossings() < 3:
        bonus = 10000
    else:
        bonus = 1
    ccCount = ol.ccCount()
    return 1.0 + bonus/(d.number_crossings()**5.0 + ccCount + 1.0)

pop = ADTOpPopulation.Population(10,30,5)

print "pop.size() = %d\n" % (pop.size())

ol = pop.toList()
for l in ol:
    print [op.toString() for op in l.toList()]

for i in range(0,10):
    pop.iterate(fit)

ol = pop.toList()
for l in ol:
    print [op.toString() for op in l.toList()]
