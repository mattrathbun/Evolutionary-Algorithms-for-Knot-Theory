import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import ADT

K = ADT.ADT([4,8,12,2,14,6,10], [1, 1, 1, 1, -1, 1, -1])
Kname = "7_6"

print "%s                         : %s\n" % (Kname, K.to_string())

for i in range(1,15):
    L = K.copy()
    L.crossing_change(i)
    print "%s with crossing change %d : %s" % (Kname, i, L.to_string())
