# Helper function. Takes three numbers: i, m, M. (m meant to be min and M max).
# Returns i if i is between m and M. Otherwise, 
#   if i is smaller than m, return m, larger than M, return M
def normalise(i,m,M):
  return (m if i < m else (M if i > M else i))
  
# In case Matt forgets to use the British spelling.
def normalize(i,m,M):
  return normalise(i,m,M)
  
# Helper function. Takes an even number, positive or negative, and returns
# 	the index at which that even number shows up in a DT-code.
def index(even, code):
  if even % 2 == 0:
    return [i for i,j in enumerate(code) if (abs(j) == abs(even))][0]
  else:
    raise TypeError("Only even numbers should be present in code.")

# Main class. Encodes a knot diagram by a Dowker-Thistlewaite code, 
#	augmented by extra data at each crossing as to whether the under-strand
#	crosses the over-strand to the left or to the right.
#	DT-notation is generally represented by a list of even numbers, in correspondence with
#	a list of ordered odd numbers.
#	We will encode a DTLink object as two lists:
#		1. A list of the even numbers associated with each odd number, c_1, c_2, ... c_{2n-1}; called 'code'.
#			The 'sign' of c_i is positive if the over-strand corresponds to the odd number (2i-1).
#			The 'sign' of c_i is negative if the over-strand corresponds to the even number |c_i|.
#		2. A list of +/-1's, with +1 meaning that the oriented over-strand when rotated counter-clockwise by 90 degrees aligns with
#			the oriented under-strand (regardless of the odd or even labeling), and -1 for vice versa; called 'orientations'
#			   ^    +1       ^   -1
#			   |             |
#			------>       ---|-->
#			   |             |
# Additional notes: A number i between 1 and 2n corresponds to both a crossing point in the diagram, as well as
#	an oriented edge in the diagram going from the point i to the point i+1.


class ADTLink(object):
  def __init__(self, code, orientations):
    if isinstance(code,list):
        self.code = code
    elif isinstance(code,str):
        self.code = [int(x) for x in code.split()]
    else:
        raise TypeError("Arguments must be either a list or a string.")
    if isinstance(orientations,list):
        self.orientations = orientations
    elif isinstance(orientations,str):
        self.code = [int(x) for x in orientations.split()]
    else:
        raise TypeError("Arguments must be either a list or a string.")
    if len(self.code) != len(self.orientations):
        raise TypeError("Code and Orientations must have the same length.")

  def __eq__(self,other):
    if type(other) == type(self):
      return self.__dict__ == other.__dict__
    else:
      return False

  def __ne__(self,other):
    return not self.__eq__(other)

  def to_list(self):
    return self.code, self.orientations

  # Number of crossings in the diagram is the length of the code.
  def number_crossings(self):
    return len(self.code)

  def copy(self):
    new_dt = []
    new_or = []
    for i in self.code:
      new_dt.append(i)
    for i in self.orientations:
        new_or.append(i)
    return ADTLink(new_dt, new_or)

  def to_string(self):
    codeString = " ".join(str(x) for x in self.code)
    orientationsString = " ".join(str(x) for x in self.orientations)
    return codeString, orientationsString

  # Helper method. Given an integer arc (odd or +/-even), returns a number between 1 and 2*n,
  #	  with the appropriate modular identification.
  def wrap(self, arc):
    n = self.number_crossings()
    if arc % (2*n) == 0:
        return 2*n
    else:
        return arc % (2*n)
        
  # Helper method. Given an integer arc, represented by a number at one of the crossings in the diagram (even or odd),
  #   returns a 4-element list of the odd number at the crossing; the absolute value of the even number at that crossing;
  #   and a +1 or -1 depending on whether the even number is positive or negative (corresponding to whether
  #   the even number belongs to under-strand or the over-strand of the diagram, respectively; and a +1 or -1 depending
  #	  on the orientation of the crossing.
  def quad(self, arc):
    code = self.code
    orient = self.orientations
    n = self.number_crossings()
    arc = normalise(abs(arc),1,2*n)
    if (arc % 2 == 1):
