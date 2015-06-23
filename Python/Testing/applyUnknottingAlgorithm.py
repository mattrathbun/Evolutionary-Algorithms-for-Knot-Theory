import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOpPopulation, ADTOpPopulationSets, Fit
import math
from datetime import datetime


def applyUnknottingAlgorithm(fit, K, numiterations):
    startApply = datetime.now()
    pop = ADTOpPopulationSets.Population(25,60,5, model='original')

    print "pop.size() = %d\n" % (pop.size())

    pl = pop.toList()
    for l in pl:
        print [op.toString() for op in l.toList()]

    i = 0
    mu = 0.25
    upMoveBias = 1
    horizontalMoveBias = 1
    downMoveBias = 1
    CCBias = 1
    
    maxfvs = [1, 100, 1, 100, 1, 100, 1, 100, 1, 100, 1]
    while True:
        i += 1
        print "\n"
        print "\n"
        print "\n"
        print "Iteration {} of {}".format(i, numiterations)
        print "pop HAS {} MEMBERS IN IT!!!".format(len(pop.toList()))
        print "\n"
        print "\n"
        print "\n"
        best_opList = pop.iterate(fit, mu = mu, upMoveBias = upMoveBias, downMoveBias = downMoveBias, horizontalMoveBias = horizontalMoveBias, CCBias = CCBias)
#        for l in pop.toList():
#            print [op.toString() for op in l.toList()]
        L = K.copy()
        d, min_ol = best_opList.apply(L)
        
        
        del maxfvs[0]
        maxfvs.append(pop.maxFitness)
        diffs = [abs(maxfvs[j+1] - maxfvs[j]) for j in range(len(maxfvs)-1)]
        x = sum(diffs)/float(len(diffs))
        mu = 0.65*math.exp(-x) + 0.25
        y = math.floor(2*mu) + 1.0
        upMoveBias = int(y)
        horizontalMoveBias = int(y)
        CCBias = int(y)
        
        success = False
        if (min_ol.ccCount() == K.getInvariant('unknottingNumber')) and (d.number_crossings() < 3):
            success = True
        
        if (i == numiterations) or success:
            print "***************************************"
            print "\n"
            print "\n"
            print "\n"
            print "The best sequence we found is:"
            print [op.toString() for op in best_opList.toList()]
            print "It has fitness {}".format(fit(best_opList))
            print "The resulting diagram is:"
            print d.to_string()
            print "It has {} crossings.".format(d.number_crossings())
            print "The (effective) length of the sequence is {}".format(len(min_ol.toList()))
            print "It has {} crossing changes!".format(min_ol.ccCount())
            print "Which compares to a crossing number of {} for the knot {}".format(K.getInvariant('unknottingNumber'), K.to_string())
            if success:
                print "This is a SUCCESS!"
            print "It took us {} of {} iterations to get there".format(i, numiterations)
            
            print "\n"
            print "Finished applyUnknottingAlgorithm. Took: ", datetime.now() - startApply
            return success, i, numiterations, pop, best_opList, min_ol, d


#K = ADT.ADT([6, -2, -10, -14, 4, 12, 8, 16], [-1, -1, 1, 1, -1, 1, -1, -1])

# The knot 7_6
K = ADT.ADT([10, 8, 14, 4, 12, 2, 6], [1, -1, 1, -1, 1, 1, 1])
K.setInvariant('unknottingNumber', 1)

#K = ADT.ADT([-4, -18, -22, -14, -6, -20, -8, -10, -2, -12, -16], [1, 1, 1, -1, 1, -1, -1, 1, 1, -1, 1])
#K = ADT.ADT([


# class Fit(object):
#     def __init__(self, a, b, c, target):
#         self.a = a
#         self.b = b
#         self.c = c
#         self.target = target
#     
#     def __call__(self, ol):
#         if ol.fitness == -float('inf'):
#             L = self.target.copy()
#             d, min_ol = ol.apply(L)
#             if d.number_crossings() < 3:
#                 bonus = 10000
#             else:
#                 bonus = 1
#             ccCount = min_ol.ccCount()
#             fitness = 1.0 + bonus/(d.number_crossings()**float(self.a) + ccCount**float(self.b) + min_ol.length()**float(self.c) + 1.0)
#             ol.setFitness = fitness
#             return fitness
#         elif isinstance(ol.fitness, float):
#             return ol.fitness
#         else:
#             raise TypeError("Not sure what self.fitness is.")

# def fit(ol, a=2, b=3, c=1):
# #    print "Starting fit function." 
# #    startfit = datetime.now()
#     if ol.fitness == -float('inf'):
#         L = K.copy()
#         d, min_ol = ol.apply(L)
#         if d.number_crossings() < 3:
#             bonus = 10000
#         else:
#             bonus = 1
#         ccCount = min_ol.ccCount()
# #    print "Finishing fit function. Took: ", datetime.now() - startfit
#         fitness = 1.0 + bonus/(d.number_crossings()**float(a) + ccCount**float(b) + min_ol.length()**float(c) + 1.0)
#         ol.setFitness = fitness
#         return fitness
#     elif isinstance(ol.fitness, float):
#         return ol.fitness
#     else:
#         raise TypeError("Not sure what self.fitness is.")
#     #return 1.0 + bonus/(d.number_crossings()**5.0 + ccCount + 1.0)

#pop = ADTOpPopulationSets.Population(25,30,5, model='randtail')
#pop = ADTOpPopulationSets.Population(50,50,5, model='original')



#param_choice = []
#choice_efficiency = float('inf')
#for c in [1, 2, 3, 4]:
#    for b in [5, 4, 3, 2]:
#        for a in [5, 4, 3, 2]:
#             fit = Fit.Fit(a, b, c, K)
#             print "\n"
#             print "Attempting applyUnknottingAlgorithm with parameters a = {}, b = {}, and c = {}".format(a, b, c)
#             print "\n"
#             success, i, numiterations, pop, best, min_ol, d = applyUnknottingAlgorithm(fit, K, 40)
#             if success and float(i)/float(numiterations) < choice_efficiency :
#                 param_choice = [a, b, c]
#                 choice_efficiency = float(i)/float(numiterations)
#             print "\n"
#             print "So far, the best choice of parameters is: ", param_choice
#             print "And it has an efficiency of: ", choice_efficiency
#             print "\n"
# print "\n"
# print "*****************************************"
# print "The best choice of parameters is: ", param_choice
# print "They give us an efficiency of: ", choice_efficiency

fit = Fit.Fit(3, 2, 1, K)
success, j, numiterations, pop, best_opList, min_ol, d = applyUnknottingAlgorithm(fit, K, 100)