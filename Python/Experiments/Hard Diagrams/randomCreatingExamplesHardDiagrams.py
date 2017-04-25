import os, sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpPopulation, ADTOpPopulationSets, Fit
import fronds
import AllDiagrams
from datetime import datetime
import random, itertools, math

AllDiagrams.init()

storageFile = "NonEasyDiagrams"

length = 10
number_attempts = 100000


base_code_entries = [2*(i+1) for i in range(length)] 
all_base_codes = list(itertools.permutations(base_code_entries))
base_pm_one = list(itertools.combinations_with_replacement([1,-1], length))

for i in range(number_attempts):
    uncrossed_code = list(random.choice(all_base_codes))
    crossings = list(random.choice(base_pm_one))
    code = [a*b for a,b in zip(uncrossed_code, crossings)]
    orientation = list(random.choice(base_pm_one))
    
    print "code {}/{} \n".format(i+1, number_attempts)
    K = ADT.ADT(code, orientation)
    if K.isrealisable():    
        a, b = fronds.frond(K)
        if b != "Trivial" and b != None:
            myfile = open(storageFile, 'a')
            myfile.write(str(K.to_string()))
            myfile.write('\n')
            myfile.close()
                    
                