import ADTLink
#K = ADTLink.ADTLink([4, 6, 8, 2], [-1, 1, -1, 1])
#for i in range(1, 9):
#	print "i = {}".format(i)
#	print K.R2Candidates(i, 'r')

K = ADTLink.ADTLink([-8, -14, 12, -2, -10, -4, 6], [-1, 1, -1, -1, -1, 1, -1])
#print K.R2Candidates(9, 'l')
#print K.R2Candidates(9, 'r')
print "arc = 10, side = r"
#print K.R2Candidates(10, 'r') 
print K.regions(10, 'r')

print "arc = 1, side = l"
#print K.R2Candidates(1, 'l')
print K.regions(1, 'l')

print "arc = 9, side = l"
#print K.R2Candidates(9, 'l')
print K.regions(9, 'l')

print "arc = 9, side = r"
#print K.R2Candidates(9, 'r')
print K.regions(9, 'r')

print "arc = 8, side = l"
#print K.R2Candidates(8, 'l')
print K.regions(8, 'l')

print "arc = 8, side = r"
#print K.R2Candidates(8, 'r')
print K.regions(8, 'r')

print "arc = 4, side = l"
#print K.R2Candidates(4, 'l')
print K.regions(4, 'l')

print "arc = 4, side = r"
#print K.R2Candidates(4, 'r')
print K.regions(4, 'r')

print "arc = 11, side = l"
#print K.R2Candidates(11, 'l')
print K.regions(11, 'l')

print "arc = 13, side = r"
#print K.R2Candidates(13, 'r')
print K.regions(13, 'r')

print "arc = 14, side = l"
#print K.R2Candidates(14, 'l')
print K.regions(14, 'l')

print "arc = 14, side = r"
#print K.R2Candidates(14, 'r')
print K.regions(14, 'r')