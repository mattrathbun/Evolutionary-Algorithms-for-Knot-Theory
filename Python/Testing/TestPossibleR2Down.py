import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ADT, ADTOp

L = ADT.ADT([-12, 14, -16, -22, -20, -6, 2, -4, -18, -10, 8], [-1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1])

print L.possibleR2Down()
# Should be arcs: 1, 3, 7, 8, 12, 14, 20, 21
