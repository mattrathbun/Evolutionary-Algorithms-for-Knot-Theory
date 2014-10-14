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
