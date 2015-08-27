import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpPopulation, ADTOpPopulationSets, Fit
from datetime import datetime

#myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestFile", 'a')

print "Starting script."
start = datetime.now()

length = 15 #length of test/target unknot diagrams
attempts = 10 #the number of times we attempt to test the algorithm's effectiveness
popsize = 10*length #the number of sequences in the population during each attempt
numiterations = 4*length #the maximum number of iterations used in each attempt at the algorithm

totalSpeed = 0

def testRandomPopulations():
    iteration = 0
    while True:
        myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparisonOutput", "a")
        myfile.write("Iteration {} of {}".format(iteration+1, numiterations))
    	myfile.write("\n")
    	myfile.close()
        print "Iteration {} of {}".format(iteration+1, numiterations)
        iteration += 1
        pop = ADTOpPopulationSets.Population(popsize, 3*length, length/2, opPopulationType="Move", model="original")
        L = K.copy()
        for ol in pop.toList():
            d, min_ol = ol.apply(L)
            if d.number_crossings() < 3:
                myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparisonOutput", "a")
                myfile.write("Success on iteration {}.".format(iteration))
                myfile.write("\n")
                for op in ol.toList():
                    myfile.write(op.toString())
                myfile.write("\n")
                myfile.write("The resulting diagram is:")
                myfile.write("\n")
                myfile.write(d.to_string())
                myfile.write("\n")
                myfile.close()
                print "Success on iteration {}.\n".format(iteration)
                print [op.toString() for op in ol.toList()]
                print "\nThe resulting diagram is:\n"
                print d.to_string()
                return 1, iteration
        if iteration == numiterations:
            return 0, iteration
            
# attempts is set above
successes = 0
for j in range(attempts):
    myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparisonOutput", 'a')
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
    myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparisonOutput", 'a')
    myfile.write("K is {}".format(K.to_string()))
    myfile.write("\n")
    myfile.close()
    print "K is ", K.to_string()
    print "\n"
    
    successful, speed = testRandomPopulations()
    successes += successful
    totalSpeed += float(speed)/float(numiterations)
    
    myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparisonOutput", 'a')
    myfile.write("{} successes so far, out of {} attempts.".format(successes, j+1))
    myfile.write("\n")
    myfile.close()
    print "{} successes so far, out of {} attempts.".format(successes, j+1)
    print "\n"
    
myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparisonOutput", 'a')
myfile.write("We had {}% success!".format(float(successes)/float(attempts)*100))
myfile.write("\n")
myfile.write("Average speed was {}%".format(float(totalSpeed)/float(attempts)*100))
myfile.write("\n")
    
print "We had {}% success!".format(float(successes)/float(attempts)*100)
print "Average speed was {}%".format(float(totalSpeed)/float(attempts)*100)
    
myfile.write("Finished script. Took: {}".format(datetime.now() - start))
myfile.write("\n")
myfile.close()
print "Finished script. Took: ", datetime.now() - start
