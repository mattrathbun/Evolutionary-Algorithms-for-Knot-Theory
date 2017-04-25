import os, sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpPopulation, ADTOpPopulationSets, Fit
import fronds
import AllDiagrams
from datetime import datetime
import random, itertools, math

storageFile = "EasyDiagrams"

AllDiagrams.init()

length = 10



explored = []
K = ADT.ADT([], [])
exploring = [K]

start = datetime.now()

while len(exploring) > 0:
    print "The explored list has size: {} \n".format(len(explored))
    for i in range(len(exploring)):
        D = exploring[i]
        moves = D.simpleFinePossibleMoves()
        for m in moves:
            copy = D.copy()
            E = m.apply(copy)
            if (E != False) and (E not in explored) and (E not in exploring) and (E.number_crossings() <= length):
                exploring.insert(0,E)
                print "    The exploring list has size: {} \n".format(len(exploring))
    exploring.remove(D)
    myfile = open(storageFile, 'a')
    myfile.write(str(D.to_string()))
    myfile.write('\n')
    myfile.close()
    explored.append(D)

print "There are {} diagrams that we have explored.".format(len(explored))
for D in explored:
    print D.to_string()
    print "\n"
    
end = datetime.now()

print "Total time was {}.".format(end - start)
 
                
                