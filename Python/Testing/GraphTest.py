import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

from ADTLink import *
from graph_tool.all import *

g = Graph()
diags = []
edges = []
#diags.append(ADTLink([],[]))
diags.append(ADTLink([4,6,2],[1,1,1]))
#diags.append(ADTLink([4,6,8,2],[-1,1,-1,1]))
g.add_vertex()
maxlvl = 1

def find_diag(D):
    try:
        idx = diags.index(D)
        return idx
    except ValueError:
        return -1

def propagate(cur,lvl):
    if lvl > maxlvl:
        return
    print "propagate(%d,%d)" % (cur, lvl)
    v = g.vertex(cur)
    K = diags[cur]
    num_arcs = 2*K.number_crossings() if K.number_crossings() > 0 else 1
    # iterate through possible R1 moves

    for i in range(num_arcs):
        for j in ['L','R']:
            for k in [1,-1]:
                L = K.copy()
                if L.R1Up(i,j,k):
                    op = "R1Up(%d,%c,%d)" % (i,j,k)
                    print "    ", op
                    print "        ", L.to_string()
                    idx = find_diag(L)
                    # if we haven't seen this node yet:
                    if idx == -1:
                        #   add it to diags
                        diags.append(L)
                        idx = len(diags) - 1
                        g.add_vertex()
                    w = g.vertex(idx)
                    # make a new edge connecting this node to the new one
                    edgename = "%d R1Up(%d,%c,%d) %d" % (cur,i,j,k,idx)
                    if (edgename not in edges):
                        g.add_edge(v,w)
                        edges.append(edgename)
                    # propagate(newdiag,lvl+1)
                    propagate(idx,lvl+1)

    for i in range(num_arcs):
        L = K.copy()
        if L.number_crossings() > 0 and L.R1Down(i):
            op = "R1Down(%d)" % (i)
            print "    ", op
            print "        ", L.to_string()
            idx = find_diag(L)
            # if we haven't seen this node yet:
            if idx == -1:
                #   add it to diags
                diags.append(L)
                idx = len(diags) - 1
                g.add_vertex()
            w = g.vertex(idx)
            # make a new edge connecting this node to the new one
            edgename = "%d R1Down(%d) %d" % (cur,i,idx)
            if (edgename not in edges):
                g.add_edge(v,w)
                edges.append(edgename)
            # propagate(newdiag,lvl+1)
            propagate(idx,lvl+1)

propagate(0,0)

vbet = betweenness(g)[0]
#ebet = betweenness(g)[1]
#pos = sfdp_layout(g)
#pos = sfdp_layout(g, C=1.0, gamma=0.2)
#pos = fruchterman_reingold_layout(g)
#pos = arf_layout(g)
pos = radial_tree_layout(g,0)
#graph_draw(g, pos=pos, vertex_fill_color=vbet, output_size=(2000,2000), \
#           output="trefoil.png")
graph_draw(g, pos=pos, vertex_fill_color=vbet)
#graph_draw(g, vertex_fill_color=vbet)
#graphviz_draw(g, pos=pos)
