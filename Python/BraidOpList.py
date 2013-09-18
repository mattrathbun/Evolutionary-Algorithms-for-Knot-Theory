import BraidOp
from random import *

class BraidOpList(object):
	def __init__(self, opList):
		self.opList = opList
		
	def copy(self):
		ol = []
		for i in self.opList:
			ol.append(i)
		return BraidOpList(ol)
		
	def length(self):
		return len(self.opList)
		
	
		
	



def randomOpList(minl, maxl):
	length = randint(minl, maxl)
	