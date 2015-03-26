from ADT import *
from graph_tool.all import *

class ADTComplex:
    def __init__(self, adt):
        self.adt = adt
        self.g = Graph(directed = False)
        self.crossings = []
        self.arcs = []
        self.regions = []
        self.vtype = self.g.new_vertex_property("int")
        self.wtype = self.g.new_vertex_property("int")
        self.n = adt.number_crossings()

        self.init_crossings()
        self.init_arcs()
        self.init_regions()
    
    def init_crossings(self):
        for i in range(self.n):
            self.crossings.append([i])
            self.g.add_vertex()
            self.vtype[self.g.vertex(i)] = 0
        # print "crossings: ", self.crossings
            
    def init_arcs(self):
        for i in range(1, 2*self.n + 1):
            odd1, even1, sign1, orient1 = self.adt.quad(i)
            odd2, even2, sign2, orient2 = self.adt.quad(self.adt.wrap(i+1))
            #el = sorted([(odd1-1)/2, (odd2-1)/2])
            self.arcs.append([i,self.adt.wrap(i+1)])
            e = self.g.vertex(self.g.add_vertex())
            v = self.g.vertex((odd1-1)/2)
            w = self.g.vertex((odd2-1)/2)
            self.vtype[e] = 1
            self.g.add_edge(v,e)
            self.g.add_edge(e,w)
        # print "arcs: ", self.arcs
    
    def init_regions(self):
        for i in range(1,2*self.n+1):
            for s in ['L','R']:
                t0 = self.adt.regions(i,s)
                rnames = self.region_names(i,s)
                if rnames not in self.regions:
                    self.regions.append(rnames)
        # print "regions: ", self.regions
        for reg in self.regions:
            if [2*self.n,'L'] in reg:
                continue
            ri = self.g.add_vertex()
            rv = self.g.vertex(ri)
            self.vtype[rv] = 2
            # print "  new region node: %d" % (rv)
            rp = reg[0]
            # print "  rp = ", rp
            # print "  regions = ", self.adt.regions(rp[0],rp[1])
            for reg2 in self.adt.regions(rp[0],rp[1]):
                # print "    arc = ", reg2
                odd0, even0, sign0, orient0 = self.adt.quad(reg2[0])
                vi = (odd0-1)/2
                d = reg2[1] - reg2[0]
                if (d == 1 or d < -1):
                    ei = reg2[0] + self.n - 1
                elif (d == -1 or d > 1):
                    ei = reg2[1] + self.n - 1
                # print "      vr edge = [%d,%d]" % (vi,ri)
                # print "      er edge = [%d=%d,%d]" % (ei,fi,ri)
                v = self.g.vertex(vi)
                e = self.g.vertex(ei)
                self.g.add_edge(v,rv)
                self.g.add_edge(e,rv)         

    def region_names(self,n,s):
        regs = self.adt.regions(n,s)
        rnames = []
        for arc in regs:
            if arc[1] == self.adt.wrap(arc[0]+1):
                rnames.append([arc[0],s])
            else:
                t = 'L' if s == 'R' else 'R'
                rnames.append([arc[1],t])
        return sorted(rnames)
   
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
