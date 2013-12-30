# Any benefit to encoding DT code as a dictionary {1:e_1, 3:e_3, ... } instead of a list?


# Helper function. Takes three numbers: i, m, M. (m meant to be min and M max).
# Returns i if i is between m and M. Otherwise, 
#   if i is smaller than m, return m, larger than M, return M
def normalise(i,m,M):
  return (m if i < m else (M if i > M else i))
  
# In case Matt forgets to use the British spelling.
def normalize(i,m,M):
  return normalise(i,m,M)

# Main class. Encodes a knot diagram as a Dowker-Thistlewaite code.
# DT-notation is represented by a list of even numbers, in correspondence with
#  a list of ordered odd numbers. 
class DTLink(object):
  def __init__(self,code):
    if isinstance(code,list):
      self.code = code
    elif isinstance(code,str):
      self.code = [int(x) for x in code.split()]
    else:
      raise TypeError("Argument must be either a list or a string.")

  def __eq__(self,other):
    if type(other) == type(self):
      return self.__dict__ == other.__dict__
    else:
      return False

  def __ne__(self,other):
    return not self.__eq__(other)

  def to_list(self):
    return self.code

  # Number of crossings in the diagram is the length of the code.
  def number_crossings(self):
    return len(self.code)

  def copy(self):
    new_dt = []
    for i in self.code:
      new_dt.append(i)
    return DTLink(new_dt)

  def to_string(self):
    return " ".join(str(x) for x in self.code)

  # Helper method. Given an integer arc, representing a number at one of the crossings in the diagram (even or odd),
  #   returns a 3-element list of the odd number at the crossing, the absolute value of the even number at that crossing,
  #   and a +1 or -1 depending on whether the even number is positive or negative (corresponding to whether
  #   the even number belongs to understrand or the overstrand of the diagram, respectively.
  def triple(arc):
    code = self.code
    n = self.number_crossings()
    arc = normalise(abs(arc),1,2*n)
    if (arc % 2 == 1):
      over = arc
      idx = (arc - 1)/2
      under = abs(code[idx])
      sign = cmp(code[idx],0)
      return [over,under,sign]
    else:
      under = abs(arc)
      # [0] added so that idx is an integer and not a list. (Else code[idx] does not work.)
      idx = [i for i,j in enumerate(code) if abs(j) == under][0]
      over = 2 * idx + 1
      sign = cmp(code[idx],0)
      return [over,under,sign]

  # Method that performs a Reidemeister 1 Move, introducing a single positive twist at the location arc.
  # arc is an integer corresponding to a label at one of the crossings of the diagram.
  # The twist should be introduced in the arc that immediately PREcedes the label arc.
  # Method mutates the DTLink object, and returns True if the move is successfully performed
  #   (which it always should since an R1Up move has no obstruction).
  def R1UpPlus(self,arc):
    n = self.number_crossings()
    idx = normalise(arc,1,2*n)
    new_dt = []
    for i in range(n+1):
      over = 2*i+1
      # Introduced indentation after the if, elif, and else statements.
      # For (odd) over indices before the strand to be changed, leave the (even) code the same if it is also before the strand to be changed,
      #   and change the (even) code by 2 if it is after the strand to be changed (arc/idx) (keeping the same sign).
      if (over < idx):
        # code at position i
	    ci = self.code[i]
	    # code sign at position i
	    cis = cmp(ci,0)
	    # absolute value of code at position i
	    cia = abs(ci)
	    # !!!! Why is this ci+2*cis instead of (ci+2)*cis ? !!!!
	    # I think it should be adding (even) numbers to the code with absolute value 2 greater
	    # than the corresponding old label, and having the same sign as the old label.
	    # This says change the label by +2 or -2.  
	    new_dt.append(ci if cia < idx else ci+2*cis)
	  # For over indices that equal the strand to be changed (necessarily odd), insert the next even number at that index in the code.
      elif (over == idx):
	    new_dt.append(idx+1)
      # For over indices that are one more than the (even) strand to be changed, insert the (even) strand to be changed at that index in the code.
      elif (over == idx+1):
	    new_dt.append(idx)
	  # For over indices after the strand to be changed, leave the (even) code the same if it is before the strand to be changed,
	  #   and change the (even) code by 2 if it is after the strand to be changed (arc/idx) (keeping the same sign).
      else:
        # Code index of the original code (shifted forward by one list position in the new code)
	    ci = self.code[i-1]
	    # Sign of the code in the original code (shifted forward by one list position in the new code)
	    cis = cmp(ci,0)
	    # Absolute value of the code index of the original code (shifted forward by one list position in the new code)
	    cia = abs(ci)
	    # !!!! Again, I think this should be (ci+2)*cis !!!!
	    new_dt.append(ci if cia < idx else ci+2*cis)
    self.code = new_dt
    return True

  # Method that performs a Reidemeister 1 Move, introducing a single negative twist at the location arc. (See R1UpPlus above).
  # Method mutates the DTLink object, and returns True if move is successfully performed (which it should, because there is no obstruction).
  def R1UpMinus(self,arc):
    n = self.number_crossings()
    idx = normalise(arc,1,2*n)
    new_dt = []
    for i in range(n+1):
      over = 2*i+1
      # Introduced indentation after the if, elif, and else statements.
      if (over < idx):
	      ci = self.code[i]
	      cis = cmp(ci,0)
	      cia = abs(ci)
	      # !!!! I think this should be (ci+2)*cis !!!!
	      new_dt.append(ci if cia < idx else ci+2*cis)
      elif (over == idx):
	      new_dt.append(-idx-1)
      elif (over == idx+1):
	      new_dt.append(-idx)
      else:
	      ci = self.code[i-1]
	      cis = cmp(ci,0)
	      cia = abs(ci)
	      new_dt.append(ci if cia < idx else ci+2*cis)
    self.code = new_dt
    return True

  # Method that performs a Reidemeister 1 Move, eliminating a single positive twist at the location arc.
  # Method mutates the DTLink object, returns True if move is successfully performed
  # (the move will be unsuccessful if the diagram does not contain a positive twist at the location arc, i.e. if 
  #  a (positive) even number in the code corresponds to an adjacent (odd) number.)
  def R1DownPlus(self,arc):
    n = self.number_crossings()
    arc = normalise(arc,1,2*n)
    new_dt = []
    success = False
    mn = 0
    for i in range(n):
      over = 2*i+1
      ci = self.code[i]
      
      # !!!! I believe that this does not remove a *positive* twist. Both a positive twist
      # and a negative twist can be introduced with the same DT code (by twisting right or left,
      # but either way having the even number correspond to the under-crossing. !!!!
      
      # !!!! In fact, more broadly, the DT notation does not uniquely determine a knot diagram,
      # as any connect-sum component of a diagram can be replaced by its mirror image, without
      # changing the DT code. For tabulating knots, this is not a problem, but for our purposes
      # of manipulating diagrams, this could be troublesome. There is probably a way to overdetermine
      # the code to eliminate this ambiguity? !!!!
       
      # Added indentation after the if and else statements.
      if ((arc == over) and (abs(over - ci) == 1)) or ((arc == ci) and abs(over - ci) == 1):
	      success = True
	      mn = min(over,ci)
      else:
	      new_dt.append(ci)
          for i in range(n-1):
            ni = new_dt[i]
            nis = cmp(ni,0)
            nia = abs(ni)
            new_dt[i] = (ni if nia < mn else ni-2*nis)
    self.code = new_dt
    return success

  def R1DownMinus(self,arc):
    n = self.number_crossings()
    arc = normalise(arc,1,2*n)
    new_dt = []
    success = False
    mn = 0
    for i in range(n):
      over = 2*i+1
      ci = self.code[i]
      if ((arc == over) and (abs(over + ci) == 1)) or ((arc == -ci) and abs(over + ci) == 1):
	success = True
	mn = min(over,-ci)
      else:
	new_dt.append(ci)
    for i in range(n-1):
      ni = new_dt[i]
      nis = cmp(ni,0)
      nia = abs(ni)
      new_dt[i] = (ni if nia < mn else ni-2*nis)
    self.code = new_dt
    return success
