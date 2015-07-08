import ADT, ADTOp, ADTOpList

numberOfExamples = 20
distanceLimit = 10
knots = [set() for _ in xrange(distanceLimit+1)]

for e in range(1,numberOfExamples):
    # print "**** example ",e
    k = ADT.ADT([],[])
    # print k.to_string()
    knots[0].add(k.copy())
    distance = 1
    while distance <= distanceLimit:
        move = ADTOp.simpleCoarseRandomOp() #use default parameters
        if move.apply(k):
            # print k.to_string()
            knots[distance].add(k.copy())
            distance = distance + 1

i = 0
for s in knots:
    print "***** set number ",i
    for k in s:
        print k.to_string()
    i = i+1
