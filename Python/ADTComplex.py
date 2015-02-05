from ADT import *
from graph_tool.all import *

class ADTComplex:
    def __init__(self, adt):
        self.adt = adt
        self.g = Graph(directed = False)
        self.nodes = []
        self.edges = []
        self.faces = []
        self.regions = []
        self.vtype = self.g.new_vertex_property("int")
        self.n = adt.number_crossings()
        n = self.n

        # Add nodes corresponding to crossings
        for i in range(n):
            self.nodes.append([i])
            self.g.add_vertex()
            self.vtype[self.g.vertex(i)] = 0
            
        # Add nodes corresponding to arcs
        for i in range(n):
            odd, even, sign, orient = adt.quad(2*i+1)
            
            odd2, even2, sign2, orient2 = adt.quad(adt.wrap(odd+1))
            el = [i, (odd2-1)/2]
            el.sort()
            self.nodes.append(el)
            self.edges.append(el)
            self.g.add_vertex()
            e = self.g.vertex(n+2*i)
            v = self.g.vertex(i)
            w = self.g.vertex((odd2-1)/2)
            self.vtype[e] = 1
            self.g.add_edge(v,e)
            self.g.add_edge(e,w)
            
            odd3, even3, sign3, orient3 = adt.quad(adt.wrap(even+1))
            el = [i,(odd3-1)/2]
            el.sort()
            self.nodes.append(el)
            self.edges.append(el)
            self.g.add_vertex()
            e = self.g.vertex(n+2*i+1)
            v = self.g.vertex(i)
            w = self.g.vertex((odd3-1)/2)
            self.vtype[e] = 1
            self.g.add_edge(v,e)
            self.g.add_edge(e,w)

        print "edges: ", self.edges
        # Add nodes corresponding to regions
        for i in range(n):
            odd, even, sign, orient = adt.quad(2*i+1)
            for side in ["L", "R"]:
                reg = adt.regions(odd,side)
                regv = list(set([self.node_index(arc) for r in reg for arc in r]))
                regv.sort()
                if regv not in self.regions:
                    self.regions.append(regv)
        print "regions: ", self.regions

        for r in self.regions:
            rn = self.g.add_vertex()
            rv = self.g.vertex(rn)
            self.vtype[rv] = 2
            for i in r:
                v = self.g.vertex(i)
                self.g.add_edge(v,rv)
            if len(r) == 2:
                for i in range(len(r)-1):
                    re = [r[i],r[(i+1)%len(r)]]
                    re.sort()
                    print "  edge %s in region %s" % (str(re),str(r))
                    el = [idx for idx,val in enumerate(self.nodes) if val == re]
                    print "  nodes: %s" % (str(el))
                    print "  region %s is bigon" % (str(r))
                    for j in el:
                        w = self.g.vertex(j)
                        self.g.add_edge(rv,w)
                        print "    edge %s -- %s (%d -- %d)" % (str(r), str(re), rn, j)
            else:
                for i in range(len(r)):
                    re = [r[i],r[(i+1)%len(r)]]
                    re.sort()
                    print "  edge %s in region %s" % (str(re),str(r))
                    el = [idx for idx,val in enumerate(self.nodes) if val == re]
                    print "  nodes: %s" % (str(el))
                    print "    region %s is polygon or loop" % (str(r))
                    w = self.g.vertex(el[0])
                    self.g.add_edge(rv,w)
                    print "    edge %s -- %s (%d -- %d)" % (str(r), str(re), rn, el[0])  
                
                
            

        # Add nodes corresponding to regions
        #for i in range(n):
        #    odd, even, sign, orient = adt.quad(2*i+1)
        #    for side in ['L', 'R']:
        #        ri = self.g.add_vertex()
        #        rv = self.g.vertex(ri)
        #        regs = adt.regions(odd,side)
        #        regvs = list(set([self.node_index(arc) for reg in regs for arc in reg]))
        #        for xi in regvs:
        #            xv = self.g.vertex(xi)
        #            if rv not in xv.all_neighbours():
        #                print "edge (%2d,%2d)" % (xi, ri)
        #                self.g.add_edge(xv,rv)
        
    def node_index(self,i):
        odd = self.adt.quad(i)[0]
        return (odd-1)/2

     
    def draw_graph(self):
        pos = arf_layout(self.g)
        pos = sfdp_layout(self.g, C=0.5, gamma=0.5)
        # pos = radial_tree_layout(self.g,0)
        # pos = fruchterman_reingold_layout(self.g)
        # pos = sfdp_layout(self.g)
        graph_draw(self.g, pos=pos, vertex_text=self.g.vertex_index, vertex_fill_color=self.vtype)
        graph_draw(self.g, pos=pos, vertex_text=self.g.vertex_index, vertex_fill_color=self.vtype, output="complex.png")

