import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpPopulation, ADTOpPopulationSets, Fit
import AllDiagrams
from datetime import datetime

AllDiagrams.init()

#fileName = "TestFile"
#fileName = "../../../../../../Dropbox (CSU Fullerton)/TestFileMemory"
fileName = "dump"

#myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestFile", 'a')

print "Starting script."
start = datetime.now()




length = 20 #length of test/target unknot diagrams
attempts = 10 #the number of times we attempt to test the algorithm's effectiveness
#popsize = 10*length #the number of sequences in the population during each attempt
popsize = 10*length #the number of sequences in the population during each attempt
numiterations = 4*length #the maximum number of iterations used in each attempt at the algorithm

def testSimplification():
    fit = Fit.Fit(2, 0, 1, 1, K)
    
#    pop = ADTOpPopulationSets.Population(50,30,15, opPopulationType='Move', model='original')
    pop = ADTOpPopulationSets.Population(popsize,3*length, length/2, opPopulationType='Move', model='original') 

#        print "pop.size() = %d\n" % (pop.size())

    pl = pop.toList()
#        for l in pl:
#            print [op.toString() for op in l.toList()]

#    numiterations is set above
    iteration = 0
    while True:
        myfile = open(fileName, 'a')
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
            
            myfile = open(fileName, 'a')
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
                return 1, iteration
            else:
                return 0, iteration


def testRandomPopulations():
    iteration = 0
    while True:
#        myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparisonOutput", "a")
        myfile = open(fileName, "a")
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
#                myfile = open("../../../../../../Dropbox (CSU Fullerton)/TestSimplificationComparisonOutput", "a")
                myfile = open(fileName, "a")
                myfile.write("Success on iteration {}.".format(iteration))
                myfile.write("\n")
                for op in ol.toList():
                    myfile.write(op.toString())
                myfile.write("\n")
                myfile.write("The resulting diagram is:")
                myfile.write("\n")
                myfile.write(str(d.to_string()))
                myfile.write("\n")
                myfile.close()
                print "Success on iteration {}.\n".format(iteration)
                print [op.toString() for op in ol.toList()]
                print "\nThe resulting diagram is:\n"
                print d.to_string()
                return 1, iteration
        if iteration == numiterations:
            return 0, iteration


def testGreedyGeneticSimplification():
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
                return 1, iteration
            else:
                return 0, iteration


def testGreedySimplification():
##    fit = Fit.Fit(2, 0, 0, 0, K)
    
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
###        best = pop.iterate(fit)
        for ol in pl:
            L1 = K.copy()
            d, min_ol = ol.apply(L1)
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
                for op in ol.toList():
                    myfile.write(op.toString())
##                myfile.write("\n")
##                myfile.write("\n")
##                myfile.write("It has fitness {}".format(fit(ol)))
##                myfile.write("\n")
##                myfile.write("The resulting diagram has {} crossings.".format(d.number_crossings()))
##                myfile.write("\n")
##                myfile.close()
                print "The best sequence we found is:"
                print [op.toString() for op in ol.toList()]
##                print "It has fitness {}".format(fit(ol))
                print "The resulting diagram is:"
                print d.to_string()
                print "It has {} crossings.".format(d.number_crossings())
                print "The (effective) length of the sequence is {}".format(len(min_ol.toList()))
                print "\n"
                if d.number_crossings() < 3:
                    return 1, iteration
                else:
                    return 0, iteration
            else:
                L2 = K.copy()
                ol2 = ol.copy()
                ol2.mutate(model='original', upMoveBias=1, downMoveBias=1, horizontalMoveBias = 1, CCBias = 0)
                d2, min_ol2 = ol2.apply(L2)
                if d2 <= d:
                    ol = ol2
                    


# attempts is set above
simplificationSuccesses = 0
randomSuccesses = 0
greedyGeneticSuccesses = 0
greedySuccesses = 0

simplificationTotalSpeed = 0
randomTotalSpeed = 0
greedyGeneticTotalSpeed = 0
greedyTotalSpeed = 0

for j in range(attempts):
    AllDiagrams.init()
    myfile = open(fileName, 'a')
    print "\n"
    myfile.write("Starting attempt {} of {}.".format(j+1, attempts))
    myfile.write("\n")
    print "Starting attempt {} of {}.".format(j+1, attempts)
    print "\n"
    myfile.close()
    
    K = ADT.ADT([],[])
#    length set above
    while K.number_crossings() < length:
        M = ADTOp.simpleCoarseRandomMove(upBias=3)
        M.apply(K)
    myfile = open(fileName, 'a')
    myfile.write("K is {}".format(K.to_string()))
    myfile.write("\n")
    myfile.close()
    print "K is ", K.to_string()
    print "\n"

    simplificationSuccessful, simplificationSpeed  = testSimplification()
    randomSuccessful, randomSpeed = testRandomPopulations()
    greedyGeneticSuccessful, greedyGeneticSpeed = testGreedyGeneticSimplification()
    greedySuccessful, greedySpeed = testGreedySimplification()

    simplificationSuccesses += simplificationSuccessful
    simplificationTotalSpeed += simplificationSpeed
    
    randomSuccesses += randomSuccessful
    randomTotalSpeed += randomSpeed
    
    greedyGeneticSuccesses += greedyGeneticSuccessful
    greedyGeneticTotalSpeed += greedyGeneticSpeed
    
    greedySuccesses += greedySuccessful
    greedyTotalSpeed += greedySpeed
    
    
myfile = open(fileName, 'a')
myfile.write("Simplificaiton had {}% success!".format(float(simplificationSuccesses)/float(attempts)*100))
myfile.write("    With speed {}.".format(simplificationTotalSpeed))
myfile.write("Random had {}% success!".format(float(randomSuccesses)/float(attempts)*100))
myfile.write("    With speed {}.".format(randomTotalSpeed))
myfile.write("Greedy Genetic Simplification had {}% success!".format(float(greedyGeneticSuccesses)/float(attempts)*100))
myfile.write("    With speed {}.".format(greedyGeneticTotalSpeed))
myfile.write("Greedy Simplification had {}% success!".format(float(greedySuccesses)/float(attempts)*100))
myfile.write("    With speed {}.".format(greedyTotalSpeed))

myfile.write("\n")
    
print "Simplificaiton had {}% success!".format(float(simplificationSuccesses)/float(attempts)*100)
print "    With speed {}.".format(simplificationTotalSpeed)
print "Random had {}% success!".format(float(randomSuccesses)/float(attempts)*100)
print "    With speed {}.".format(randomTotalSpeed)
print "Greedy Genetic Simplification had {}% success!".format(float(greedyGeneticSuccesses)/float(attempts)*100)
print "    With speed {}.".format(greedyGeneticTotalSpeed)
print "Greedy Simplification had {}% success!".format(float(greedySuccesses)/float(attempts)*100)
print "    With speed {}.".format(greedyTotalSpeed)

    
myfile.write("Finished script. Took: {}".format(datetime.now() - start))
myfile.write("\n")
myfile.close()
print "Finished script. Took: ", datetime.now() - start
