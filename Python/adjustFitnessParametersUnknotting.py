import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOpPopulation, ADTOpPopulationSets, Fit, AllDiagrams, applyUnknottingAlgorithm
import math
from datetime import datetime



def adjustFitnessParameters(K, parameter_range):
    choice_efficiency = float('inf')
    param_choice = []
    params = tuple([a,b,c,d] for a in range(parameter_range) for b in range(parameter_range) for c in range(parameter_range) for d in range(parameter_range))
    for param in params:
        fit = Fit.Fit(param[0], param[1], param[2], param[3], K)
        print "\n"
        print "Attempting applyUnknottingAlgorithm with Fitness parameters a = {}, b = {}, c = {}, and d = {}".format(param[0], param[1], param[2], param[3])
        print "\n"
        success, j, numiterations, pop, best_opList, min_ol, d = applyUnknottingAlgorithm.applyUnknottingAlgorithm(fit = fit, K = K, numiterations = 100, unknotting_number_known=True)
        if success and float(j)/float(numiterations) < choice_efficiency :
            param_choice = [param[0], param[1], param[2], param[3]]
            choice_efficiency = float(j)/float(numiterations)
            print "\n"
            print "So far, the best choice of parameters is: ", param_choice
            print "And it has an efficiency of: ", choice_efficiency
            print "\n"
    print "\n"
    print "*****************************************"
    print "The best choice of parameters is: ", param_choice
    print "They give us an efficiency of: ", choice_efficiency
    return param_choice, choice_efficiency
    
    
# The knot 7_6
# K = ADT.ADT([10, 8, 14, 4, 12, 2, 6], [1, -1, 1, -1, 1, 1, 1])
# K.setInvariant('unknottingNumber', 1)
# adjustFitnessParameters(K, 3)

# The trefoil
# K = ADT.ADT([4,6,2], [1,1,1])
# K.setInvariant('unknottingNumber', 1)
# adjustFitnessParameters(K, 5)