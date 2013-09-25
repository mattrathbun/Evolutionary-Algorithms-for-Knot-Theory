import braidOpList
import random

class Population(object):
  def __init__(self,num,maxl,minl):
    self.oplists = []
    for i in range(num):
      self.oplists.append(braidOpList.randomList(maxl,minl))

  def toList(self):
    return self.oplists

  def size(self):
    return len(self.oplists)

  def iterate(self, fit, mu = 0.05):
    n = self.size()
    pop1 = self.oplists.copy()
    fcmp = lambda x,y: cmp(fit(x),fit(y))
    pop1.sort(cmp = fcmp)
    tfv = 0
    maxf = 0
    minf = 1000000
    for ol in pop1:
      fv = fit(ol)
      maxf = (fv > maxf ? fv : maxf)
      minf = (fv < minf ? fv : minf)
      tfv += fv
    afv = tfv/n

    print "total fitness   = ", tfv
    print "average fitness = ", afv
    print "max fitness     = ", maxf 
    print "min fitness     = ", minf 

    pop2 = []
    for ol in pop1:
      fv = fit(ol)
      i = fv/afv
      while (i>0):
	if random.random() <= i:
	  pop2.append(ol.copy())
        i--
    for i in range(len(pop2),len(pop1)):
      pop2.insert(0,pop1[0].copy())
    pop2 = pop2[:n]

    for i in range(0,len(pop2)-1,2):
      BraidOpList.recombine(pop2[i],pop2[i+1])

    for i in range(len(pop2)):
      if (random.random() < mu):
	pop2[i].mutate()

    pop2.sort(cmp = fcmp)
    self.oplists = pop2
