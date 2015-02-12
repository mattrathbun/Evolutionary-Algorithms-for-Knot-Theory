import ADTOp
from random import *


class ADTOpList(object):

    def __init__(self, opList):
        self.opList = opList

    def toList(self):
        return self.opList

    def __eq__(self, other):
        if type(other) == type(self):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def copy(self):
        ol = []
        for i in self.opList:
            ol.append(i)
        return ADTOpList(ol)

    def length(self):
        return len(self.opList)

    def apply(self, diagram):
        d = diagram.copy()
        nl = []
        for op in self.opList:
            try:
                op
            except NameError:
                pass
            else:
                eff = op.apply(d)
                if eff == 1:
                    nl.append(op)
        return d, ADTOpList(nl)

    def append(self, list_of_ops):
        curr = self.opList
        self.opList = curr + list_of_ops

    def prepend(self, list_of_ops):
        curr = self.opList
        self.opList = list_of_ops + curr

    def mutate(self, restriction=None):
        n = self.length()
        type = randint(0, 4)
        ol = self.toList()
        if type == 0:  # Randomly change one of the operations
            if restriction == 'Move':
                ol[randint(0, n-1)] = ADTOp.coarseRandomMove()
            elif restriction == 'CC':
                ol[randint(0, n-1)] = ADTOp.coarseRandomCC()
            else:
                ol[randint(0, n - 1)] = ADTOp.coarseRandomOp()
        elif type == 1:  # Cyclic permutation
            ol.append(ol[0])
            del ol[0]
        elif type == 2:  # Cyclic permutation the other direction
            ol.insert(0, ol[-1])
            del ol[-1]
        elif type == 3:  # Delete a random operation from the list
            del ol[randint(0, n - 1)]
        elif type == 4:  # Insert a random operation
            ol.insert(randint(0, n - 1), ADTOp.coarseRandomOp())
        self.opList = ol

    def recombine(self, other):
        pos = randint(1, min(self.length(), other.length()) - 1)
        self_first_word = self.toList()[0:pos] + other.toList()[pos:]
        other_first_word = other.toList()[0:pos] + self.toList()[pos:]
        return (ADTOpList(self_first_word), ADTOpList(other_first_word))

    def downCount(self):
        dc = 0
        for op in self.toList():
            if op.type == 'Move':
                if op.getDirection() == "D":
                    dc += 1
        return dc

    def upCount(self):
        uc = 0
        for op in self.toList():
            if op.type == 'Move':
                if op.getDirection() == "U":
                    uc += 1
        return uc
        
    def ccCount(self):
        cc = 0
        for op in self.toList():
            if op.type = 'CC':
                cc += 1
        return cc


def randomOpList(maxl, minl, upBias=1, horizontalBias=1, downBias=1, CCBias=1):
    length = randint(minl, maxl)
    ops = []
    for i in range(0, length):
        ops.append(ADTOp.coarseRandomOp(upBias, horizontalBias, downBias, CCBias))
    return ADTOpList(ops)
