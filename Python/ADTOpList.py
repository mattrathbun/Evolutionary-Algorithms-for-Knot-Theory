import ADTOp
from random import *


opListTypes = ['Move', 'CC']

class ADTOpList(object):

    def __init__(self, opList, minl = 0, maxl = 20, opListType=None):
        self.opList = opList
        self.opListType = opListType
        self.minl = minl
        self.maxl = maxl

    def toList(self):
        return self.opList
        
    def getOpListType(self):
        return self.opListType
        
    def setOpListType(self, opListType):
        self.opListType = opListType
        
    def checkOpListType(self):
        if self.opListType:
            for op in self.opList:
                if op.opType != self.opListType:
                    raise TypeError("Supposed to be a list of type {}, but {} has type {}.".format(self.opListType, op.toString(), op.opType))
        else:
            return True

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
        return ADTOpList(ol, self.opListType)


    def length(self):
        return len(self.opList)
        
    def toString(self):
        l = []
        for op in self.opList:
            l.append(op.toString())
        return l

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
        return d, ADTOpList(nl, self.opListType)

    def append(self, list_of_ops):
        curr = self.opList
        self.opList = curr + list_of_ops

    def prepend(self, list_of_ops):
        curr = self.opList
        self.opList = list_of_ops + curr

    def mutate(self, model='original'):
        n = self.length()
        ol = self.toList()
        if model=='original':
            mutationType = randint(0, 4)
            if mutationType == 0:  # Randomly change one of the operations
                if self.opListType == 'Move':
                    ol[randint(0, n-1)] = ADTOp.coarseRandomMove()
                elif self.opListType == 'CC':
                    ol[randint(0, n-1)] = ADTOp.coarseRandomCC()
                else:
                    ol[randint(0, n - 1)] = ADTOp.coarseRandomOp()
            elif mutationType == 1:  # Cyclic permutation
                ol.append(ol[0])
                del ol[0]
            elif mutationType == 2:  # Cyclic permutation the other direction
                ol.insert(0, ol[-1])
                del ol[-1]
            elif mutationType == 3:  # Delete a random operation from the list
                del ol[randint(0, n - 1)]
            elif mutationType == 4:  # Insert a random operation
                if self.opListType == 'Move':
                    ol.insert(randint(0, n-1), ADTOp.coarseRandomMove())
                elif self.opListType == 'CC':
                    ol.insert(randint(0, n-1), ADTOp.coarseRandomCC())
                else:
                    ol.insert(randint(0, n - 1), ADTOp.coarseRandomOp())
            self.opList = ol
        if model=='randtail':
            print "Mutating with the new model."
            m = randint(0, n-1)
            k = randint(0, self.maxl) 
            for i in range(m, m+k):
                if self.opListType == 'Move':
                    new = ADTOp.coarseRandomMove()
                elif self.opListType == 'CC':
                    new = ADTOp.coarseRandomCC()
                else:
                    new = ADTOp.coarseRandomOp()
                try:
                    ol[i] = new
                except:
                    ol.append(new)
            self.opList = ol
        if model=='modtail':
            print "Mutating with the newest model."
            m = randint(0, n-1)
            k = randint(0, self.maxl) 
            for i in range(m, m+k):
                try:
                    if ol[i].opType == "Move":
                        num = ol[i].number
                        dir = ol[i].direction
                        ol[i] = ADTOp.ADTMove(num, dir)
                    elif ol[i].opType == "CC":
                        ol[i] = ADTOp.ADTCC()
                    else:
                        ol[i] = ADTOp.coarseRandomOp()
                except:
                    if self.opListType == 'Move':
                        new = ADTOp.coarseRandomMove()
                    elif self.opListType == 'CC':
                        new = ADTOp.coarseRandomCC()
                    else:
                        new = ADTOp.coarseRandomOp()
                    ol.append(new)
            self.opList = ol

    def recombine(self, other, model='original'):
        if model=='original':
            pos = randint(1, min(self.length(), other.length()) - 1)
            self_first_word = self.toList()[0:pos] + other.toList()[pos:]
            other_first_word = other.toList()[0:pos] + self.toList()[pos:]
            return (ADTOpList(self_first_word, self.opListType), ADTOpList(other_first_word, self.opListType))
        if model == 'randtail':
            return (self, other)

    def downCount(self):
        dc = 0
        for op in self.toList():
            if op.opType == 'Move':
                if op.getDirection() == "D":
                    dc += 1
        return dc

    def upCount(self):
        uc = 0
        for op in self.toList():
            if op.opType == 'Move':
                if op.getDirection() == "U":
                    uc += 1
        return uc
        
    def horizontalCount(self):
        hc = 0
        for op in self.toList():
            if op.opType == "Move":
                if op.getDirection() == "H":
                    hc += 1
        return hc
        
    def ccCount(self):
        cc = 0
        for op in self.toList():
            if op.opType == 'CC':
                cc += 1
        return cc


def randomOpList(maxl, minl, upBias=1, horizontalBias=1, downBias=1, CCBias=1):
    length = randint(minl, maxl)
    ops = []
    for i in range(0, length):
        ops.append(ADTOp.coarseRandomOp(upBias, horizontalBias, downBias, CCBias))
    return ADTOpList(ops)
    
def randomMoveList(maxl, minl, upBias = 1, horizontalBias = 1, downBias = 1):
    moves = randomOpList(maxl, minl, upBias=upBias, horizontalBias=horizontalBias, downBias=downBias, CCBias=0)
    moves.setOpListType('Move')
    return moves
    
def randomCCList(maxl, minl):
    cc = randomOpList(maxl, minl, upBias=0, horizontalBias=0, downBias=0)
    cc.setOpListType('CC')
    return cc
    