#      over = arc
        idx = (arc - 1)/2
#      under = abs(code[idx])
        even = abs(code[idx])
        sign = cmp(code[idx],0)
#      return [arc,under,sign]
        return [arc, even, sign, orient[idx]]
    else:
#      under = abs(arc)
        even = abs(arc)
      # [0] added so that idx is an integer and not a list. (Else code[idx] does not work.)
#      idx = [i for i,j in enumerate(code) if abs(j) == under][0]
        idx = [i for i,j in enumerate(code) if abs(j) == even][0]
#      over = 2 * idx + 1
        odd = 2 * idx + 1
        sign = cmp(code[idx],0)
#      return [over,under,sign]
        return [odd, even, sign, orient[idx]]

##### !!!!!
  # Methods that perform a Reidemeister 1 Move, introducing a single twist at the location arc.
  # arc is an integer corresponding to a label at one of the crossings of the diagram.
  # The twist should be introduced in the arc that immediately PROcedes the label arc (the arc which
  # connects the point arc to the point arc+1).
  # Method mutates the ADTLink object, and returns True if the move is successfully performed
  #   (which it always should since an R1Up move has no obstruction).
##### !!!!!
  def R1UpPlusLeft(self,arc):
    n = self.number_crossings()
    arc = normalise(arc,1,2*n)
    new_dt = []
    new_or = list(self.orientations)
    for i in self.code:
    	if abs(i) > arc:
    		new_dt.append(i + 2*cmp(i, 0))
    	else:
    		new_dt.append(i)
    if arc % 2 == 1:
        new_dt.insert((arc+1)/2, arc+1)
        new_or.insert((arc+1)/2, 1)
    else:
        new_dt.insert(arc/2, -(arc+2))
        new_or.insert(arc/2, 1)
    self.code = new_dt
    self.orientations = new_or
    return True
    
  def R1UpPlusRight(self,arc):
    n = self.number_crossings()
    arc = normalise(arc,1,2*n)
    new_dt = []
    new_or = list(self.orientations)
    for i in self.code:
    	if abs(i) > arc:
    		new_dt.append(i + 2*cmp(i, 0))
    	else:
    		new_dt.append(i)
    if arc % 2 == 1:
        new_dt.insert((arc+1)/2, -(arc+1))
        new_or.insert((arc+1)/2, 1)
    else:
        new_dt.insert(arc/2, arc+2)
        new_or.insert(arc/2, 1)
    self.code = new_dt
    self.orientations = new_or
    return True

  def R1UpMinusLeft(self,arc):
    n = self.number_crossings()
    arc = normalise(arc,1,2*n)
    new_dt = []
    new_or = list(self.orientations)
    for i in self.code:
    	if abs(i) > arc:
    		new_dt.append(i + 2*cmp(i, 0))
    	else:
    		new_dt.append(i)
    if arc % 2 == 1:
        new_dt.insert((arc+1)/2, -(arc+1))
        new_or.insert((arc+1)/2, -1)
    else:
        new_dt.insert(arc/2, arc+2)
        new_or.insert(arc/2, -1)
    self.code = new_dt
    self.orientations = new_or
    return True
        
  def R1UpMinusRight(self,arc):
    n = self.number_crossings()
    arc = normalise(arc,1,2*n)
    new_dt = []
    new_or = list(self.orientations)
    for i in self.code:
    	if abs(i) > arc:
    		new_dt.append(i + 2*cmp(i, 0))
    	else:
    		new_dt.append(i)
    if arc % 2 == 1:
        new_dt.insert((arc+1)/2, arc+1)
        new_or.insert((arc+1)/2, -1)
    else:
        new_dt.insert(arc/2, -(arc+2))
        new_or.insert(arc/2, -1)
    self.code = new_dt
    self.orientations = new_or
    return True	


  # Methods that perform a Reidemeister 1 Move, eliminating a single twist at the location arc.
  # Method mutates the ADTLink object, returns True if move is successfully performed
  # (the move will be unsuccessful if the diagram does not contain a positive twist at the location arc, i.e. if 
  #  a (positive) even number in the code corresponds to an adjacent (odd) number.)
  def R1DownPlusLeft(self, arc):
    n = self.number_crossings()
    arc = normalise(arc, 1, 2*n)
    new_dt = []
    temp_dt = list(self.code)
    new_or = list(self.orientations)
    if (arc % 2 == 1) and (self.code[((arc-1)/2) % n] == -(arc+1)) and (self.orientations[((arc-1)/2) % n] == 1):
        temp_dt.pop(((arc-1)/2) % n)
        for i in temp_dt:
            if abs(i) > arc+1 :
                new_dt.append(i - 2*cmp(i, 0))
            else:
                new_dt.append(i) 
        self.code = new_dt
        self.orientations.pop(((arc-1)/2) % n)
        return True
    elif (arc % 2 == 0) and (self.code[(arc/2) % n] == arc) and (self.orientations[(arc/2) % n] == 1):
        temp_dt.pop((arc/2) % n)
        for i in temp_dt:
            if abs(i) > arc:
                new_dt.append(i - 2*cmp(i,0))
            else:
                new_dt.append(i)
        self.code = new_dt
        self.orientations.pop((arc/2) % n)
        return True
    else:
        return False

  def R1DownPlusRight(self, arc):
    n = self.number_crossings()
    arc = normalise(arc, 1, 2*n)
    new_dt = []
    temp_dt = list(self.code)
    new_or = list(self.orientations)
    if (arc % 2 == 1) and (self.code[((arc-1)/2) % n] == arc+1) and (self.orientations[((arc-1)/2) % n] == 1):
        temp_dt.pop(((arc-1)/2) % n)
        for i in temp_dt:
            if abs(i) > arc+1:
                new_dt.append(i - 2*cmp(i, 0))
            else:
                new_dt.append(i) 
        self.code = new_dt
        self.orientations.pop(((arc-1)/2) %n)
        return True
    elif (arc % 2 == 0) and (self.code[(arc/2) % n] == -arc) and (self.orientations[(arc/2) % n] == 1):
        temp_dt.pop((arc/2) % n)
        for i in temp_dt:
            if abs(i) > arc:
                new_dt.append(i - 2*cmp(i,0))
            else:
                new_dt.append(i)
        self.code = new_dt
        self.orientations.pop((arc/2) % n)
        return True
    else:
        return False

  def R1DownMinusLeft(self, arc):
    n = self.number_crossings()
    arc = normalise(arc, 1, 2*n)
    new_dt = []
    temp_dt = list(self.code)
    new_or = list(self.orientations)
    if (arc % 2 == 1) and (self.code[((arc-1)/2) % n] == arc+1) and (self.orientations[((arc-1)/2) % n] == -1):
        temp_dt.pop(((arc-1)/2) % n)
        for i in temp_dt:
            if abs(i) > arc+1 :
                new_dt.append(i - 2*cmp(i, 0))
            else:
                new_dt.append(i) 
        self.code = new_dt
        self.orientations.pop(((arc-1)/2) % n)
        return True
    elif (arc % 2 == 0) and (self.code[(arc/2) % n] == -arc) and (self.orientations[(arc/2) % n] == -1):
        temp_dt.pop((arc/2) % n)
        for i in temp_dt:
            if abs(i) > arc:
                new_dt.append(i - 2*cmp(i,0))
            else:
                new_dt.append(i)
        self.code = new_dt
        self.orientations.pop((arc/2) % n)
        return True
    else:
        return False
            
  def R1DownMinusRight(self, arc):
    n = self.number_crossings()
    arc = normalise(arc, 1, 2*n)
    new_dt = []
    temp_dt = list(self.code)
    new_or = list(self.orientations)
    if (arc % 2 == 1) and (self.code[((arc-1)/2) % n] == -(arc+1)) and (self.orientations[((arc-1)/2) % n] == -1):
        temp_dt.pop(((arc-1)/2) % n)
        for i in temp_dt:
            if abs(i) > arc+1 :
                new_dt.append(i - 2*cmp(i, 0))
            else:
                new_dt.append(i) 
        self.code = new_dt
        self.orientations.pop(((arc-1)/2) % n)
        return True
    elif (arc % 2 == 0) and (self.code[(arc/2) % n] == arc) and (self.orientations[(arc/2) % n] == -1):
        temp_dt.pop((arc/2) % n)
        for i in temp_dt:
            if abs(i) > arc:
                new_dt.append(i - 2*cmp(i,0))
            else:
                new_dt.append(i)
        self.code = new_dt
        self.orientations.pop((arc/2) % n)
        return True
    else:
        return False

  # Helper method that takes a point at a crossing (odd or +/- even) and returns the other
  #		point at that crossing (+even or odd).
  def jump(self, point):
    n = self.number_crossings()
    odd, even, sign, orient = self.quad(point)
    if point % 2 == 1:
        return even
    elif point % 2 == 0:
        return odd
                          
  # Helper method that takes in an 'arc' and a 'side' ("L" or "R"), and returns:
  #		False and an empty list if the region to that side of arc is a monogon or bigon, 
  #		True and a list of all other arcs which are
  #			adjacent to the region on the side of the arc indicated by the arguments.
  #		These returned arcs are represented as two-element lists, from vertex to vertex (with positive labels).
