#import os, sys
#lib_path = os.path.abspath('../')
#sys.path.append(lib_path)
import ADT, ADTOp, ADTOpList

K = ADT.ADT([4,8,12,2,14,6,10], [1, 1, 1, 1, -1, 1, -1])
Kname = "7_6"

print "%s : %s\n" % (Kname, K.to_string())

while true:
    move = ADTOp.simpleCoarseRandomOp();
    if (move.apply(k)

###############
############### still being worked on
###############

        
n = 1
moves = ADTOpList.randomMoveList(n, n).toList()
print "We have a list of moves."
for i in moves:
    print i.toString()
print "***** applying moves"
for i in moves:
    print " ** applying move "
    L = K.copy()
    if i.apply(L):
        print "  successful application of move"
        K = L
        print " ",K.to_string()
    else:
        print "  unsuccessful application of move"
