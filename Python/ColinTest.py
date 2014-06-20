import ADTLink

K = ADTLink.ADTLink([-6,10,12,-2,4,-8],[1,1,-1,1,1,1])
#print K.isrealisable()
#print K.to_list()
#print "\n"

#for i in range(1,12):
#    print i,K.right(i),K.doubleRight(i)

print "#############################################################"

print K.to_list()
K.R3(8,'r')
print K.to_list()
## I think this example is off by a single sign.
## print "Should get ([-6, -8, 12, -2, 10, -4], [1, 1, -1, 1, 1, 1])."

print "#############################################################"

K = ADTLink.ADTLink([-6, -10, 12, -2, 4, -8], [1, -1, -1, 1, 1, 1])

print K.to_list()
K.R3(8, 'R')
print K.to_list()
print "Should get ([-6, -8, 12, -2, 10, 4], [1, 1, -1, 1, 1, -1])."

print "#############################################################"
