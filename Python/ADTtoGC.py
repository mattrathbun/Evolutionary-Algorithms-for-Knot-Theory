import ADT
import ADTOp
import sys

def ADTtoGC(adt):
    label = 1
    cache = {}
    GCLabels = []
    GCOrientations = []
    n = adt.number_crossings()
    for i in range(1, 2*n + 1):
        odd, even, sign, orient = adt.quad(i)
        if (odd, even) in cache:
            GCLabels.append(cache[(odd,even)])
            GCOrientations.append(orient)
        else:
            GCLabels.append(label)
            GCOrientations.append(orient)
            cache[(odd, even)] = label
            label += 1
    return [GCLabels, GCOrientations]