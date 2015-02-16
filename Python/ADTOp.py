from math import *
import random

moves = ['R1Up', 'R1Down', 'R2Up', 'R2Down', 'R3']
coarse_up_moves = ['R1Up', 'R2Up']
coarse_down_moves = ['R1Down', 'R2Down']
coarse_horizontal_moves = ['R3']
changes = ['CC']
ops = moves + changes


## 'Ops' are any operation that modifies an ADT object.

class ADTOp(object):
    def __init__(self, opType):
        self.opType = opType
        
    def __eq__(self, other):
        if type(other) == type(self):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def getOpType(self):
        return self.opType

    def getOpTypeString(self):
        return str(self.opType)

    def copy(self):
        return ADTOp(self.opType)
        
    def toString(self):
        return str(self.opType)


def coarseRandomOp(upMoveBias=1, horizontalMoveBias=1, downMoveBias=1, CCBias=1):
    randOp = random.choice(upMoveBias * coarse_up_moves + downMoveBias *
                           coarse_down_moves + horizontalMoveBias * coarse_horizontal_moves
                           + CCBias * changes)
    if randOp == 'R1Up':
        return ADTMove(number=1, direction='U', data=None)
    elif randOp == 'R1Down':
        return ADTMove(number=1, direction='D', data=None)
    elif randOp == 'R2Up':
        return ADTMove(number=2, direction='U', data=None)
    elif randOp == 'R2Down':
        return ADTMove(number=2, direction='D', data=None)
    elif randOp == 'R3':
        return ADTMove(number=3, direction='H', data=None)
    elif randOp == 'CC':
        return ADTCC()
    else:
        raise TypeError('Unknown kind of Op.')


def fineRandomOp(diagram):
    possible_ops = diagram.finePossibleOps()
    op = random.choice(possible_ops)
    return op



## 'Moves' specifically refer to Reidemeister moves operating on ADT objects

class ADTMove(ADTOp):

    def __init__(self, number, direction, data=None):
        self.opType = 'Move'
        self.number = number
        self.direction = direction
        self.data = data # data is meant to be a dictionary

    def __eq__(self, other):
        if type(other) == type(self):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def getNumber(self):
        return self.number

    def getDirection(self):
        return self.direction

    def getData(self):
        return self.data

    def getMove(self):
        return self.number, self.direction

    def getFullMove(self):
        return self.number, self.direction, self.data

    def getMoveString(self):
        return str(self.number) + str(self.direction)

    def toString(self):
        if self.number == 1 and self.direction == 'U':
            if self.checkFullData():
                return "1U(pos={}, side={}, sign={})".format(str(self.data['arc']), str(self.data['side']), str(self.data['sign']))
            else:
                return "1U"
        elif self.number == 1 and self.direction == "D":
            if self.checkFullData():
                return "1D(pos={})".format(str(self.data['arc']))
            else:
                return "1D"
        elif self.number == 2 and self.direction == "U":
            if self.checkFullData():
                return "2U(pos={}, side={}, target={})".format(str(self.data['arc']), str(self.data['side']), str(self.data['target']))
            else:
                return "2U"
        elif self.number == 2 and self.direction == "D":
            if self.checkFullData():
                return "2D(pos={})".format(str(self.data['arc']))
            else:
                return "2D"
        elif self.number == 3:
            if self.checkFullData():
                return "3H(pos={}, side={})".format(str(self.data['arc']), str(self.data['side']))
            else:
                return "3H"
        else:
            print "This is strange."
            return self.number, self.direction

    def copy(self):
        return ADTMove(number=self.number, direction=self.direction, data=self.data)

    def checkFullData(self):
        if not self.data:
            return False
        if self.number == 1:
            if self.direction == 'U':
                if len(self.data) == 3 and all(k in self.data for k in ('arc', 'side', 'sign')):
                    return True
                else:
                    return False
            elif self.direction == 'D':
                if len(self.data) == 1 and 'arc' in self.data:
                    return True
                else:
                    return False
            else:
                return False
        elif self.number == 2:
            if self.direction == 'U':
                if len(self.data) == 3 and all(k in self.data for k in ('arc', 'side', 'target')):
                    return True
                else:
                    return False
            elif self.direction == 'D':
                if len(self.data) == 1 and 'arc' in self.data:
                    return True
                else:
                    return False
            else:
                return False
        elif self.number == 3:
            if self.direction == 'H':
                if len(self.data) == 2 and all(k in self.data for k in ('arc', 'side')):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def finePossibleMovesRequest(self, diagram):
        return diagram.finePossibleMoves()

    def coarsePossibleDataRequest(self, diagram):
        if self.number == 1 and self.direction == 'U':
            return diagram.possibleR1Up()
        elif self.number == 1 and self.direction == 'D':
            return diagram.possibleR1Down()
        elif self.number == 2 and self.direction == 'U':
            return diagram.possibleR2Up()
        elif self.number == 2 and self.direction == 'D':
            return diagram.possibleR2Down()
        elif self.number == 3 and self.direction == 'H':
            return diagram.possibleR3()
        else:
            raise TypeError('Unknown kind of Move.')

    def fillData(self, data):
        if not self.checkFullData():
            self.data = data

    def randomData(self, knot):
        if not self.checkFullData():
            possible_data = self.coarsePossibleDataRequest(knot)
            if possible_data == []:
                pass
            else:
                self.fillData(random.choice(possible_data))

    def apply(self, knot):
    	K = knot.copy()
        if not self.checkFullData():
            self.randomData(knot)
            if not self.checkFullData():
                return False