#  def R2Candidates(self, arc, side):
#    side = str(side).lower()
#    if side in ["l", "left", "0"]:
#        side = 0
#    elif side in ["r", "right", "1"]:
#        side = 1
#    else:
#        raise TypeError("Side should be l or r.")
#    forward = 0
#    once = 0
#    output = []
#    n = self.number_crossings()
#    arc = normalise(arc, 1, 2*n)
##        odd, even, sign, orient = quad(arc)
#    tail = arc
#    head = self.wrap(arc + 1)
#    while True:
#        tail = self.jump(head)
#        odd, even, sign, orient = self.quad(tail)
#        if ((side + forward) % 2 == 0) and (tail % 2 == 1):
#            head = self.wrap(tail - sign*orient)
#        elif ((side + forward) % 2 == 0) and (tail % 2 == 0):
#            head = self.wrap(tail + sign*orient)
#        elif ((side + forward) % 2 == 1) and (tail % 2 == 1):
#            head = self.wrap(tail + sign*orient)
#        elif ((side + forward) % 2 == 1) and (tail % 2 == 0):
#            head = self.wrap(tail - sign*orient)
#        if (tail == arc and head == self.wrap(arc + 1)):
#            break
#        output.append([tail, head])
#        if ((tail - head) % (2*n) == 1):
#            forward = 1
#        else:
#        	forward = 0
#    if len(output) > 1:
#        return True, output
#    else:
#        return False, []

  def regions(self, arc, side):
    side = str(side).lower()
    if side in ["l", "left", "0"]:
        side = 0
    elif side in ["r", "right", "1"]:
        side = 1
    else:
        raise TypeError("Side should be l or r.")
    forward = 0
    once = 0
    output = []
    n = self.number_crossings()
    arc = normalise(arc, 1, 2*n)
