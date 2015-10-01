fileName = "../../../../allDiagrams3"

allDiagramsSet = set()
counter = 0

with open(fileName) as f:
    for line in f:
         counter += 1
         if line not in allDiagramsSet:
             allDiagramsSet.update(line)
             
print "Out of {} lines in the file allDiagrams,".format(counter)
print "\n"
print "there are {} unique diagrams.".format(len(allDiagramsSet)) 