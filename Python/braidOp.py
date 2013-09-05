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
		strand_index = 'undetermined'
	else:
		strand_index = None
	return BraidOp(randOp, strand_index)

class BraidOp(object):
	def __init__(self, op, strand_index=None):
		self.op = op
		self.strand_index = strand_index
		## Takes a string from the list opNames, and an optional positive integer 
		## strand_index that defaults to None
		## This is because the R2_up_moves require an additional parameter to be well-defined.
		#### Special note: This parameter cannot be determined randomly here, because
		#### the allowed values depend on the braid index of the braid being operated on.
		
		
	def copy(self):
		return BraidOp(self.op, self.strand_index)
		
	def apply(self, braid):
		if self.op in R2_up_moves:
			print 'I am here now.'
			if self.strand_index == 'undetermined':
				self.strand_index = random.randint(1, braid.braid_index() - 1)
			getattr(braid, self.op)(self.strand_index)
		else:
			getattr(braid, self.op)()
		
	
		
	

		