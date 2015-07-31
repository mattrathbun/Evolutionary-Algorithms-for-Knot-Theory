## fitness function for simplifying diagrams of unknots.

import ADT, ADTOp, ADTOpList, ADTOpPopulationSets

K = ADT.ADT([-16, -4, -6, -26, -10, -20, 24, 2, 14, 18, 22, 12, 8], [1, -1, -1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1])

def fit(ol):
    if ol.fitness == -float('inf'):
        L = K.copy()
        d, min_ol = ol.apply(L)
        if d.number_crossings() < 3:
            bonus = 10000
        else:
            bonus = 1
        fitness = 1.0 + bonus/(d.number_crossings()**2.0 + min_ol.length() + 1.0)
        ol.setFitness(fitness)
        return fitness
    elif isinstance(ol.fitness, float):
        return ol.fitness
    else:
        raise TypeError("Not sure what self.fitness is.")
    #return 1.0 + bonus/(d.number_crossings()**5.0 + ccCount + 1.0)
