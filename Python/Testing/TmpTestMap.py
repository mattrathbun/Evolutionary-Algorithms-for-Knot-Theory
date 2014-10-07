L = [1,-2,3,4,5,6,-7,8,9,10]
L3 = [2,3]

rewrite = {}

rewrite.update({2:12})
rewrite.update({3:13})

print rewrite
L2 = map(lambda x:(rewrite[x] if x in rewrite else x) if x > 0 else (-rewrite[-x] if -x in rewrite else x), L)
print L2


print range(1,2*6,2)
