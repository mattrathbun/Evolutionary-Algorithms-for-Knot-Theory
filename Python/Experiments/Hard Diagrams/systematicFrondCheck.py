import os, sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpPopulation, ADTOpPopulationSets, Fit
import fronds
import AllDiagrams
from datetime import datetime
import random, itertools, math

AllDiagrams.init()

length = 10

code_entries = [2*(i+1) for i in range(length)] 

#all_codes = itertools.permutations(code_entries)
#all_orientations = itertools.combinations_with_replacement([1,-1], length)

explored = set()
candidates = []

for i, c in enumerate(itertools.permutations(code_entries)):
    print "code {}/{} \n".format(i+1, math.factorial(length))
    K = ADT.ADT(list(c), length*[1])
    if K.isrealisable():    
        for j, o in enumerate(itertools.combinations_with_replacement([1,-1], length)):
            print "orientation {}/{} \n".format(j+1, 2**length)
            K = ADT.ADT(list(c), list(o))
            K.standardize()
            if K.to_tuple() not in explored:
                explored.add(K.to_tuple())
                ## Check whether K is the trivial knot or otherwise (as best as possible with polynomials)
                a, b = fronds.frond(K)
                if b != "Trivial":
                    candidates.append(K.to_string())
                    
print "We found {} diagram that should be hard unknot diagrams.\n".format(len(candidates))
print candidates
                
                
                
                
        
        

