


class Fit(object):
    def __init__(self, a, b, c, target):
        self.a = a
        self.b = b
        self.c = c
        self.target = target
    
    def __call__(self, ol):
        if ol.fitness == -float('inf'):
            L = self.target.copy()
            d, min_ol = ol.apply(L)
            if d.number_crossings() < 3:
                bonus = 10000
            else:
                bonus = 1
            ccCount = min_ol.ccCount()
            fitness = 1.0 + bonus/(d.number_crossings()**float(self.a) + ccCount**float(self.b) + min_ol.length()**float(self.c) + 1.0)
            ol.setFitness = fitness
            return fitness
        elif isinstance(ol.fitness, float):
            return ol.fitness
        else:
            raise TypeError("Not sure what self.fitness is.")