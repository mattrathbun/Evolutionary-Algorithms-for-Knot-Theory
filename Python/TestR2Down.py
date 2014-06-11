import ADTLink

K = ADTLink.ADTLink([6, -8, -10, 12, 4, 2], [-1, -1, -1, -1, 1, 1])
print "K is:"
print K.to_list()
print "\n"

# print "Performing R2DownPlus(4, 'l'):"
# print K.R2DownPlus(4, 'l')
# print K.to_list()
# print "\n"
print "Performing R2Down(4):"
print K.R2Down(4)
print K.to_list()
print "\n"

# print "Performing R2DownPlus(4, 'r'):"
# print K.R2DownPlus(4, 'r')
# print K.to_list()
# print "\n"
print "Performing R2Down(4):"
print K.R2Down(4)
print K.to_list()
print "\n"

# print "Now, performing R2DownPlus(2, 'l'):"
# print K.R2DownPlus(2, 'l')
# print K.to_list()
# print "\n"
print "Now, performing R2Down(2):"
print K.R2Down(2)
print K.to_list()
print "\n"

L = ADTLink.ADTLink([-12, 14, -16, -22, -20, -6, 2, -4, -18, -10, 8], [-1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1])
L1 = L.copy()
L2 = L.copy()
print "L_1 and L_2 are:"
print L.to_list()
print "\n"


# print "Performing R2DownPlus(1, 'l') to L_1:"
# print L1.R2DownPlus(1, 'l')
# print L1.to_list()
# print "\n"
print "Performing R2Down(1) to L_1:"
print L1.R2Down(1)
print L1.to_list()
print "\n"

# print "Performing R2DownPlus(12, 'r') to L_2:"
# print L2.R2DownPlus(12, 'r')
# print L2.to_list()
# print "\n"
print "Performing R2Down(12) to L_2:"
print L2.R2Down(12)
print L2.to_list()
print "\n"

print "Are L_1 and L_2 equal after these moves?"
print L1 == L2
print "\n"

# print "L is {}".format(L.to_list())
# print "Performing R2DownPlus(10, 'l')"
# print L.R2DownPlus(10, 'l')
# print L.to_list()
# print "\n"
print "L is {}".format(L.to_list())
print "Performing R2Down(10)"
print L.R2Down(10)
print L.to_list()
print "\n"

# print "Performing R2DownPlus(9, 'l')"
# print L.R2DownPlus(9, 'l')
# print L.to_list()
# print "\n"
print "Performing R2Down(9)"
print L.R2Down(9)
print L.to_list()
print "\n"

# for i in range(1, 22):
# 	Ltest = L.copy()
# 	if Ltest.R2DownPlus(i, 'l'):
# 		print "{} on the left".format(i)
for i in range(1, 22):
	Ltest = L.copy()
	if Ltest.R2Down(i):
		print "{}".format(i)

# for i in range(1, 22):
# 	Ltest = L.copy()
# 	if Ltest.R2DownPlus(i, 'r'):
# 		print "{} on the right".format(i)
# print "\n"
		
M = ADTLink.ADTLink([2, -4], [1, -1])
print "M is:"
print M.to_list()
print "\n"

# print "Performing R2DownPlus(4, 'l')"
# print M.R2DownPlus(4, 'l')
# print M.to_list()
# print "\n"
print "Performing R2Down(4)"
print M.R2Down(4)
print M.to_list()
print "\n"

N = ADTLink.ADTLink([6, 4, -8, -2], [-1, -1, 1, 1])
print "N is:"
print N.to_list()
print "\n"

# print "Performing R2DownPlus(8, 'l')"
# print N.R2DownPlus(8, 'l')
# print N.to_list()
# print "\n"
print "Performing R2Down(8)"
print N.R2Down(8)
print N.to_list()
print "\n"

K = ADTLink.ADTLink([6, -8, 2, 4], [1, 1, 1, -1])
print "K is:"
print K.to_list()
print "\n"

# print "Performing R2DownPlus(7, 'l')"
# print K.R2DownPlus(7, 'l')
# print K.to_list()
# print "\n"
print "Performing R2Down(7)"
print K.R2Down(7)
print K.to_list()
print "\n"

K = ADTLink.ADTLink([4, -6, -8, -2], [1, 1, -1, 1])
print "K is:"
print K.to_list()
print "\n"

# print "Performing R2DownPlus(4, 'l')"
# print K.R2DownPlus(4, 'l')
# print K.to_list()
# print "\n"
print "Performing R2Down(4)"
print K.R2Down(4)
print K.to_list()
print "\n"

K = ADTLink.ADTLink([6, 8, -2, 4], [-1, 1, 1, 1])
print "K is:"
print K.to_list()
print "\n"

# print "Performing R2DownPlus(1, 'l')"
# print K.R2DownPlus(1, 'l')
# print K.to_list()
# print "\n"
print "Performing R2Down(1)"
print K.R2Down(1)
print K.to_list()
print "\n"

K = ADTLink.ADTLink([-4, 6, -8, -2], [1, 1, 1, -1])
print "K is:"
print K.to_list()
print "\n"

# print "Performing R2DownPlus(6, 'l')"
# print K.R2DownPlus(6, 'l')
# print K.to_list()
# print "\n"
print "Performing R2Down(6)"
print K.R2Down(6)
print K.to_list()
print "\n"