#        odd, even, sign, orient = quad(arc)
    tail = arc
    head = self.wrap(arc + 1)
    while True:
        tail = self.jump(head)
        odd, even, sign, orient = self.quad(tail)
        if ((side + forward) % 2 == 0) and (tail % 2 == 1):
            head = self.wrap(tail - sign*orient)
        elif ((side + forward) % 2 == 0) and (tail % 2 == 0):
            head = self.wrap(tail + sign*orient)
        elif ((side + forward) % 2 == 1) and (tail % 2 == 1):
            head = self.wrap(tail + sign*orient)
        elif ((side + forward) % 2 == 1) and (tail % 2 == 0):
            head = self.wrap(tail - sign*orient)
        output.append([tail, head])
        if (tail == arc and head == self.wrap(arc + 1)):
            break
        if ((tail - head) % (2*n) == 1):
            forward = 1
        else:
        	forward = 0
#    print 'output of regions is: {}'.format(output)
    return output

  ##### !!!!!
  # Methods that perform a Reidemeister 2 Move, introducing two additional crossings.
  # arc -- is an integer corresponding to a label at one of the crossings of the diagram, indicating the edge
  #   from arc to arc+1 (or rather, wrap(arc+1)).
  # side -- is a choice of 'l' or 'r' to determine to which side of arc in the diagram arc will be 
  #   perturbed to introduce the additional crossings with another strand. 
  # edge -- is a two-element list [edge0, edge1].
  # [edge0, edge1] -- is the other strand that arc will cross over or under.  
  # Method mutates the ADTLink object, and returns True if the move is successfully performed
