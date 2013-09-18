import braidOpList

class Population(object):
  def __init__(self,num,maxl,minl):
    self.oplists = []
    for i in range(num):
      self.oplists.append(braidOpList.randomList(maxl,minl))

  def toList(self):
    return self.oplists

  def size(self):
    return len(self.oplists)

