import os, sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
import ADT, ADTOp, ADTOpPopulation, ADTOpPopulationSets, Fit
import AllDiagrams
from datetime import datetime
import random

AllDiagrams.init()

storageFile = "Fronds"

def fetchDownMoves(knot):
    all_possible_moves = knot.finePossibleMoves()
    return [move for move in all_possible_moves if move.direction in ["D"]]

def fetchUpMoves(knot):
    all_possible_moves = knot.finePossibleMoves()
    return [move for move in all_possible_moves if move.direction in ["U"]]
    
def fetchDownHorizontalMoves(knot):
    all_possible_moves = knot.finePossibleMoves()
    return [move for move in all_possible_moves if move.direction in ["D", "H"]]

def fetchDownHorizontalUpMoves(knot):
    all_possible_moves = knot.finePossibleMoves()
    return [move for move in all_possible_moves if move.direction in ["D", "H", "U"]]
    
def resultDownMoves(knot):
    all_possible_down_moves = fetchDownMoves(knot)
    results = []
    for move in all_possible_down_moves:
        K = knot.copy()
        if move.apply(K):
            results.append(K)
    return results

def resultUpMoves(knot):
    all_possible_up_moves = fetchUpMoves(knot)
    results = []
    for move in all_possible_up_moves:
        K = knot.copy()
        if move.apply(K):
            results.append(K)
    return results
    
def resultDownHorizontalMoves(knot):
    all_possible_down_or_horizontal_moves = fetchDownHorizontalMoves(knot)
    results = []
    for move in all_possible_down_or_horizontal_moves:
        K = knot.copy()
        if move.apply(K):
            results.append(K)
    return results

def resultDownHorizontalUpMoves(knot):
    all_possible_down_or_horizontal_or_up_moves = fetchDownHorizontalUpMoves(knot)
    results = []
    for move in all_possible_down_or_horizontal_or_up_moves:
        K = knot.copy()
        if move.apply(K):
            results.append(K)
    return results

def frond(knot, depth=1):
    if fetchDownMoves(knot) != []:
        print "This is not a leaf."
        return
    else:
        explored = set()
        exploring = [(knot, 0, True)] ## [diagram, depth_counter, leaf or not]
        for diagram in exploring:
            print "Explored is currently: \n"
            print explored
            print "\n"
            print "Exploring is currently: \n"
            print exploring
            print "\n"
            down_or_horizontal_adjacent = resultDownHorizontalMoves(diagram[0])
            for d in down_or_horizontal_adjacent:
                l = len(fetchDownMoves(d))
                if l == 0:
                    if (d.to_string(), diagram[1], True) not in explored:
                        exploring.append((d, diagram[1], True))
                else:
                    if (d.to_string(), diagram[1], False) not in explored:
                        exploring.append((d, diagram[1], False))
            if diagram[1] < depth:
                up_adjacent = resultUpMoves(diagram[0])
                for d in up_adjacent:
                    if (d.to_string(), diagram[1] + 1, False) not in explored:
                        exploring.append((d, diagram[1] + 1, False))
            (a, b, c) = exploring.pop(0)
            explored.add((a.to_string(), b, c))
        print "There are {} diagrams in the frond.\n".format(len(explored))
        leaves = set()
        for item in explored:
            print item[0]
            if item[2]:
                leaves.append(item)
        print "There are {} leaves in the frond.\n".format(len(leaves))
        for leaf in leaves:
            print leaf[0]
            print len(leaf[0])*2
            print "\n"
        return explored, leaves
    
    
                
                
                
                
        