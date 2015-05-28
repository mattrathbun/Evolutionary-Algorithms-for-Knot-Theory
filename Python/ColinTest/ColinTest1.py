import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpList

K = ADT.ADT([4,6,5],[1,1,1])
Kname = "trefoil"
# K = ADT.ADT([4,8,12,2,14,6,10], [1, 1, 1, 1, -1, 1, -1])
# Kname = "7_6"

print "%s : %s\n" % (Kname, K.to_string())

n = 10
moves = ADTOpList.randomMoveList(n, n, upBias=5, downBias=5).toList()
print "We have a list of moves."
for i in moves:
    print i.toString()
print "***** applying moves"
for i in moves:
    L = K.copy()
    if i.apply(L):
        print "successful application of move"
        print K.to_string()
        K = L
    else:
        print "unsuccessful application of move"
