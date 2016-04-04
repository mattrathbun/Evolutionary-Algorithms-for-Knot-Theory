import os, sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
import ADT, ADTOpPopulation, ADTOpPopulationSets, Fit, AllDiagrams
import math
from datetime import datetime

AllDiagrams.init()

def applyUnknottingAlgorithm(fit, K, numiterations, up, hor, down, cc, opChange, opPerm, opRevPerm, opDel, opIns):
    startApply = datetime.now()
    pop = ADTOpPopulationSets.Population(100,100,10, model='original')

    print "pop.size() = %d\n" % (pop.size())

    pl = pop.toList()
    for l in pl:
        print [op.toString() for op in l.toList()]

    i = 0
    mu = 0.25
    upMoveBias = up
    horizontalMoveBias = hor
    downMoveBias = down
    CCBias = cc
    opChangeBias=opChange
    opPermuteBias=opPerm
    opReversePermuteBias=opRevPerm
    opDeletionBias=opDel
    opInsertionBias=opIns
    
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
        best_opList = pop.iterate(fit, mu=mu, upMoveBias=upMoveBias, downMoveBias=downMoveBias, horizontalMoveBias=horizontalMoveBias, CCBias=CCBias, opChangeBias=opChangeBias, opPermuteBias=opPermuteBias, opReversePermuteBias=opReversePermuteBias, opDeletionBias=opDeletionBias, opInsertionBias=opInsertionBias)
#        for l in pop.toList():
#            print [op.toString() for op in l.toList()]
        L = K.copy()
        d, min_ol = best_opList.apply(L)
        
        
        del maxfvs[0]
        maxfvs.append(pop.maxFitness)
        diffs = [abs(maxfvs[j+1] - maxfvs[j]) for j in range(len(maxfvs)-1)]
        x = sum(diffs)/float(len(diffs))
        mu = 0.45*math.exp(-x) + 0.25
        
#        y = math.floor(2*mu) + 1.0
#        upMoveBias = int(y)
#        horizontalMoveBias = int(y)
#        CCBias = int(y)
        
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

## 9_{48}
## Non-alternating
## Unknotting number = 2
## Original DT code: [4, 10, -14, -12, 16, 2, -6, 18, 8]
#K = ADT.ADT([4, 10, -14, -12, 16, 2, -6, 18, 8], [1, -1, -1, -1, -1, -1, -1, 1, -1])
#K.setInvariant('unknottingNumber', 2)

## 10_{165}
## Non-alternating
## Unknotting number = 2
## Original DT code: [6, 8, 14, 18, 16, 4, -20, 10, 2, -12]
K = ADT.ADT([6, 8, 14, 18, 16, 4, -20, 10, 2, -12], [1, -1, -1, 1, -1, -1, -1, -1, -1, -1])
K.setInvariant('unknottingNumber', 2)


### 12n_{0744}
### Unknotting number = 2
### Original DT code: [6, -10, 14, 16, -22, 20, 18, 24, 2, 12, -4, -8]
#K = ADT.ADT([10,12,22,-14,-18,16,-20,24,2,-8,6,4],[-1,1,1,1,1,1,1,1,-1,1,1,1])
#K.setInvariant('unknottingNumber', 2)

fit = Fit.Fit(2, 1, 1, 2, K)
## So far the BEST parameters have been fit = Fit.Fit(2, 1, 1, 2, K)    

success, j, numiterations, pop, best_opList, min_ol, d = applyUnknottingAlgorithm(fit = fit, K = K, numiterations = 2000, up = 1, hor = 1, down = 5, cc = 10, opChange=1, opPerm=1, opRevPerm=1, opDel=1, opIns=6)