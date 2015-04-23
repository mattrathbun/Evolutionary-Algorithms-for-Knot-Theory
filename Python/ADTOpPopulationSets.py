import ADTOpList
import random
import numpy
from datetime import datetime


opPopulationTypes = ['Move', 'CC']

class Population(object):

    def __init__(self, num, maxl, minl, opPopulationType=None, model='original'):
        # num is population size
        # minl, maxl are the min and max list sizes
        self.num = num
        self.maxl = maxl
        self.minl = minl
        
        self.opPopulationType = opPopulationType
        self.oplists = set()
        self.model = model
        if self.opPopulationType == 'Move':
            for i in range(num):
                self.oplists.add(ADTOpList.randomMoveList(maxl, minl))
        elif opPopulationType == 'CC':
            for i in range(num):
                self.oplists.add(ADTOpList.randomCCList(maxl, minl))
        else:
            for i in range(num):
                self.oplists.add(ADTOpList.randomOpList(maxl, minl))

    def toList(self):
        return list(self.oplists)

    def size(self):
        return len(self.oplists)

    def iterate(self, fit, mu=0.50):
        print "Starting to iterate"
        startiter = datetime.now()
        n = self.size()
        pop1 = list(self.oplists)
#         print "Looking at pop1"
#         for guy in pop1:
#             print guy.opListType
#         print "\n\n\n\n"
        
        fcmp = lambda x, y: cmp(fit(x), fit(y))
        print "Starting to sort"
        startsort = datetime.now()
        pop1.sort(cmp=fcmp)
        print "Finished sorting. Took this long: ", datetime.now() - startsort
        possible_survivors = set()
        tfv = 0
        # maxf = 0
        # minf = 1000000
        maxf = fit(pop1[-1])
        minf = fit(pop1[0])
        for ol in pop1:
            fv = fit(ol)
            if fv > 2:
                possible_survivors.add(ol.copy())
#                 print "     Look! We have a possible survivor: {}".format(ol.toString())
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
        possible_survivors = list(possible_survivors)
        possible_survivors.sort(cmp=fcmp)
        if len(possible_survivors) > persistence:
            survivors = [possible_survivors[-(i+1)].copy() for i in range(persistence)]
#            print "    We have {} possible_survivors!.".format(len(possible_survivors))
#             for l in survivors:
#                 l.toString()
        else:
            survivors = [ol.copy() for ol in possible_survivors]
#            print "    We have {} survivors!".format(len(survivors))
#             for l in survivors:
#                 l.toString()
                
        survivors = set(survivors)

        # pop2 will be the new population

        pop2 = set()

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
                    parent.append(candidates[best].copy())

                pop2.update(parent[0].recombine(parent[1], self.model))
                pop3 = pop2
        elif self.model == 'randtail' or self.model == 'modtail':
            pop2 = pop1[len(pop1)/2:]
            while len(pop2) < len(pop1)-min(len(survivors),persistence):
                if self.opPopulationType == 'Move':
#                     print "SHOULD ONLY BE PRODUCING MOVES"
                    pop2.append(ADTOpList.randomMoveList(self.maxl, self.minl))
                elif self.opPopulationType == 'CC':
#                     print "BUT NOT ONLY PRODUCING MOVES"
                    pop2.append(ADTOpList.randomCCList(self.maxl, self.minl))
                else:
#                     print "BUT NOT ONLY PRODUCING MOVES (2)"
                    pop2.append(ADTOpList.randomOpList(self.maxl, self.minl))

#         print "Looking at pop2 \n\n"
#         for guy in pop2:
#             print guy.opListType
        pop3 = list(pop2)
#         print "Looking at pop3: \n\n"
#         for guy in pop3:
#             print guy.opListType

        # mutation

        print "    Starting mutation"
        startmut = datetime.now()
        for i in range(len(pop3)):
            if (random.random() < mu):
                pop3[i].mutate(self.model)
        print "    Finished mutation. Took this long: ", datetime.now() - startmut
        
        pop3 = set(pop3)
        pop3.update(survivors)
#         print "    And now the survivors should be included in the population."
#         print "    Survivors:"
#         for l in survivors:
#             print l.toString()
        print "    Population:"
        for l in pop3:
            print "    ", l.toString()

        pop3 = list(pop3)
        

        print "    Re-sorting..."
        startsecondsort = datetime.now()
        pop3.sort(cmp=fcmp)
        print "    Finished second sort. Took this long: ", datetime.now() - startsecondsort
        
        self.oplists = set(pop3)
        
        print "Finished iteration. Took: ", datetime.now() - startiter
        print "\n"
        
        return pop3[-1]
        
        