##### !!!!!

  # Note also, the parity of arc will be the same as the parity of edge0, if [edge0, edge1]
  #   represents an edge adjacent to a region determined by arc.

  def R2UpPlus(self, arc, side, edge):
  	n = self.number_crossings()
  	arc = normalise(arc, 1, 2*n)
  	candidates = list(self.regions(arc, side))
  	candidates.remove([arc, self.wrap(arc+1)])
  	if not(edge in candidates):
  		return False
  	new_dt = []
  	new_or = list(self.orientations)
  	edge0, edge1 = edge
  	if side in ['l', 'left', '0']:
  		side = 1
  	elif side in ['r', 'right', '1']:
  		side = -1
  	else:
  		raise TypeError("Side should be l or r.")
  	if arc % 2 == 0:
  		if arc < edge0:
			if edge1 == self.wrap(edge0 + 1):
				for i in self.code:
					if (abs(i) > arc) and (abs(i) > edge0):
						new_dt.append(i + 4*cmp(i, 0))
					elif (abs(i) > arc):
						new_dt.append(i + 2*cmp(i, 0))
					else: # abs(i) <= arc
						new_dt.append(i)
				new_dt.insert(arc/2, edge0 + 4)
				new_or.insert(arc/2, side)
				new_dt.insert(edge0/2 + 1, -(arc + 2))
				new_or.insert(edge0/2 + 1, -side)
			else: # edge0 == self.wrap(edge1 + 1)
				for i in self.code:
  					if (abs(i) > arc) and (abs(i) >= edge0):
  						new_dt.append(i + 4*cmp(i, 0))
  					elif (abs(i) > arc):
  						new_dt.append(i + 2*cmp(i, 0))
  					else: # abs(i) <= arc
  						new_dt.append(i)
  				new_dt.insert(arc/2, edge0 + 2)
  				new_or.insert(arc/2, -side)
  				new_dt.insert(edge0/2 + 1, -(arc + 2))
  				new_or.insert(edge0/2 + 1, side)
  		else: # edge0 < arc
  			if edge1 == self.wrap(edge0 + 1):
  				for i in self.code:
  					if (abs(i) > arc):
  						new_dt.append(i + 4*cmp(i, 0))
  					elif (abs(i) > edge0): # but <= arc
  						new_dt.append(i + 2*cmp(i, 0))
  					else: # abs(i) <= edge0
  						new_dt.append(i)
  				new_dt.insert(edge0/2, -(arc + 4))
  				new_or.insert(edge0/2, -side)
  				new_dt.insert(arc/2 + 1, edge0 + 2)
  				new_or.insert(arc/2 + 1, side)
  			else: # edge1 < edge0
  				for i in self.code:
  					if (abs(i) > arc):
  						new_dt.append(i + 4*cmp(i, 0))
  					elif (abs(i) >= edge0): # but <= arc
  						new_dt.append(i + 2*cmp(i, 0))
  					else: # abs(i) < edge0
  						new_dt.append(i)
  				new_dt.insert(edge0/2, -(arc + 4))
  				new_or.insert(edge0/2, side)
  				new_dt.insert(arc/2 + 1, edge0)
  				new_or.insert(arc/2 + 1, -side)
  	else: # arc % 2 == 1
  		if arc < edge0:
  			if edge1 == self.wrap(edge0 + 1):
  				for i in self.code:
  					if abs(i) > edge0:
  						new_dt.append(i + 4*cmp(i, 0))
  					elif abs(i) > arc: # but <= edge0
  						new_dt.append(i + 2*cmp(i, 0))
  					else: # abs(i) <= arc
  						new_dt.append(i)
  				new_dt.insert((arc + 1)/2, edge1 + 2)
  				new_or.insert((arc + 1)/2, -side)
  				new_dt.insert(edge1/2 + 1, -(arc + 1))
  				new_or.insert(edge1/2 + 1, side)
  			else: # edge0 == self.wrap(edge1 + 1)
  				for i in self.code:
  					if abs(i) >= edge0:
  						new_dt.append(i + 4*cmp(i, 0))
  					elif abs(i) > arc: # but < edge0
  						new_dt.append(i + 2*cmp(i, 0))
  					else: # abs(i) <= arc
  						new_dt.append(i)
  				new_dt.insert((arc + 1)/2, edge1 + 4)
  				new_or.insert((arc + 1)/2, side)
  				new_dt.insert(edge1/2 + 1, -(arc + 1))
  				new_or.insert(edge1/2 + 1, -side)
  		else: # edge0 < arc
  			if edge1 == self.wrap(edge0 + 1):
  				for i in self.code:
  					if abs(i) > arc:
  						new_dt.append(i + 4*cmp(i, 0))
  					elif abs(i) > edge0: # but <= arc
  						new_dt.append(i + 2*cmp(i, 0))
  					else: # abs(i) <= edge0
  						new_dt.append(i)
  				new_dt.insert(edge1/2, -(arc + 3))
  				new_or.insert(edge1/2, side)
  				new_dt.insert((arc + 1)/2 + 1, edge0 + 1)
  				new_or.insert((arc + 1)/2 + 1, -side)
  			else: # edge0 == self.wrap(edge1 + 1)
  				for i in self.code:
  					if abs(i) > arc:
  						new_dt.append(i + 4*cmp(i, 0))
  					elif abs(i) >= edge0: # but <= arc
  						new_dt.append(i + 2*cmp(i, 0))
  					else: # abs(i) < edge0
  						new_dt.append(i)
  				new_dt.insert(edge1/2, -(arc + 3))
  				new_or.insert(edge1/2, -side)
  				new_dt.insert((arc + 1)/2 + 1, edge0 + 1)
  				new_or.insert((arc + 1)/2 + 1, side)
  	self.code = new_dt
  	self.orientations = new_or
  	return True
  	
  				
  				
  				
  				
  				
