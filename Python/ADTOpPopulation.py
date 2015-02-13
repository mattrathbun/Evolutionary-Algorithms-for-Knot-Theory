import ADTOpList
import random
import numpy

opPopulationTypes = ['Move', 'CC']

class Population(object):

    def __init__(self, num, maxl, minl, opPopulationType=None):
        # num is population size
        # minl, maxl are the min and max list sizes
        self.opPopulationType = opPopulationType
        self.oplists = []
        if self.opPopulationType == 'Move':
            for i in range(num):
                self.oplists.append(ADTOpList.randomMoveList(maxl, minl))
        elif opPopulationType == 'CC':
            for i in range(num):
                self.oplists.append(ADTOpList.randomCCList(maxl, minl))
        else:
            for i in range(num):
                self.oplists.append(ADTOpList.randomOpList(maxl, minl))

    def toList(self):
        return self.oplists

    def size(self):
        return len(self.oplists)

    def iterate(self, fit, mu=0.05):
        n = self.size()
        pop1 = list(self.oplists)
        fcmp = lambda x, y: cmp(fit(x), fit(y))
        pop1.sort(cmp=fcmp)
        tfv = 0
        # maxf = 0
        # minf = 1000000
        maxf = fit(pop1[-1])
        minf = fit(pop1[0])
        for ol in pop1:
            fv = fit(ol)
            # maxf = (fv if fv > maxf else maxf)
            # minf = (fv if fv < maxf else minf)
            tfv += fv
        afv = tfv / n

        print "total fitness   = ", tfv
        print "average fitness = ", afv
        print "max fitness     = ", maxf
        print "min fitness     = ", minf
        print ""

        # pop2 will be the new population

        pop2 = []

        # generating a new population

        # for ol in pop1:
        #     fv = fit(ol)
        #     i = fv / afv
        #     while (i > 0):
        #         if random.random() <= i:
        #             pop2.append(ol.copy())
        #             i -= 1

        # do we need to do this?
        # because we are overwriting all of pop2 later
        # for i in range(len(pop2), len(pop1)):
        #     pop2.insert(0, pop1[0].copy())
        #     pop2 = pop2[:n]

        # recombination - the old way, this code can be deleted??

        #   for i in range(0,len(pop2)-1,2):
        #    ADTOpList.recombine(pop2[i],pop2[i+1])

        # recombination with tournament selection size 3

        for i in range(len(pop1)/2):
            parent = []
            for j in range(0, 2):
                candidates = random.sample(pop1, 3)
                fitnesses = map(fit, candidates)
                best = numpy.argmax(fitnesses)
                parent.append(candidates[best])

            pop2.extend(parent[0].recombine(parent[1]))

        # mutation

        for i in range(len(pop2)):
            if (random.random() < mu):
                pop2[i].mutate()

        pop2.sort(cmp=fcmp)
        self.oplists = pop2
