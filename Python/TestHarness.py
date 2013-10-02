# this is a place to mess around with creating objects etc.

# okay, so in Python we can just write a sequence of commands
# not like java where we have to wrap all this up in a class 

import Braid
import Population
from random import *
import numpy

print("test harness")
braidInput = [1,2,5,4,6,3,2,1]
b = Braid.Braid([1,2,5,4,3,2,1])
b.print_it();

# p = Population.Population(20,15,10)

# test

######################################################################
# the following is colin trying to understand how random numbers and
# function application works

longlist = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
for i in range(0,10):
    print(choice(longlist));

print(sample(longlist,3))

print(map(lambda x:x*x, longlist))
print(numpy.argmax(longlist))



