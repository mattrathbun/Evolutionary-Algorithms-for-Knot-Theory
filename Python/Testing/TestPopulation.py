import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADTOpPopulation

def fit(ol):
    return ol.length()

pop = ADTOpPopulation.Population(10,10,5)

print "pop.size() = %d\n" % (pop.size())

ol = pop.toList()
for l in ol:
    print [op.toString() for op in l.toList()]

pop.iterate(fit)
