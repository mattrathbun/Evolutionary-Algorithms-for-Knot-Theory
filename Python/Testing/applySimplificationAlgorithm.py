import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOpList, ADTOpPopulation, ADTOpPopulationSets
import math
from datetime import datetime


def applySimplificationAlgorithm(fit, K, numiterations, up=1, hor=1, down=1):
    startApply = datetime.now()
    pop = ADTOpPopulationSets.Population(25, 40, 5, opPopulationType='Move', model='original')

    print "pop.size() = %d\n" % (pop.size())

    pl = pop.toList()
    for l in pl:
        print [op.toString() for op in l.toList()]

    i = 0
    mu = 0.25
    upMoveBias = up
    horizontalMoveBias = hor
    downMoveBias = down
    
    maxfvs = [1, 100, 1, 100, 1, 100, 1, 100, 1, 100, 1]
    while True:
        i += 1
        print "\n"
        print "\n"
        print "Iteration {} of {}".format(i, numiterations)
        print "\n"
        print "\n"
        pop.iterate(fit, mu = mu, upMoveBias = upMoveBias, downMoveBias = downMoveBias, horizontalMoveBias = horizontalMoveBias, CCBias = 0)
        best_opList = pop.getFittestMember(fit)[1]
        #        for l in pop.toList():
#            print [op.toString() for op in l.toList()]
        L = K.copy()
        d, min_ol = best_opList.apply(L)
        
        
        del maxfvs[0]
        maxfvs.append(pop.maxFitness)
        diffs = [abs(maxfvs[j+1] - maxfvs[j]) for j in range(len(maxfvs)-1)]
        x = sum(diffs)/float(len(diffs))
        mu = 0.35*math.exp(-x) + 0.25
#        y = math.floor(2*mu) + 1.0
#        upMoveBias = int(y)
#        horizontalMoveBias = int(y)
#        CCBias = int(y)
        
        success = False
        if d.number_crossings() < 3:
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
            if success:
                print "This is a SUCCESS!"
            print "It took us {} of {} iterations to get there".format(i, numiterations)
            
            print "\n"
            print "Finished applyUnknottingAlgorithm. Took: ", datetime.now() - startApply
            return success, i, numiterations, pop, best_opList, min_ol, d


# A randomly generated diagram of the unknot:
# K = ADT.ADT([8, 2, -4, -6, -14, -12, 10], [-1, -1, 1, 1, -1, 1, 1])


class Fit(object):
    def __init__(self, a, b, c, target=None):
        self.a = a
        self.b = b
        self.c = c
        self.target = target
    
    def __call__(self, ol):
        if ol.fitness == -float('inf'):
            L = self.target.copy()
            d, min_ol = ol.apply(L)
            if d.number_crossings() < 3:
                bonus = 10000
            else:
                bonus = 1
#            ccCount = min_ol.ccCount()
            fitness = 1.0 + bonus/(d.number_crossings()**float(self.a) + min_ol.length()**float(self.b) + abs(ol.length() - min_ol.length())**float(self.c) + 1.0)
            ol.setFitness(fitness)
            return fitness
        elif isinstance(ol.fitness, float):
            return ol.fitness
        else:
            raise TypeError("Not sure what self.fitness is.")

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



# param_choice = []
# choice_efficiency = float('inf')
# for c in [1, 2, 3]:
#     for b in [1, 2, 3]:
#         for a in [4, 3, 2]:
#              fit = Fit(a, b, c, K)
#              print "\n"
#              print "Attempting applyUnknottingAlgorithm with parameters a = {}, b = {}, and c = {}".format(a, b, c)
#              print "\n"
#              success, j, numiterations, pop, best_opList, min_ol, d = applySimplificationAlgorithm(fit, K, 100)
#              if success and float(j)/float(numiterations) < choice_efficiency :
#                  param_choice = [a, b, c]
#                  choice_efficiency = float(j)/float(numiterations)
#              print "\n"
#              print "So far, the best choice of parameters is: ", param_choice
#              print "And it has an efficiency of: ", choice_efficiency
#              print "\n"
# print "\n"
# print "*****************************************"
# print "The best choice of parameters is: ", param_choice
# print "They give us an efficiency of: ", choice_efficiency

# Parameters for fitness model suggested by a *brief* experimentation process. Could well be refined.
# a = 4, b = 3, c = 3

def testSimplificationAlgorithm(duration, seqLen):
    sumEfficiency = 0
    successes = 0
    for k in range(duration):
        ol = ADTOpList.randomMoveList(seqLen, seqLen)
        L = ADT.ADT([],[])
        for op in ol.toList():
            op.apply(L)
        fit = Fit(4, 3, 3, L)
        success, i, numiterations, pop, best_opList, min_ol, d = applySimplificationAlgorithm(fit, L, 40)
        if success:
            successes += 1
            sumEfficiency += float(i+1)/float(numiterations)
        else:
            sumEfficiency += 1.0
    aveEfficiency = sumEfficiency/float(duration)
    successRate = float(successes)/float(duration)
    print "We have a success rate of {}".format(successRate)
    print "Overall we have an efficiency of {}".format(aveEfficiency)
    return successRate, aveEfficiency
    
testSimplificationAlgorithm(10, 20)
                

# param_choice = []
# choice_efficiency = float('inf')
# for down in [1, 2, 3]:
#     for hor in [1, 2, 3]:
#         for up in [1, 2, 3]:
#             print "\n"
#             print "Attempting applyUnknottingAlgorithm with parameters up = {}, hor = {}, down = {}, and cc = {}".format(up, hor, down, cc)
#             print "\n"
#             success, j, numiterations, pop, best_opList, min_ol, d = applyUnknottingAlgorithm(fit = fit, K = K, numiterations = 100, up = up, hor = hor, down = down, cc = cc)
#             if success and float(i)/float(numiterations) < choice_efficiency :
#                 param_choice = [up, hor, down, cc]
#                 choice_efficiency = float(i)/float(numiterations)
#             print "\n"
#             print "So far, the best choice of parameters is: ", param_choice
#             print "And it has an efficiency of: ", choice_efficiency
#             print "\n"
# print "\n"
# print "*****************************************"
# print "The best choice of parameters is: ", param_choice
# print "They give us an efficiency of: ", choice_efficiency