#   		if edge1 == self.wrap(edge0 + 1):
#   			for i in self.code:
#   				if abs(i) > min(arc, edge0) and abs(i) <= max(arc, edge0):
#   					new_dt.append(i + 2*cmp(i, 0))
#   				elif abs(i) > max(arc, edge0):
#   					new_dt.append(i + 4*cmp(i, 0))
#   				else:
#   					new_dt.append(i)
#   			new_dt.insert(min(arc, edge0)/2, -(max(arc, edge0) + 4))
#   			new_or.insert(min(arc, edge0)/2, -1)
#   			new_dt.insert(max(arc, edge0)/2 + 1, min(arc, edge0) + 2)
#   			new_or.insert(max(arc, edge0)/2 + 1, 1)
#   		else:
#   			print "edge1 != self.wrap(edge0 + 1)"
#   			if edge0 == min(arc, edge0):
#   				for i in self.code:  				
#   					print "arc = {}".format(arc)
#   					print "edge0 = {}".format(edge0)
#   					print "min(arc, edge0) = {}".format(min(arc, edge0))
#   					if abs(i) > edge0 and abs(i) <= arc:
#   						new_dt.append(i + 2*cmp(i, 0))
#   					elif abs(i) > arc:
#   						new_dt.append(i + 4*cmp(i, 0))
#   					else:
#   						new_dt.append(i)
#   				new_dt.insert(edge0/2, -(arc + 4))
#   				new_or.insert(edge0/2, 1)
#   				new_dt.insert((arc/2) + 1, edge0)
#   				new_or.insert((arc/2) + 1, -1)
#   			else:
#   				print "arc = {}".format(arc)
#   				print "edge0 = {}".format(edge0)
#   				print "min(arc, edge0) = {}".format(min(arc, edge0))
#   				for i in self.code:
#   					print "i = {}".format(i)
#   					if abs(i) > arc and abs(i) < edge0:
#   						new_dt.append(i + 2*cmp(i, 0))
#   					elif abs(i) >= edge0:
#   						new_dt.append(i + 4*cmp(i, 0))
#   					else:
#   						new_dt.append(i)
#   				new_dt.insert(arc/2, edge0 + 2)
#   				new_or.insert(arc/2, -1)
#   				new_dt.insert((edge0/2) + 1, -(arc + 2))
#   				new_or.insert((edge0/2) + 1, 1)
#   	self.code = new_dt
#   	self.orientations = new_or
#   	return True
  
