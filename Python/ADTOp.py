from math import *
import random

class ADTOp(object):
	def __init__(self, number, direction='H', position, side=None,
		crossing_sign=None, target_position=None):
		self.number = number	# 1, 2, or 3 -- Reidemeister moves
			# Necessary property for all Op objects
		self.direction = direction	# U, D, or H -- Up, Down, or Horizontal
			# Necessary property for all Op objects
		self.position = position	# Indicating at which strand the move will be performed
			# Necessary property for all Op objects
		self.side = side	# L or R -- which side of the strand on which a move is meant to be performed
			# Necessary only for R1Up and R2Up Ops
		self.crossing_sign = crossing_sign	# 1 or -1 -- Indicating which types of crossings will be introduced
			# Necessary only for R1Up and R2Up Ops
		self.target_position = target_position	# a pair of numbers -- indicating which second strand will be involved in an R2U move
			# Necessary only for R2Up Ops
			
		## Takes a string from the list opNames
		
	def __eq__(self,other):
		if type(other) == type(self):
			return self.__dict__ == other.__dict__
		else:
			return False
						
	def __ne__(self,other):
		return not self.__eq__(other)
			
	def getNumber(self):
		return self.number
	
	def getDirection(self):
		return self.direction
	
	def getType(self):
		return self.number, self.direction
		
	def getTypeString(self):
		return str(self.number)+str(self.direction)
	
	def toString(self):
		if self.number == 1 and self.direction == 'U':
			return "1U(pos={}, {}, sign={}".format(str(self.position), str(self.side), str(self.crossing_sign))
		elif self.number == 1 and self.direction == "D":
			return "1D({})".format(str(self.position))
		elif self.number == 2 and self.direction == "U":
			return "2U(pos={}, {}, target={})".format(str(self.position), str(self.side), str.(self.target_position))
		elif self.number == 2 and self.direction == "D":
			return "2D({})".format(str(self.position))
		elif self.number == 3:
			return "3H({})".format(str(self.position))
						
	def copy(self):
		return ADTOp(self.number, self.direction, self.position, self.side, self.crossing_sign, self.target_position)
		
	def apply(self, knot):
		if self.number == 1 and self.direction == "U":
			return knot.R1Up(self.position, self.side, self.crossing_sign)
		elif self.number == 1 and self.direction == "D":
			return knot.R1Down(self.position)
		elif self.number == 2 and self.direction == "U":
			return knot.R2Up(self.position, self.side, self.target_position) ###########################################################
		elif self.number == 2 and self.direction == "D":
			return knot.R2Down(self.position) ###########################################################
		elif self.number == 3:
			return knot.R3(self.position) ###########################################################
		
	def isUp(self):
		return self.direction == "U"
		
	def isDown(self):
		return self.direction == "D"
		
	def isHorizontal(self):
		return self.direction == "H"


#R2_up_moves = ['R2UpPlus', 'R2UpMinus']
#up_moves = ['R2UpPlus', 'R2UpMinus', 'M2UpPlus', 'M2UpMinus']
#horizontal_moves = ['R3', 'M1Forward', 'M1Backward', 'S']
#down_moves = ['R2Down', 'M2Down']

#opNames = ['R2UpPlus', 'R2UpMinus', 'M2UpPlus', 'M2UpMinus', 'R3', 'M1Forward',
#	'M1Backward', 'S', 'R2Down', 'M2Down']

def randomOp(upBias=1, horizontalBias=1, downBias=1):
	randOp = random.choice(upBias*up_moves+downBias*down_moves+horizontalBias*horizontal_moves)
	## We introduce here the possibility for bias. The 3 optional parameters default to 1,
	## but can be attuned to multiply the likelihood of choosing an element from the
	## corresponding list by exactly this factor.	
	if randOp in R2_up_moves:
#		strand_index = 'undetermined'
		return R2UpBraidOp(randOp, 'undetermined')
	else:
#		strand_index = None
#	return BraidOp(randOp, strand_index)
		return BraidOp(randOp)
		
class BraidOp(object):
	def __init__(self, op):
		self.op = op
		## Takes a string from the list opNames
		
	def __eq__(self,other):
		if type(other) == type(self):
			return self.__dict__ == other.__dict__
		else:
			return False
						
	def __ne__(self,other):
		return not self.__eq__(other)
			
	def toString(self):
		return self.op
			
	def copy(self):
		return BraidOp(self.op)
		
	def apply(self, braid):
		effect = 0
		old_braid = braid.copy()
		getattr(braid, self.op)()
		if braid != old_braid:
			effect = 1
		return effect
		
	def isUp(self):
		return self.op in up_moves
		
	def isDown(self):
		return self.op in down_moves
		
	def isHorizontal(self):
		return self.op in horizontal_moves
	
		
class R2UpBraidOp(BraidOp):
	def __init__(self, op, strand_index):
		BraidOp.__init__(self, op)
		self.strand_index = strand_index
				
	def copy(self):
		return R2UpBraidOp(self.op, self.strand_index)
		
	def apply(self, braid):
		if self.strand_index == 'undetermined':
			self.strand_index = random.randint(1, braid.braid_index() - 1)
#		getattr(braid, self.op)(self.strand_index)
		effect = 0
		old_braid = braid.copy()
		getattr(braid, self.op)(self.strand_index)
		if braid != old_braid:
			effect = 1
		return effect
			
	def isR2Up(self):
		return True	
	
		
	

		
