import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from ADT import *

K = ADT([4,6,8,2],[0,0,0,0])
K.orient(1)
print "K %s realisable." % ("is" if K.isrealisable() else "isn't")
