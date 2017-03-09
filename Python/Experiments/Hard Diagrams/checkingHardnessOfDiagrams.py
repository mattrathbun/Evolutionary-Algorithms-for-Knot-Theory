import os, sys, string, fronds
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
import ADT


nonRootedFronds = []

with open("SimpleHardDiagramCandidates") as f:
    for line in f:
        s = string.strip(line, "\n")
        t = line.split(";")
        code, orientations = [[int(j) for j in i.split(",")] for i in t]
        K = ADT.ADT(code, orientations)
        out = fronds.frond(K, 0) 
        if out != None:
            if out[1] != "Trivial":
                nonRootedFronds.append(K)

print "We found {} unrooted fronds.".format(len(nonRootedFronds))
for k in nonRootedFronds:
    print k.to_string()
    print "\n"
            