from DTLink import *

dt = DTLink([4,6,2]) # Trefoil
#dt = DTLink([6,8,2,4]) # Figure-8 knot
n = dt.number_crossings()

# Test R1 moves
for i in range(2*n):
  dt1 = dt.copy()
  dt1.R1UpPlus(i+1)
  #dt1.R1UpMinus(i+1)
  for j in range(2*n+1):
    dt2 = dt1.copy()
    if dt2.R1DownPlus(j+1):
    #if dt2.R1DownMinus(j+1):
      print "%s -(%d)-> %s -(%d)-> %s (%s)." % (dt.to_string(),
	  i+1, dt1.to_string(), j+1, dt2.to_string(),
	  dt == dt2)
  print ""
