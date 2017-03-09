import os, sys, string
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
import ADT

storageFile = "SimpleHardDiagramCandidates"
fileToClean = "SimpleHardDiagrams"

stored = set()

with open(fileToClean) as f:
    for line in f:
        s = string.replace(line, "\n", "")
        s = string.replace(s, "(", "")
        s = string.replace(s, ")", "")              
        t = s.split("', '")
        t = [string.replace(i, "'", "") for i in t]
        code, orientations = [[int(i) for i in j.split(",")] for j in t]
        K = ADT.ADT(code, orientations)
        K.standardize()
        if K.to_tuple() not in stored:
            stored.add(K.to_tuple())
            new_file = open(storageFile, 'a')
            new_file.write(K.to_string()[0])
            new_file.write("; ")
            new_file.write(K.to_string()[1])
            new_file.write('\n')
            new_file.close()
        else:
            pass