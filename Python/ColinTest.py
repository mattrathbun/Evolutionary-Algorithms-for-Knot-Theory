import ADTLink

K = ADTLink.ADTLink([-6,10,12,-2,4,-8],[1,1,-1,1,1,1])
#print K.isrealisable()
#print K.to_list()
#print "\n"

#for i in range(1,12):
#    print i,K.right(i),K.doubleRight(i)

print "#############################################################"
print "#### Colin's Original example"
print "#############################################################"

print K.to_list()
print" " 
K.R3(8,'r')
print" "
print "We get    ",K.to_list()
print "Should get ([-6, -8, 12, -2, 10, -4], [1, 1, -1, 1, 1, 1])."

print " "
print "#############################################################"
print "#### Matt's example with the orientation at 3/10 changed to -ve"
print "#############################################################"

K = ADTLink.ADTLink([-6, -10, 12, -2, -4, -8], [1, -1, -1, 1, 1, 1])

print K.to_list()
K.R3(8, 'R')
print "We get    ",K.to_list()
print "Should get ([-6, -8, 12, -2, 10, -4], [1, 1, -1, 1, 1, -1])."

print "#############################################################"
