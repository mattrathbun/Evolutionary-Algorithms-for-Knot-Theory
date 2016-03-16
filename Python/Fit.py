

# 
# class Fit(object):
#     def __init__(self, a, b, c, d, target):
#         self.a = a
#         self.b = b
#         self.c = c
#         self.d = d
#         self.target = target
#     
#     def __call__(self, ol):
#         if ol.fitness == -float('inf'):
#             L = self.target.copy()
#             d, min_ol = ol.apply(L)
#             if d.number_crossings() < 3:
#                 bonus = 10000
#             else:
#                 bonus = 1
#             ccCount = min_ol.ccCount()
#             fitness = 1.0 + bonus/(d.number_crossings()**float(self.a) + ccCount**float(self.b) + ol.length()**float(self.c) + (ol.length() - min_ol.length())**float(self.d) + 1.0)
#             ol.setFitness(fitness)
#             return fitness
#         elif isinstance(ol.fitness, float):
#             return ol.fitness
#         else:
#             raise TypeError("Not sure what self.fitness is.")


class Fit(object):
    def __init__(self, a, b, c, d, target):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.target = target
    
    def __call__(self, ol):
        if ol.fitness == -float('inf'):
            L = self.target.copy()
            di, min_ol = ol.apply(L)
            ccCount = min_ol.ccCount()
            if di.number_crossings() < 3:
                bonus = 10000
                fitness = 1.0 + bonus/(di.number_crossings()**float(1) + ccCount**float(3) + ol.length()**float(0) + (ol.length() - min_ol.length())**float(2) + 1.0)
            else:
                bonus = 1
                fitness = 1.0 + bonus/(di.number_crossings()**float(2) + ccCount**float(1) + ol.length()**float(0) + (ol.length() - min_ol.length())**float(2) + 1.0)
            ol.setFitness(fitness)
            return fitness
        elif isinstance(ol.fitness, float):
            return ol.fitness
        else:
            raise TypeError("Not sure what self.fitness is.")