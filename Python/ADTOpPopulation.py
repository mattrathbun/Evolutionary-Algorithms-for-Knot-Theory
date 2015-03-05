import ADTOpList
import random
import numpy
from datetime import datetime


opPopulationTypes = ['Move', 'CC']

class Population(object):

    def __init__(self, num, maxl, minl, opPopulationType=None, model='original'):
        # num is population size
        # minl, maxl are the min and max list sizes
        self.opPopulationType = opPopulationType
        self.oplists = []
        self.model = model
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

    def iterate(self, fit, mu=0.15):
        print "Starting to iterate"
        startiter = datetime.now()
        n = self.size()
        pop1 = list(self.oplists)
        fcmp = lambda x, y: cmp(fit(x), fit(y))
        print "Starting to sort"
        startsort = datetime.now()
        pop1.sort(cmp=fcmp)
        print "Finished sorting. Took this long: ", datetime.now() - startsort
        possible_survivors = []
        tfv = 0
        # maxf = 0
        # minf = 1000000
        maxf = fit(pop1[-1])
        minf = fit(pop1[0])
        for ol in pop1:
            fv = fit(ol)
            if fv > 2:
                possible_survivors.append(ol)
                print "     Look! We have a possible survivor: {}".format(ol.toString())
            # maxf = (fv if fv > maxf else maxf)
            # minf = (fv if fv < maxf else minf)
            tfv += fv
        afv = tfv / n

        print "total fitness   = ", tfv
        print "average fitness = ", afv
        print "max fitness     = ", maxf
        print "min fitness     = ", minf
        print ""

        # persistence is a parameter to check for a proportion of the population that succeeds in the goal
        #   and will be forced to survive (without mutation) into the next generation
        persistence = max(1, self.size()/10)

        # takes the highest (persistence) many members of the possible_survivors in order to force
        #   them through to the next generation
        possible_survivors.sort()
        if len(possible_survivors) > persistence:
            survivors = [possible_survivors[-(i+1)] for i in range(persistence)]
            print "    We have {} possible_survivors!.".format(len(possible_survivors))
            for l in survivors:
                l.toString()
        else:
            survivors = possible_survivors
            print "    We have {} survivors!".format(len(survivors))
            for l in survivors:
                l.toString()

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

        if self.model == 'original':
            for i in range(len(pop1)/2):
                parent = []
                for j in range(0, 2):
                    candidates = random.sample(pop1, 3)
                    fitnesses = map(fit, candidates)
                    best = numpy.argmax(fitnesses)
                    parent.append(candidates[best])

                pop2.extend(parent[0].recombine(parent[1], self.model))
                pop3 = pop2
        elif self.model == 'randtail' or self.model == 'modtail':
            for i in range(len(pop1)-min(len(survivors),persistence)):
                candidates = random.sample(pop1, 3)
                fitnesses = map(fit, candidates)
                best = numpy.argmax(fitnesses)
                pop2.append(candidates[best])
            pop3 = pop2
        # mutation

        print "Starting mutation"
        startmut = datetime.now()
        for i in range(len(pop3)):
            if (random.random() < mu):
                pop3[i].mutate(self.model)
        print "Finished mutation. Took this long: ", datetime.now() - startmut
        
        pop3.extend(survivors)
        print "    And now the survivors should be included in the population."
        print "    Survivors:"
        for l in survivors:
            print l.toString()
        print "    Population:"
        for l in pop3:
            print "    "+l.toString()

        pop3.sort(cmp=fcmp)
        self.oplists = pop3
        print "Finished iteration. Took: ", datetime.now() - startiter
