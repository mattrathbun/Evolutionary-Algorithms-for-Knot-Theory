import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpPopulation, ADTOpPopulationSets, Fit, AllDiagrams
from datetime import datetime

#AllDiagrams.init()

fileName = "dump"

#myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparison2Output", 'a')

print "Starting script."
start = datetime.now()

length = 25 #length of test/target unknot diagrams
attempts = 10 #the number of times we attempt to test the algorithm's effectiveness
popsize = 10*length #the number of sequences in the population during each attempt
numiterations = 4*length #the maximum number of iterations used in each attempt at the algorithm

def testSimplification():
    fit = Fit.Fit(2, 0, 0, 0, K)
    
#    pop = ADTOpPopulationSets.Population(50,30,15, opPopulationType='Move', model='original')
    pop = ADTOpPopulationSets.Population(popsize,3*length, length/2, opPopulationType='Move', model='original') 

#        print "pop.size() = %d\n" % (pop.size())

    pl = pop.toList()
#        for l in pl:
#            print [op.toString() for op in l.toList()]

#    numiterations is set above
    iteration = 0
    while True:
#        myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparison2Output", 'a')
        myfile = open(fileName, "a")
        myfile.write("Iteration {} of {}".format(iteration+1, numiterations))
        myfile.write("\n")
        myfile.close()
        print "Iteration {} of {}".format(iteration+1, numiterations)
        iteration += 1
        pop.iterate(fit)
        best = pop.getFittestMember(fit)[1]
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
            
#            myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparison2Output", 'a')
            myfile = open(fileName, "a")
            myfile.write("The best sequence we found is:\n")
            for op in best.toList():
                myfile.write(op.toString())
                myfile.write("\n")
#            myfile.write([op.toString() for op in best.toList()])
            myfile.write("\n")
            myfile.write("It has fitness {}".format(fit(best)))
            myfile.write("\n")
            myfile.write("The resulting diagram has {} crossings.".format(d.number_crossings()))
            myfile.write("\n")
            myfile.close()
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
        
        
# attempts is set above
successes = 0
for j in range(attempts):
#    myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparison2Output", 'a')
    myfile = open(fileName, "a")
    print "\n"
    myfile.write("Starting attempt {} of {}.".format(j+1, attempts))
    myfile.write("\n")
    print "Starting attempt {} of {}.".format(j+1, attempts)
    print "\n"
    myfile.close()
    
    K = ADT.ADT([],[])
#    length = 10, set above
    while K.number_crossings() < length:
        M = ADTOp.simpleCoarseRandomMove(upBias=3)
        M.apply(K)
#    myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparison2Output", 'a')
    myfile = open(fileName, "a")
    myfile.write("K is {}".format(K.to_string()))
    myfile.write("\n")
    myfile.close()
    print "K is ", K.to_string()
    print "\n"

    successes += testSimplification()
    
#    myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparison2Output", 'a')
    myfile = open(fileName, "a")
    myfile.write("{} successes so far, out of {} attempts.".format(successes, j+1))
    myfile.write("\n")
    myfile.close()
    print "{} successes so far, out of {} attempts.".format(successes, j+1)
    print "\n"
    
#myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparison2Output", 'a')
myfile = open(fileName, "a")
myfile.write("We had {}% success!".format(float(successes)/float(attempts)*100))
myfile.write("\n")
    
print "We had {}% success!".format(float(successes)/float(attempts)*100)
    
myfile.write("Finished script. Took: {}".format(datetime.now() - start))
myfile.write("\n")
myfile.close()
print "Finished script. Took: ", datetime.now() - start
