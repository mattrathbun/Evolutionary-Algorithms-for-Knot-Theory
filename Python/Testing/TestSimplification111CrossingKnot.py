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


length = 111 #length of test/target unknot diagrams
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
                return 1
            else:
                return 0
        
AllDiagrams.init()
print "\n"
K = ADT.ADT([-102, 162, -58, 188, 42, -94, 50, 118, -110, -222, 112, 114, 218, 208, -134, -202, -70, -78, -66, -82, -168, -96, 120, 16, -116, -194, 10, 40, -6, -84, -140, -182, 184, -80, 196, 214, -150, -210, -146, -92, 170, 186, -104, 178, 176, 36, 68, 52, -122, 190, 158, -86, 4, 164, -100, 156, -130, -154, -126, -192, 98, -44, -14, 48, 22, 206, 26, 74, 76, -88, 174, 64, -90, 198, 200, 30, 204, -128, 18, 108, -106, -2, -160, -8, -54, -38, -180, -62, 138, 60, 142, -144, 172, -56, -166, -46, 124, 12, 34, -212, -72, -216, 24, 220, -28, -136, -148, 32, -152, -132, -20], [1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1, -1, 1, 1, -1, 1, -1])
print "K is ", K.to_string()
print "\n"

testSimplification()
    
