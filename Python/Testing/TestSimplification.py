import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpPopulation, ADTOpPopulationSets
from datetime import datetime

print "Starting script."
start = datetime.now()


#K = ADT.ADT([-16, -4, -6, -26, -10, -20, 24, 2, 14, 18, 22, 12, 8], [1, -1, -1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1])

def fit(ol):
#    print "Starting fit function." 
#    startfit = datetime.now()
#    print "(Just checking. While fit is being called, K = ", K.to_string()
    L = K.copy()
    
    d, min_ol = ol.apply(L)
    if d.number_crossings() < 3:
        bonus = 10000
    else:
        bonus = 1
#    print "Finishing fit function. Took: ", datetime.now() - startfit
    return 1.0 + bonus/(d.number_crossings()**2.0 + min_ol.length() + 1.0)
    #return 1.0 + bonus/(d.number_crossings()**5.0 + ccCount + 1.0)

def testSimplification():

    pop = ADTOpPopulationSets.Population(20,30,5, opPopulationType='Move', model='randtail')

#        print "pop.size() = %d\n" % (pop.size())

    pl = pop.toList()
#        for l in pl:
#            print [op.toString() for op in l.toList()]

    numiterations = 2
    iteration = 0
    while True:
        print "Iteration {} of {}".format(iteration+1, numiterations)
        iteration += 1
        best = pop.iterate(fit)
        L = K.copy()
        d, min_ol = best.apply(L)
        if d.number_crossings() < 3 or iteration == numiterations:
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
            print "The resulting diagram is:"
            print d.to_string()
            print "It has {} crossings.".format(d.number_crossings())
            print "The (effective) length of the sequence is {}".format(len(min_ol.toList()))
            print "\n"
            
            if d.number_crossings() < 3:
                return 1
            else:
                return 0
        
        
attempts = 10
successes = 0
for j in range(attempts):
    K = ADT.ADT([],[])
    length = 14
    while K.number_crossings() < length:
        M = ADTOp.coarseRandomMove(upBias=3)
        M.apply(K)
    print "K is ", K.to_string()
    print "\n"

    successes += testSimplification()
    print "{} successes so far, out of {} attempts.".format(successes, j+1)
    print "\n"
    
print "We had {}% success!".format(float(successes)/float(attempts)*100)
    

print "Finished script. Took: ", datetime.now() - start
