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

  def number_crossings(self):
    return len(self.code)

  def copy(self):
    new_dt = []
    for i in self.code:
      new_dt.append(i)
    return DTLink(new_dt)

  def to_string(self):
    return " ".join(str(x) for x in self.code)

  def R1UpPlus(self,arc):
    n = self.number_crossings()
    idx = (1 if arc < 1 else arc)
    idx = (2*n if arc > 2*n else arc)
    new_dt = []
    for i in range(n+1):
      over = 2*i+1
      if (over < idx):
	ci = self.code[i]
	cis = cmp(ci,0)
	cia = abs(ci)
	new_dt.append(ci if cia < idx else ci+2*cis)
      elif (over == idx):
	new_dt.append(idx+1)
      elif (over == idx+1):
	new_dt.append(idx)
      else:
	ci = self.code[i-1]
	cis = cmp(ci,0)
	cia = abs(ci)
	new_dt.append(ci if cia < idx else ci+2*cis)
    self.code = new_dt
    return True

  def R1UpMinus(self,arc):
    n = self.number_crossings()
    idx = (1 if arc < 1 else arc)
    idx = (2*n if arc > 2*n else arc)
    new_dt = []
    for i in range(n+1):
      over = 2*i+1
      if (over < idx):
	ci = self.code[i]
	cis = cmp(ci,0)
	cia = abs(ci)
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

  def R1DownPlus(self,arc):
    n = self.number_crossings()
    arc = (1 if arc < 1 else arc)
    arc = (2*n if arc > 2*n else arc)
    new_dt = []
    success = False
    mn = 0
    for i in range(n):
      over = 2*i+1
      ci = self.code[i]
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
    arc = (1 if arc < 1 else arc)
    arc = (2*n if arc > 2*n else arc)
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
