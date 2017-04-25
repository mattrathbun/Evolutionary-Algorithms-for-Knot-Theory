import os, sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpPopulation, ADTOpPopulationSets, Fit
import fronds
import AllDiagrams
from datetime import datetime
import random, itertools, math

AllDiagrams.init()

storageFile = "AlsoNonEasyDiagrams"

length = 10

code_entries = [2*(i+1) for i in range(length)] 
base_pm_one = list(itertools.combinations_with_replacement([1,-1], length))

#all_codes = itertools.permutations(code_entries)
#all_orientations = itertools.combinations_with_replacement([1,-1], length)

explored = set()
candidates = []

for i, c in enumerate(itertools.permutations(code_entries)):
    print "code {}/{} \n".format(i+1, math.factorial(length))
    for s in base_pm_one:
        code = [a*b for a,b in zip(list(c), list(s))]
        K = ADT.ADT(code, length*[1])
    if K.isrealisable():    
        for j, o in enumerate(itertools.combinations_with_replacement([1,-1], length)):
            print "orientation {}/{} \n".format(j+1, 2**length)
            K = ADT.ADT(code, list(o))
            K.standardize()
            if K.to_tuple() not in explored:
                explored.add(K.to_tuple())
                ## Check whether K is the trivial knot or otherwise (as best as possible with polynomials)
                a, b = fronds.frond(K)
                if b != "Trivial" and b!= None:
                    myfile = open(storageFile, 'a')
                    myfile.write(str(K.to_string()))
                    myfile.write('\n')
                    myfile.close()
                    candidates.append(K.to_string())
                    
                    
print "We found {} diagram that should be hard unknot diagrams.\n".format(len(candidates))
print candidates
                
                
                