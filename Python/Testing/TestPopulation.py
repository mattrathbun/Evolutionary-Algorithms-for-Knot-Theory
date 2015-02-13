import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADTOpPopulation

def fit(ol):
#    return ol.length()
#    return ol.upCount()
    return ol.upCount() + ol.horizontalCount()

pop = ADTOpPopulation.Population(10,10,5, 'Move')

print "pop.size() = %d\n" % (pop.size())

ol = pop.toList()
for l in ol:
    print [op.toString() for op in l.toList()]

for i in range(0,10):
    pop.iterate(fit)

ol = pop.toList()
for l in ol:
    print [op.toString() for op in l.toList()]
