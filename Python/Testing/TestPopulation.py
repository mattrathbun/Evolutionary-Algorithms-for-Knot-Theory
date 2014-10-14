import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import Population

pop = Population.Population(10,10,5)

ol = pop.toList()
for l in ol:
    print [op.toString() for op in l.toList()]

