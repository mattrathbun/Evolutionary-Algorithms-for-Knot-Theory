from math import *
import random
from sys import argv

#file = argv[1]

unknot = [1]

class Braid(object):
	def __init__(self, braid):
		self.braid = braid
	## Takes in a braid _as a list_.
	
	def __eq__(self,other):
		if type(other) == type(self):
			return self.__dict__ == other.__dict__
		else:
			return False
						
	def __ne__(self,other):
		return not self.__eq__(other)
			
	def toList(self):
		return self.braid
	
	def number_crossings(self):
		return len(self.braid)
	
	def braid_index(self):
		return max(abs(max(self.braid)), abs(min(self.braid)))+1
		
	def copy(self):
		new_braid = []
		for i in self.braid:
			new_braid.append(i)
		return Braid(new_braid)		

		
## UP moves ##
##############
	
## Introduces crossings between strands strand_index and (strand_index+1)
## Assume that this happens at the end of the word (bottom of the braid)
## 	(Okay because of MarkovII move).			
####
	def R2UpPlus(self, strand_index):
		if (strand_index + 1) > self.braid_index() or strand_index < 1:
			return Braid(self.braid)
		else:
			self.braid.append(strand_index)
			self.braid.append(-strand_index)
			return Braid(self.braid)
			
	def R2UpMinus(self, strand_index):
		if (strand_index + 1) > self.braid_index():
			return Braid(self.braid)
		else:
			self.braid.append(-strand_index)
			self.braid.append(strand_index)
			return Braid(self.braid)
			
####

## Reidemeister II moves are special because they require an additional argument
####

	R2_up_moves = [R2UpPlus, R2UpMinus]
	
####


## MarkovII is stabilization/de-stabilization / Reidemeister I moves
####

	def M2UpPlus(self):
		m = self.braid_index()
		self.braid.append(m)
		return Braid(self.braid)
		
	def M2UpMinus(self):
		m = self.braid_index()
		self.braid.append(-m)
		return Braid(self.braid)
		
####

	up_moves = [R2UpPlus, R2UpMinus, M2UpPlus, M2UpMinus]

## HORIZONTAL moves ##
###################

## Reidemeister III moves/braid relation moves
####

	def R3(self):
		if len(self.braid) > 2:
			for i in reversed( range(2, len(self.braid)) ):
				if (self.braid[i] == self.braid[i-2]) & (abs(self.braid[i] - self.braid[i-1]) == 1):
					self.braid[i],self.braid[i-1],self.braid[i-2] = self.braid[i-1],self.braid[i],self.braid[i-1]
					return Braid(self.braid)
			return Braid(self.braid)
		else:
			return Braid(self.braid)	
####

## We will take MarkovI to cycle the last generator (crossing) to the beginning
## (This is sufficient in lieu of general conjugation because we have included
## the other Reidemeister moves)
####
	def M1Forward(self):
		self.braid.insert(0, self.braid.pop())
		return Braid(self.braid)
	
## We almost certainly don't need this, but it might be useful to have
## the reverse operation (for efficiency?)
	def M1Backward(self):
		self.braid.append(self.braid.pop(0))
		return Braid(self.braid)
####

## S corresponds to sliding two crossings past one another.

## Only acts on the first instance where it is possible (thanks to MarkovI)
####
	def S(self):
		for i in reversed(range(len(self.braid))):
			if abs(abs(self.braid[i]) - abs(self.braid[i-1])) > 1:
				self.braid[i],self.braid[i-1] = self.braid[i-1],self.braid[i]
				return Braid(self.braid)
		return Braid(self.braid)
####

	horizontal_moves = [R3, M1Forward, M1Backward, S]

## DOWN moves ##
################


## MarkovII is stabilization/de-stabilization / Reidemeister I moves
####

	def M2Down(self):
		if abs(self.braid[-1]) == (self.braid_index() - 1) & len(self.braid) > 1:
			self.braid.pop()
			return Braid(self.braid)
		else:
			return Braid(self.braid)	
####

## R2Down looks only for the first instance (from the bottom of the braid) to cancel
## two crossings
####

	def R2Down(self):
		if len(self.braid) > 2:
			for i in reversed( range(1, len(self.braid)) ):
				if self.braid[i] == -self.braid[i-1]:
					del self.braid[i-1]
					del self.braid[i-1]
					return Braid(self.braid)
			return Braid(self.braid)
		else:
			return Braid(self.braid)
####

	down_moves = [R2Down, M2Down]
		
##########