#         print "Trying to apply move: ", self.toString()
#         print "to diagram: ", knot.to_string()
        if self.number == 1 and self.direction == "U":
            knot.R1Up(arc=self.data['arc'], side=self.data['side'], sign=self.data['sign'])
        elif self.number == 1 and self.direction == "D":
            knot.R1Down(arc=self.data['arc'])
        elif self.number == 2 and self.direction == "U":
            knot.R2Up(arc=self.data['arc'], side=self.data['side'], target=self.data['target'])
        elif self.number == 2 and self.direction == "D":
            knot.R2Down(arc=self.data['arc'])
        elif self.number == 3:
            if knot.R3(arc=self.data['arc'], side=self.data['side'])==False:
#                 print "This is where the False is coming from (0)"
                return False
        else:
            raise TypeError(
                'What kind of move are you, and how did you get this far?')

        if knot.isrealisable():
            if knot != K:
                return knot
            else:
                return False
        else:
            print "We have a problem."
            print "Starting with: ", K.to_string()
            print "Applying move: ", self.toString()
            print "Became: ", knot.to_string()
            raise TypeError("We have a problem!!!")
            

#     def apply(self, knot):
#         if not self.checkFullData():
#             self.randomData(knot)
#             if not self.checkFullData():
#                 return False
#         if self.number == 1 and self.direction == "U":
#             return knot.R1Up(arc=self.data['arc'], side=self.data['side'], sign=self.data['sign'])
#         elif self.number == 1 and self.direction == "D":
#             return knot.R1Down(arc=self.data['arc'])
#         elif self.number == 2 and self.direction == "U":
#             return knot.R2Up(arc=self.data['arc'], side=self.data['side'], target=self.data['target'])
#         elif self.number == 2 and self.direction == "D":
#             return knot.R2Down(arc=self.data['arc'])
#         elif self.number == 3:
#             return knot.R3(arc=self.data['arc'], side=self.data['side'])
#         else:
#             raise TypeError(
#                 'What kind of move are you, and how did you get this far?')



def coarseRandomMove(upBias=1, horizontalBias=1, downBias=1):
    randOp = random.choice(upBias * coarse_up_moves + downBias *
                           coarse_down_moves + horizontalBias * coarse_horizontal_moves)
    # We introduce here the possibility for bias. The 3 optional
    # parameters default to 1, but can be attuned to multiply the
    # likelihood of choosing an element from the corresponding list by
    # exactly this factor.
    if randOp == 'R1Up':
        return ADTMove(number=1, direction='U', data=None)
    elif randOp == 'R1Down':
        return ADTMove(number=1, direction='D', data=None)
    elif randOp == 'R2Up':
        return ADTMove(number=2, direction='U', data=None)
    elif randOp == 'R2Down':
        return ADTMove(number=2, direction='D', data=None)
    elif randOp == 'R3':
        return ADTMove(number=3, direction='H', data=None)
    else:
        raise TypeError('Unknown kind of Move.')


def fineRandomMove(diagram):
    possible_moves = diagram.finePossibleMoves()
    move = random.choice(possible_moves)
    return move
    

## 'CC's refer to crossing changes performed on ADT objects.
    
class ADTCC(ADTOp):

    def __init__(self, data=None):
        self.opType = 'CC'
        self.data = data

    def __eq__(self, other):
        if type(other) == type(self):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def getOpType(self):
        return self.opType

    def getData(self):
        return self.data
        
    def toString(self):
        if self.opType == "CC":
            if self.checkFullData():
                return "CC(@{})".format(str(self.data['arc']))
            else:
                return "CC"
        else:
            print "I don't know how to print that opType yet."

    def copy(self):
        return ADTCC(opType=self.opType, data=self.data)

    def checkFullData(self):
        if self.opType == "CC":
            if self.data:
                return True
            else:
                return False
        else:
            return False
            
    def possibleCCRequest(self, diagram):
        return diagram.finePossibleCC()

    def fillData(self, data):
        if not self.checkFullData():
            self.data = data

    def randomData(self, knot):
        if not self.checkFullData():
            possible_data = self.possibleCCRequest(knot)
            if possible_data == []:
                pass
            else:
                self.fillData(random.choice(possible_data))

    def apply(self, knot):
        K = knot.copy()
        if not self.checkFullData():
            self.randomData(knot)
            if not self.checkFullData():
                return False
#         print "Trying to apply change: ", self.toString()
#         print "to diagram: ", knot.to_string()
        if self.opType == "CC":
            knot.crossing_change(arc=self.data['arc'])
        else:
            raise TypeError(
                'What kind of change are you, and how did you get this far?')

        if knot.isrealisable():
            if knot != K:
                return knot
            else:
                return False
        else:
            print "We have a problem."
            print "Starting with: ", K.to_string()
            print "Applying move: ", self.toString()
            print "Became: ", knot.to_string()
            raise TypeError("We have a problem!!!")


def coarseRandomCC():
    return ADTCC()


def fineRandomCC(diagram):
    n = diagram.number_crossings()
    arc = random.randint(1, n)
    return ADTCC({'arc':arc})

