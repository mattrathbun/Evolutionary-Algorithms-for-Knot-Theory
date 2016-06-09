import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOpPopulation, ADTOpPopulationSets, Fit, AllDiagrams, applyUnknottingAlgorithm
import math
from datetime import datetime


# The knot 7_6
K = ADT.ADT([10, 8, 14, 4, 12, 2, 6], [1, -1, 1, -1, 1, 1, 1])
K.setInvariant('unknottingNumber', 1)


fit = Fit.Fit(3, 4, 2, 1, K)

param_choice = []
choice_efficiency = float('inf')
for cc in [1, 2, 3]:
    for down in [1, 2, 3]:
        for hor in [1, 2, 3]:
            for up in [1, 2, 3]:
                print "\n"
                print "Attempting applyUnknottingAlgorithm with parameters up = {}, hor = {}, down = {}, and cc = {}".format(up, hor, down, cc)
                print "\n"
                success, j, numiterations, pop, best_opList, min_ol, d = applyUnknottingAlgorithm.applyUnknottingAlgorithm(fit = fit, K = K, numiterations = 100, up = up, hor = hor, down = down, cc = cc)
                if success and float(j)/float(numiterations) < choice_efficiency :
                    param_choice = [up, hor, down, cc]
                    choice_efficiency = float(j)/float(numiterations)
                print "\n"
                print "So far, the best choice of parameters is: ", param_choice
                print "And it has an efficiency of: ", choice_efficiency
                print "\n"
print "\n"
print "*****************************************"
print "The best choice of parameters is: ", param_choice
print "They give us an efficiency of: ", choice_efficiency