#   def R2UpPlus(self, arc, side, edge):
#   	n = self.number_crossings()
#   	arc = normalise(arc, 1, 2*n)
#   	candidates = list(self.regions(arc, side))
#   	candidates.remove([arc, self.wrap(arc+1)])
#   	if not(edge in candidates):
#   		return False
#   	new_dt = []
#   	new_or = list(self.orientations)
#   	edge0, edge1 = edge
#   	if side in ['l', 'left', '0']:
#   		side = 1
#   	elif side in ['r', 'right', '1']:
#   		side = -1
#   	else:
#   		raise TypeError("Side should be l or r.")
#   	if arc % 2 == 0:
#   		if edge1 == self.wrap(edge0 + 1):
#   			for i in self.code:
#   				if abs(i) > min(arc, edge0) and abs(i) <= max(arc, edge0):
#   					new_dt.append(i + 2*cmp(i, 0))
#   				elif abs(i) > max(arc, edge0):
#   					new_dt.append(i + 4*cmp(i, 0))
#   				else:
#   					new_dt.append(i)
#   			new_dt.insert(min(arc, edge0)/2, -(max(arc, edge0) + 4))
#   			new_or.insert(min(arc, edge0)/2, -1)
#   			new_dt.insert(max(arc, edge0)/2 + 1, min(arc, edge0) + 2)
#   			new_or.insert(max(arc, edge0)/2 + 1, 1)
#   		else:
#   			print "edge1 != self.wrap(edge0 + 1)"
#   			if edge0 == min(arc, edge0):
#   				for i in self.code:  				
#   					print "arc = {}".format(arc)
#   					print "edge0 = {}".format(edge0)
#   					print "min(arc, edge0) = {}".format(min(arc, edge0))
#   					if abs(i) > edge0 and abs(i) <= arc:
#   						new_dt.append(i + 2*cmp(i, 0))
#   					elif abs(i) > arc:
#   						new_dt.append(i + 4*cmp(i, 0))
#   					else:
#   						new_dt.append(i)
#   				new_dt.insert(edge0/2, -(arc + 4))
#   				new_or.insert(edge0/2, 1)
#   				new_dt.insert((arc/2) + 1, edge0)
#   				new_or.insert((arc/2) + 1, -1)
#   			else:
#   				print "arc = {}".format(arc)
#   				print "edge0 = {}".format(edge0)
#   				print "min(arc, edge0) = {}".format(min(arc, edge0))
#   				for i in self.code:
#   					print "i = {}".format(i)
#   					if abs(i) > arc and abs(i) < edge0:
#   						new_dt.append(i + 2*cmp(i, 0))
#   					elif abs(i) >= edge0:
#   						new_dt.append(i + 4*cmp(i, 0))
#   					else:
#   						new_dt.append(i)
#   				new_dt.insert(arc/2, edge0 + 2)
#   				new_or.insert(arc/2, -1)
#   				new_dt.insert((edge0/2) + 1, -(arc + 2))
#   				new_or.insert((edge0/2) + 1, 1)
#   	self.code = new_dt
#   	self.orientations = new_or
#   	return True


