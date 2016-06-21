import os, sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
import ADT, ADTOpPopulation, ADTOpPopulationSets, Fit, AllDiagrams, applyUnknottingAlgorithm
import math, operator
from datetime import datetime

AllDiagrams.init()

parameter_range = 4


#selectFitnessParameters
performance = {}
params = tuple([a,b,c,d] for a in range(parameter_range) for b in range(parameter_range) for c in range(parameter_range) for d in range(parameter_range))
for param in params:
    print "\n"
    print "Attempting applyUnknottingAlgorithm with Fitness parameters a = {}, b = {}, c = {}, and d = {}".format(param[0], param[1], param[2], param[3])
    print "\n"
    f = open('KnotInfoData.txt', 'r')
    f.readline() # Skip the first line, since it will always be the unknot
    successes = 0
    for l in f.readlines():
        code = [int(i) for i in l[l.find("[")+1:l.find("]")].split(",")]
        unknotting_number = l[l.find("],")+3]
        print "Current knot is K = {}".format(code)
        try:
            unknotting_number = int(unknotting_number)
        except KeyError:
            print "Unknotting number for K is currently unknown."
            continue
        except ValueError:
            print "Unknotting number for K is currently unknown."
            continue
        n = len(code)
        K = ADT.ADT(code, [1]*n)
        K.setInvariant('unknottingNumber', unknotting_number)
        print "K has unknotting number {}".format(K.getInvariant('unknottingNumber'))
        fit = Fit.Fit(param[0], param[1], param[2], param[3], K)
        success, j, numiterations, pop, best_opList, min_ol, d = applyUnknottingAlgorithm.applyUnknottingAlgorithm(fit = fit, K = K, numiterations = 100, unknotting_number_known=True)
        if success:
            successes += 1
    f.close()
    print "Finished cycling through knots. Had {} out of 2978 successes.".format(successes)
    performance[tuple(param)] = successes
print "\nFinished cycling through all the different parameters."
print "\nThe best performing parameters are \n"
print max(performance.iteritems(), key=operator.itemgetter(1))[0]
print "\nThey resulted in successfully efficient unknotting for"
print max(performance.iteritems(), key=operator.itemgetter(1))[1]
print "\n of the 2978 knots up to 12 crossings!!"























