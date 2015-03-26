import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOpPopulation
from datetime import datetime

print "Starting script."
start = datetime.now()

#K = ADT.ADT([6, -2, -10, -14, 4, 12, 8, 16], [-1, -1, 1, 1, -1, 1, -1, -1])

#K = ADT.ADT([10, 8, 14, 4, 12, 2, 6], [1, -1, 1, -1, 1, 1, 1])

K = ADT.ADT([-4, -18, -22, -14, -6, -20, -8, -10, -2, -12, -16], [1, 1, 1, -1, 1, -1, -1, 1, 1, -1, 1])
#K = ADT.ADT([




def fit(ol):
#    print "Starting fit function." 
#    startfit = datetime.now()
    L = K.copy()
    d, min_ol = ol.apply(L)
    if d.number_crossings() < 3:
        bonus = 10000
    else:
        bonus = 1
    ccCount = min_ol.ccCount()
#    print "Finishing fit function. Took: ", datetime.now() - startfit
    return 1.0 + bonus/(d.number_crossings()**3.0 + ccCount**2.0 + min_ol.length() + 1.0)
    #return 1.0 + bonus/(d.number_crossings()**5.0 + ccCount + 1.0)

pop = ADTOpPopulation.Population(25,30,5, model='modtail')

print "pop.size() = %d\n" % (pop.size())

pl = pop.toList()
for l in pl:
    print [op.toString() for op in l.toList()]

numiterations = 20

for i in range(0,numiterations):
    print "Iteration {} of {}".format(i, numiterations)
    best = pop.iterate(fit)
    for l in pop.toList():
        print [op.toString() for op in l.toList()]

print "***************************************"
print "\n"
print "\n"
pl = pop.toList()
for l in pl:
    print [op.toString() for op in l.toList()]

print "\n"
print "\n"
print "The best sequence we found is:"
print [op.toString() for op in best.toList()]
print "It has fitness {}".format(fit(best))
L = K.copy()
d, min_ol = best.apply(L)
print "The resulting diagram is:"
print d.to_string()
print "It has {} crossings.".format(d.number_crossings())
print "The (effective) length of the sequence is {}".format(len(min_ol.toList()))
print "And it has only {} crossing changes!".format(min_ol.ccCount())


print "Finished script. Took: ", datetime.now() - start
