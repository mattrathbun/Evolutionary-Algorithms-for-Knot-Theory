import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT

K = ADT.ADT([4,8,12,2,14,6,10], [1, 1, 1, 1, -1, 1, -1])
Kname = "7_6"

print "%s                  : %s\n" % (Kname, K.to_string())

for i in range(1,15):
    for sign in [1,-1]:
        for side in ['L','R']:
            L = K.copy()
            L.R1Up(i,side,sign)
            print "%s with R1Up(%d,%s,%s) : %s" % \
                    (Kname, \
                     i, \
                     side, \
                     ('+' if sign == 1 else '-'), \
                     L.to_string())
            for j in L.possibleR1Down():
                LL = L.copy()
                arc = j['arc']
                LL.R1Down(arc)
                print "    R1Down(%d) gives  : %s" % \
                        (arc, \
                         (Kname if LL == K else "NOT %s" % (Kname)))
            print ""
    print ""

print "####################### Problem starts here!!! ###########################"

def testR1DownProblem(diagram, arc):
	print "Here's the diagram before the R1Down move: ", diagram.to_string()
	print "Here's an attempt at an R1 Down move at strand {}".format(arc)
	diagram.R1Down(arc)
	print diagram.to_string()
	if not diagram.isrealisable():
		raise TypeError("R1Down move is not producing a valid diagram!")

L = ADT.ADT([22, 4, 20, -10, 12, -8, 6, 18, -2, -14, -16], [-1, 1, -1, 1, -1, 1, -1, -1, 1, 1, 1])
testR1DownProblem(L, 22)
## Should be: ...
## Produces: [4, 20, -10, 12, -8, 6, 18, -2, -14, -16], [1, -1, 1, -1, 1, -1, -1, 1, 1, 1]
	

K = ADT.ADT([12, -8, 10, 2, 4, -6], [-1, -1, 1, 1, 1, -1])
testR1DownProblem(K, 12)
K.R1Down(12)
## Should be: [
## Produces: [-8, 10, 2, 4, -6], [-1, 1, 1, 1, -1]

K = ADT.ADT([8, -4, 6, -2], [1, -1, -1, 1])
testR1DownProblem(K, 8)
## Should be: ....
## Produces:  [-4, 6, -2], [-1, -1, 1]	
