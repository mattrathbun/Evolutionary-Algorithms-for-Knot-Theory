import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOpPopulation, ADTOpPopulationSets
from datetime import datetime


def applyUnknottingAlgorithm(fit, K, numiterations):
    startApply = datetime.now()
    pop = ADTOpPopulationSets.Population(30,50,5, model='original')

    print "pop.size() = %d\n" % (pop.size())

    pl = pop.toList()
    for l in pl:
        print [op.toString() for op in l.toList()]

    i = 0
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
        best = pop.iterate(fit)
#        for l in pop.toList():
#            print [op.toString() for op in l.toList()]
        L = K.copy()
        d, min_ol = best.apply(L)
        
        if (i == numiterations) or ((min_ol.ccCount() == K.getInvariant('unknottingNumber')) and (d.number_crossings() < 3)):

            print "***************************************"
            print "\n"
            print "\n"
            print "\n"
            print "The best sequence we found is:"
            print [op.toString() for op in best.toList()]
            print "It has fitness {}".format(fit(best))
            print "The resulting diagram is:"
            print d.to_string()
            print "It has {} crossings.".format(d.number_crossings())
            print "The (effective) length of the sequence is {}".format(len(min_ol.toList()))
            print "It has {} crossing changes!".format(min_ol.ccCount())
            print "Which compares to a crossing number of {} for the knot {}".format(K.getInvariant('unknottingNumber'), K.to_string())
            print "It took us {} of {} iterations to get there".format(i, numiterations)
            
            print "\n"
            print "Finished applyUnknottingAlgorithm. Took: ", datetime.now() - startApply
            return i, numiterations, pop, best, min_ol, d


#K = ADT.ADT([6, -2, -10, -14, 4, 12, 8, 16], [-1, -1, 1, 1, -1, 1, -1, -1])

# The knot 7_6
K = ADT.ADT([10, 8, 14, 4, 12, 2, 6], [1, -1, 1, -1, 1, 1, 1])
K.setInvariant('unknottingNumber', 1)

#K = ADT.ADT([-4, -18, -22, -14, -6, -20, -8, -10, -2, -12, -16], [1, 1, 1, -1, 1, -1, -1, 1, 1, -1, 1])
#K = ADT.ADT([


class Fit(object):
    def __init__(self, a, b, c, target):
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
            ccCount = min_ol.ccCount()
            fitness = 1.0 + bonus/(d.number_crossings()**float(self.a) + ccCount**float(self.b) + min_ol.length()**float(self.c) + 1.0)
            ol.setFitness = fitness
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
pop = ADTOpPopulationSets.Population(50,50,5, model='original')


fit = Fit(2, 3, 1, K)

applyUnknottingAlgorithm(fit, K, 10)
