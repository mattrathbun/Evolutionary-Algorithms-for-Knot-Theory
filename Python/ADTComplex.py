from ADT import *
from graph_tool.all import *

class ADTComplex:
    def __init__(self, adt):
        self.adt = adt
        self.g = Graph(directed = False)
        self.n = adt.number_crossings()
        self.n_arcs = 2*self.n
        self.n_regs = self.n + 2
        
        self.init_incidence()
        self.calc_incidence()
    
    def init_incidence(self):
        self.c2 = [[0 for j in range(self.n_arcs)] for i in range(self.n_regs)]
        self.c3 = [[0 for j in range(4)] for i in range(self.n)]
        self.er = [[0 for j in range(self.n_arcs)] for i in range(self.n_arcs)]
        self.c4 = [[0 for j in range(self.n_arcs)] for i in range(self.n_arcs)]
        self.rm = [[0 for j in range(self.n_regs)] for i in range(self.n_regs)]
        self.kf = [[0 for j in range(self.n)] for i in range(self.n_regs)]
        self.op = [[0 for j in range(self.n_arcs)] for i in range(self.n_regs)]
    
    def calc_incidence(self):
        self.calc_incidence_c2()
        self.calc_incidence_c3()
        
    def calc_incidence_c2(self):
        adt = self.adt
        b1 = [[0 for j in range(2)] for i in range(self.n_arcs)]
        r = 0
        for i in range(1, self.n_arcs + 1):
            if b1[i-1][0] == 0:
                k = i
                r += 1
                self.c2[r-1][i-1] = 1
                b1[i-1][0] = 1
                dd = 1
                while adt.jump(adt.wrap(k+(dd+1)/2)) != i:
                    if dd == 1:
                        dd1 = adt.quad(adt.wrap(k+1))[3]
                        k = adt.wrap(adt.jump(adt.wrap(k+1)) + (dd1-1)/2)
                    else:
                        dd1 = -adt.quad(k)[3]
                        k = adt.wrap(adt.jump(k) + (dd1-1/2))
                    dd = dd1
                    self.c2[r-1][k-1] = 1
                    if dd == 1:
                        b1[k-1][0] = 1
                    else:
                        b1[k-1][1] = 1
        for i in range(1,self.n_arcs + 1):
            if b1[i-1][1] == 0:
                k = i
                dd = -1
                r += 1
                self.c2[r-1][i-1] = 1
                b1[i-1][1] = 1
                while adt.jump(adt.wrap(k+(dd+1)/2)) != adt.wrap(i+1):
                    if dd == 1:
                        dd1 = adt.quad(adt.wrap(k+1))[3]
                        k = adt.wrap(adt.jump(adt.wrap(k+1)) + (dd1-1)/2)
                    else:
                        dd1 = -adt.quad(k)[3]
                        k = adt.wrap(adt.jump(k) + (dd1-1/2))
                    dd = dd1
                    self.c2[r-1][k-1] = 1
                    if dd == 1:
                        b1[k-1][0] = 1
                    else:
                        b1[k-1][1] = 1
        return

    def calc_incidence_c3(self):
        adt = self.adt
        for i in range(1,self.n_regs+1):
            for j in range(1,self.n_arcs+1):
                if c2[i-1][j-1] == 1:
                    if c2[i-1][adt.wrap(adt.jump(j)-1)-1] == 1:
                        c3[j-1][0] = i
                    if c2[i-1][adt.jump(j)-1] == 1:
                        c3[j-1][1] = i
                if c2[i-1][adt.wrap(j-2)-1] == 1:
                    if c2[i-1][adt.jump(j)-1] == 1:
                        c3[j-1][2] = i
                    if c2[i-1][adt.wrap(adt.jump(j)-1)-1] == 1:
                        c3[j-1][3] = i
        return

    def draw_graph(self):
        #pos = arf_layout(self.g)
        pos = graph_tool.draw.sfdp_layout(self.g, C=0.5, gamma=0.5)
        # pos = radial_tree_layout(self.g,0)
        # pos = fruchterman_reingold_layout(self.g)
        # pos = sfdp_layout(self.g)
        graph_tool.draw.graph_draw(self.g, pos=pos, vertex_text=self.g.vertex_index, vertex_color=self.wtype, vertex_fill_color=self.vtype)
        #graph_draw(self.g, pos=pos, vertex_text=self.g.vertex_index, vertex_fill_color=self.vtype, output="complex.png")
