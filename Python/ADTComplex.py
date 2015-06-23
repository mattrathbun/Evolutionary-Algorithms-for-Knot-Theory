from ADT import *
from graph_tool.all import *

class ADTComplex:
    def __init__(self, adt):
        self.adt = adt
        self.g = Graph(directed = False)
        self.crossings = []
        self.arcs = []
        self.regions = []
        self.flowers = []
        self.vtype = self.g.new_vertex_property("int")
        self.wtype = self.g.new_vertex_property("int")
        self.n = adt.number_crossings()

        self.init_crossings()
        self.init_arcs()
        self.init_regions()
        self.init_flowers()
    
    def init_crossings(self):
        for i in range(self.n):
            self.crossings.append([i])
            self.g.add_vertex()
            self.vtype[self.g.vertex(i)] = 0
            
    def init_arcs(self):
        for i in range(1, 2*self.n + 1):
            odd1, even1, sign1, orient1 = self.adt.quad(i)
            odd2, even2, sign2, orient2 = self.adt.quad(self.adt.wrap(i+1))
            self.arcs.append([i,self.adt.wrap(i+1)])
            e = self.g.vertex(self.g.add_vertex())
            v = self.g.vertex((odd1-1)/2)
            w = self.g.vertex((odd2-1)/2)
            self.vtype[e] = 1
            self.g.add_edge(v,e)
            self.g.add_edge(e,w)
    
    def init_regions(self):
        for i in range(1,2*self.n+1):
            for s in ['L','R']:
                t0 = self.adt.regions(i,s)
                rnames = self.region_names(i,s)
                if rnames not in self.regions:
                    self.regions.append(rnames)
        for reg in self.regions:
            if [2*self.n,'L'] in reg:
                rp = reg[0]
                for reg2 in self.adt.regions(rp[0],rp[1]):
                    odd0, even0, sign0, orient0 = self.adt.quad(reg2[0])
                    vi = (odd0-1)/2
                    d = reg2[1] - reg2[0]
                    if (d == 1 or d < -1):
                        ei = reg2[0] + self.n - 1
                    elif (d == -1 or d > 1):
                        ei = reg2[1] + self.n - 1
                    v = self.g.vertex(vi)
                    e = self.g.vertex(ei)
                    self.wtype[v] = 1
                    self.wtype[e] = 1
            else:
                ri = self.g.add_vertex()
                rv = self.g.vertex(ri)
                self.vtype[rv] = 2
                self.wtype[rv] = 2
                rp = reg[0]
                for reg2 in self.adt.regions(rp[0], rp[1]):
                    odd0, even0, sign0, orient0 = self.adt.quad(reg2[0])
                    vi = (odd0 - 1) / 2
                    d = reg2[1] - reg2[0]
                    if (d == 1 or d < -1):
                        ei = reg2[0] + self.n - 1
                    elif (d == -1 or d > 1):
                        ei = reg2[1] + self.n - 1
                    v = self.g.vertex(vi)
                    e = self.g.vertex(ei)
                    self.g.add_edge(v, rv)
                    if self.wtype[v] != 1:
                        self.wtype[v] = 2
                    self.g.add_edge(e, rv)
                    if self.wtype[e] != 1:
                        self.wtype[e] = 2         

    def init_flowers(self):
        print "init_flowers"
        for v in self.g.vertices():
            print "vertex", v, self.vtype[v], self.wtype[v]
            if self.vtype[v] == 0:
                self.init_flower_crossing(v)
            elif self.vtype[v] == 1:
                self.init_flower_arc(v)
            elif self.vtype[v] == 2:
                self.init_flower_region(v)
        return

    def init_flower_crossing(self,v):
        if self.wtype[v] == 1:
            self.init_flower_crossing_boundary(v)
        else:
            self.init_flower_crossing_interior(v)

    def init_flower_crossing_interior(self,v):
        flower = []
        vi = int(v)
        n = self.n
        odd, even, sign, orient = self.adt.quad(2*vi+1)
        over,under = ((odd,even) if sign == 1 else (even,odd))
        #under = (even if sign == 1 else odd)
        if (orient == 1):
            flower.append(n + over - 1)
            flower.append(n + self.adt.wrap(under - 1) - 1)
            flower.append(n + self.adt.wrap(over - 1) - 1)
            flower.append(n + under - 1)
        else:
            flower.append(n + over - 1)
            flower.append(n + under - 1)
            flower.append(n + self.adt.wrap(over - 1) - 1)
            flower.append(n + self.adt.wrap(under - 1) - 1)
        print "flower_crossing_interior", vi, flower
        return
    
    def init_flower_crossing_boundary(self,v):
        return
    
    def init_flower_arc(self,v):
        return
    
    def init_flower_region(self,v):
        return

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
    
    def vertex_index(self,i):
        i = self.adt.wrap(i)
        odd, even, sign, orient = self.adt.quad(i)
        return (odd-1)/2
     
    def draw_graph(self):
        #pos = arf_layout(self.g)
        pos = graph_tool.draw.sfdp_layout(self.g, C=0.5, gamma=0.5)
        # pos = radial_tree_layout(self.g,0)
        # pos = fruchterman_reingold_layout(self.g)
        # pos = sfdp_layout(self.g)
        graph_tool.draw.graph_draw(self.g, pos=pos, vertex_text=self.g.vertex_index, vertex_color=self.wtype, vertex_fill_color=self.vtype)
        #graph_draw(self.g, pos=pos, vertex_text=self.g.vertex_index, vertex_fill_color=self.vtype, output="complex.png")
