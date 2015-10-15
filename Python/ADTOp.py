from math import *
import random, re
import AllDiagrams

moves = ['R1Up', 'R1Down', 'R2Up', 'R2Down', 'R3', 'Shift']
coarse_up_moves = ['R1Up', 'R2Up']
coarse_down_moves = ['R1Down', 'R2Down']
coarse_horizontal_moves = ['R3', 'Shift']
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

def simpleCoarseRandomOp(upMoveBias=1, horizontalMoveBias=1, downMoveBias=1, CCBias=1):
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
    elif randOp == 'Shift':
        return ADTMove(number=0, direction='H', data={})
    elif randOp == 'CC':
        return ADTCC()
    else:
        raise TypeError('Unknown kind of Op.')

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
        raise TypeError("HOW IS THIS HAPPENING??")
        return ADTCC()
    else:
        raise TypeError('Unknown kind of Op.')

def simpleFineRandomOp(diagram):
    possible_ops = diagram.simpleFinePossibleOps()
    op = random.choice(possible_ops)

def fineRandomOp(diagram):
    possible_ops = diagram.finePossibleOps()
    op = random.choice(possible_ops)
    return op



## 'Moves' specifically refer to Reidemeister moves operating on ADT objects or a shift in label.

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
        if self.number == 0 and self.direction == 'H':
            if self.checkFullData():
                return "Shift"
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
        if self.number == 0:
            return True
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

    def simpleFinePossibleMoveRequest(self, diagram):
        return diagram.simpleFinePossibleMoves()

    def finePossibleMovesRequest(self, diagram):
        return diagram.finePossibleMoves()

    def simpleCoarsePossibleDataRequest(self, diagram):
        if self.number == 0 and self.direction == 'H':
            return diagram.simplePossibleShift()
        if self.number == 1 and self.direction == 'U':
            return diagram.simplePossibleR1Up()
        elif self.number == 1 and self.direction == 'D':
            return diagram.simplePossibleR1Down()
        elif self.number == 2 and self.direction == 'U':
            return diagram.simplePossibleR2Up()
        elif self.number == 2 and self.direction == 'D':
            return diagram.simplePossibleR2Down()
        elif self.number == 3 and self.direction == 'H':
            return diagram.simplePossibleR3()
        else:
            raise TypeError('Unknown kind of Move.')

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

    def simpleRandomData(self, knot):
        if not self.checkFullData():
            possible_data = self.simpleCoarsePossibleDataRequest(knot)
            if possible_data == []:
                pass
            else:
                self.fillData(random.choice(possible_data))

    def randomData(self, knot):
        if not self.checkFullData():
            possible_data = self.coarsePossibleDataRequest(knot)
            if possible_data == []:
                pass
            else:
                self.fillData(random.choice(possible_data))

    def apply(self, knot):
        print "ABOUT TO CHECK ALLDIAGRAMS"
        print "Length of allDiagrams: ", len(AllDiagrams.allDiagrams)
        AllDiagrams.lookupCount += 1
        print "lookupCount: ", AllDiagrams.lookupCount
        if (knot.to_string(), self.toString()) in AllDiagrams.allDiagrams:
            print "LOOKUP SUCCESS"
            AllDiagrams.lookupSuccess += 1
            print "{} of {}".format(AllDiagrams.lookupSuccess, AllDiagrams.lookupCount)
            print "Which is: ", float(AllDiagrams.lookupSuccess)/float(AllDiagrams.lookupCount)
            K = AllDiagrams.allDiagrams[(knot.to_string(), self.toString())]
            print "op is "+self.toString()
            print "knot is ",knot.to_string()
            print "K is ",K.to_string()
            if K == knot:
                return False
            else:
                knot = K.copy()
                return knot
        else:
            print "LOOKUP FAILURE"
            AllDiagrams.lookupFailure += 1
            print "{} of {}".format(AllDiagrams.lookupFailure, AllDiagrams.lookupCount)
            print "Which is: ", float(AllDiagrams.lookupFailure)/float(AllDiagrams.lookupCount)
#             print "\n"
#             print knot.to_string(), self.toString()
#             print "\n"
#             print "apparently not in"
#             print "\n"
            for diag in AllDiagrams.allDiagrams:
                print diag, AllDiagrams.allDiagrams[diag].to_string()
            print "\n"
