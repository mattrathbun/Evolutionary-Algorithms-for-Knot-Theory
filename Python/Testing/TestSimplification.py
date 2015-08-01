import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpPopulation, ADTOpPopulationSets, Fit
from datetime import datetime

print "Starting script."
start = datetime.now()


def testSimplification():
    fit = Fit.Fit(2, 0, 1, 1, K)
    
    pop = ADTOpPopulationSets.Population(25,50,12, opPopulationType='Move', model='original')

#        print "pop.size() = %d\n" % (pop.size())

    pl = pop.toList()
#        for l in pl:
#            print [op.toString() for op in l.toList()]

    numiterations = 20
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
    print "\n"
    print "Starting attempt {} of {}.".format(j+1, attempts)
    print "\n"
    
    K = ADT.ADT([],[])
    length = 12
    while K.number_crossings() < length:
        M = ADTOp.simpleCoarseRandomMove(upBias=3)
        M.apply(K)
    print "K is ", K.to_string()
    print "\n"

    successes += testSimplification()
    print "{} successes so far, out of {} attempts.".format(successes, j+1)
    print "\n"
    
print "We had {}% success!".format(float(successes)/float(attempts)*100)
    

print "Finished script. Took: ", datetime.now() - start