# n = self.number_crossings()
#     arc = normalise(arc,1,2*n)
#     new_dt = []
#     new_or = list(self.orientations)
#     for i in self.code:
#     	if abs(i) > arc:
#     		new_dt.append(i + 2*cmp(i, 0))
#     	else:
#     		new_dt.append(i)
#     if arc % 2 == 1:
#         new_dt.insert((arc+1)/2, arc+1)
#         new_or.insert((arc+1)/2, -1)
#     else:
#         new_dt.insert(arc/2, -(arc+2))
#         new_or.insert(arc/2, -1)
#     self.code = new_dt
#     self.orientations = new_or
#     return True	
    
    



#    while (self.jump(head) != arc) or (once == 0):
#        once += 1
#        tail = self.jump(head)
#        odd, even, sign, orient = self.quad(tail)
#        if ((side + forward) % 2 == 0) and (tail % 2 == 1):
#            head = self.wrap(tail - sign*orient)
#            idx = index((arc+1) % n, self.code)
#            output.append([self.code[idx] , 2*idx + 1 - cmp(self.code[idx], 0)*self.orientations[idx]])
#        elif ((side + forward) % 2 == 0) and (tail % 2 == 0):
#            head = self.wrap(tail + sign*orient)
#        elif ((side + forward) % 2 == 1) and (tail % 2 == 1):
#            head = self.wrap(tail + sign*orient)
#        elif ((side + forward) % 2 == 1) and (tail % 2 == 0):
#            head = self.wrap(tail - sign*orient)
#        output.append([tail, head])
#        if ((tail - head) % (2*n) == 1):
#            forward = 1
#        else:
#        	forward = 0
#    if (self.jump(head) - head) % (2*n) in [-1, 1]:
#        tail = self.jump(head)
#        odd, even, sign, orient = self.quad(tail)
#        if ((side + forward) % 2 == 0) and (tail % 2 == 1):
#            head = self.wrap(tail - sign*orient)
#        elif ((side + forward) % 2 == 0) and (tail % 2 == 0):
#            head = self.wrap(tail + sign*orient)
#        elif ((side + forward) % 2 == 1) and (tail % 2 == 1):
#            head = self.wrap(tail + sign*orient)
#        elif ((side + forward) % 2 == 1) and (tail % 2 == 0):
#            head = self.wrap(tail - sign*orient)
#        output.append([tail, head])
#    if len(output) > 1:
#        return True, output
#    else:
#        return False, []

  def phi(self,i,r):
    if (i == r):
      return 1
    ar = self.jump(r)
    ai = self.jump(i)
    odd,even,sign,orient = self.quad(r)
    rm1 = self.wrap(r-1)
    phirm1 = self.phi(i,rm1)
    if (ai > i):
      if (ar >= i and ar <= ai):
        return -phirm1
      else:
        return phirm1
    else:
      if (ar >= i and ar <= ai):
        return phirm1
      else:
        return -phirm1

