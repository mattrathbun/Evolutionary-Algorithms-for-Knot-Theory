import ADTLink

K = ADTLink.ADTLink([-6,10,12,-2,4,-8],[1,1,-1,1,1,1])
#print K.isrealisable()
#print K.to_list()
#print "\n"

for i in range(1,12):
    print i,K.right(i),K.doubleRight(i)

print "#############################################################"

K.R3(8,'r');
