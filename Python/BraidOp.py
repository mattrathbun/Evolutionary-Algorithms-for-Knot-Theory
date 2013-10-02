from math import *
import random

R2_up_moves = ['R2UpPlus', 'R2UpMinus']
up_moves = ['R2UpPlus', 'R2UpMinus', 'M2UpPlus', 'M2UpMinus']
horizontal_moves = ['R3', 'M1Forward', 'M1Backward', 'S']
down_moves = ['R2Down', 'M2Down']

opNames = ['R2UpPlus', 'R2UpMinus', 'M2UpPlus', 'M2UpMinus', 'R3', 'M1Forward',
	'M1Backward', 'S', 'R2Down', 'M2Down']

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
	
		
	

		