#            K = knot.copy()
            if not self.checkFullData():
                self.simpleRandomData(knot)
                if not self.checkFullData():
                    return False
            K = knot.copy()
            # print "Trying to apply move: ", self.toString(), " ", self.number," ", self.direction
            # print "to diagram: ", knot.to_string()
            if self.number == 0 and self.direction == "H":
                print "Here is knot before shiftLabel() applied to knot: ", knot.to_string()
                print "Here is K before shiftLabel() applied to knot: ", K.to_string()
                print "Here is self before shiftLabel() applied to knot: ", self.toString()
                knot.shiftLabel()
                print "Here is knot after shiftLabel() applied to knot: ", knot.to_string()
                print "Here is K after shiftLabel() applied to knot: ", K.to_string()
                print "Here is self after shiftLabel() applied to knot: ", self.toString()
                
                print "Here is allDiagrams before addition: \n"
                for diag in AllDiagrams.allDiagrams:
                    print "({}, {})".format(diag, AllDiagrams.allDiagrams[diag].to_string())
                print "\n"
                
                AllDiagrams.allDiagrams[(K.to_string(), self.toString())] = knot.copy()
                
                print "Here is allDiagrams after addition: \n"
                for diag in AllDiagrams.allDiagrams:
                    print "({}, {})".format(diag, AllDiagrams.allDiagrams[diag].to_string())
                print "\n"
                
                print "Remember K is {} and knot is {}".format(K.to_string(), knot.to_string())
                print "Now, as a check, we will copy K and then shift the label of K."
                L = K.copy()
                K.shiftLabel()
                print "Now L is {}, K is {}, and knot is {}".format(L.to_string(), K.to_string(), knot.to_string())
                if AllDiagrams.allDiagrams[(L.to_string(), self.toString())] != K:
                    raise TypeError("\n\nPROBLEM!\n\n")
            elif self.number == 1 and self.direction == "U":
                knot.R1Up(arc=self.data['arc'], side=self.data['side'], sign=self.data['sign'])
                AllDiagrams.allDiagrams[(K.to_string(), self.toString())] = knot.copy()
            elif self.number == 1 and self.direction == "D":
                knot.R1Down(arc=self.data['arc'])
                AllDiagrams.allDiagrams[(K.to_string(), self.toString())] = knot.copy()
            elif self.number == 2 and self.direction == "U":
                knot.R2Up(arc=self.data['arc'], side=self.data['side'], target=self.data['target'])
                AllDiagrams.allDiagrams[(K.to_string(), self.toString())] = knot.copy()
            elif self.number == 2 and self.direction == "D":
                knot.R2Down(arc=self.data['arc'])
                AllDiagrams.allDiagrams[(K.to_string(), self.toString())] = knot.copy()
            elif self.number == 3:
                if knot.R3(arc=self.data['arc'], side=self.data['side'])==False:
#                     print "This is where the False is coming from (0)"
                    return False
                AllDiagrams.allDiagrams[(K.to_string(), self.toString())] = knot.copy()
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


def simpleCoarseRandomMove(upBias=1, horizontalBias=1, downBias=1):
    randOp = random.choice(upBias * coarse_up_moves + downBias *
                           coarse_down_moves + horizontalBias * coarse_horizontal_moves)
    # We introduce here the possibility for bias. The 3 optional
    # parameters default to 1, but can be attuned to multiply the
    # likelihood of choosing an element from the corresponding list by
    # exactly this factor.
    if randOp == 'Shift':
        return ADTMove(number=0, direction='H', data={})
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

def simpleFineRandomMove(diagram):
    possible_moves = diagram.simpleFinePossibleMoves()
    move = random.choice(possible_moves)
    return move

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
        return ADTCC(data=self.data)

    def checkFullData(self):
        if self.opType == "CC":
            if self.data:
                return True
            else:
                return False
        else:
            return False
            
    def simplePossibleCCRequest(self, diagram):
        return diagram.simpleFinePossibleCC()
    
    def possibleCCRequest(self, diagram):
        return diagram.finePossibleCC()

    def fillData(self, data):
        if not self.checkFullData():
            self.data = data

    def simpleRandomData(self, knot):
        if not self.checkFullData():
            possible_data = self.simplePossibleCCRequest(knot)
            if possible_data == []:
                pass
            else:
                self.fillData(random.choice(possible_data))

    def randomData(self, knot):
        if not self.checkFullData():
            possible_data = self.possibleCCRequest(knot)
            if possible_data == []:
                pass
            else:
                self.fillData(random.choice(possible_data))

    def apply(self, knot):
        if (knot, self) in AllDiagrams.allDiagrams:
            K = AllDiagrams.allDiagrams[(knot, self)]
            if K == knot:
                return False
            else:
                return True
        else:
            K = knot.copy()
            if not self.checkFullData():
                self.simpleRandomData(knot)
                if not self.checkFullData():
                    return False
#         print "Trying to apply change: ", self.toString()
#         print "to diagram: ", knot.to_string()
            if self.opType == "CC":
                knot.crossing_change(arc=self.data['arc'])
                AllDiagrams.allDiagrams[(K, self)] = K
            else:
                raise TypeError(
                    'What kind of change are you, and how did you get this far?')


##### IS THIS STILL NECESSARY, OR WAS THIS JUST FOR TESTING? ####
#         if knot.isrealisable():
#             if knot != K:
#                 return knot
#             else:
#                 return False
#         else:
#             print "We have a problem."
#             print "Starting with: ", K.to_string()
#             print "Applying move: ", self.toString()
#             print "Became: ", knot.to_string()
#             raise TypeError("We have a problem!!!")
            
############

def simpleCoarseRandomCC():
    return ADTCC()

def coarseRandomCC():
    return ADTCC()

def simpleFineRandomCC(diagram):
    return ADTCC({'arc':1})

def fineRandomCC(diagram):
    n = diagram.number_crossings()
    arc = random.randint(1, n)
    return ADTCC({'arc':arc})
    
    
# Silly helper function to spit out an integer if a string represents an integer.
def if_int(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return s
        
        
# def stringToOp(str):
#     if len(str)==2:
#         if str=='CC':
#             return ADTCC()
#         else:
#             return ADTMove(int(str[0]), str[1])
#     else:
#         if str[0:2] == "CC":
#             opType = "CC"
#             arc = if_int(re.findall('@(\S+)\)', str)[0])
#             data = {'arc':arc}
#             return ADTCC(data)
#         else:
#             opType = "Move"
#             num = int(str[0])
#             dir = str[1]
#             data = {}
#             raw_data = re.findall('([a-z]+?=[^\[]+?)', str)
#             raw_data.extend(re.findall('(\S+?=\[.+?\])', str))
#             for datum in raw_data:
#                 data[re.findall('(^\S+?)=', datum)[0]] = if_int(re.findall('=(.*)$', datum)[0])
#             return ADTMove(num, dir, data)
            
            
