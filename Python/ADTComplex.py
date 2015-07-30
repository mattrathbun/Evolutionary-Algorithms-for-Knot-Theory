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
        self.c2 = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_regs+1)]
        self.c3 = [[0 for j in range(4)] for i in range(self.n)]
        self.er = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_arcs+1)]
        self.c4 = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_arcs+1)]
        self.rm = [[0 for j in range(self.n_regs+1)] for i in range(self.n_regs+1)]
        self.kf = [[0 for j in range(self.n+1)] for i in range(self.n_regs+1)]
        self.op = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_regs+1)]
    
    def calc_incidence(self):
        self.calc_incidence_c2()
        self.calc_incidence_c3()
        self.calc_incidence_er()
        self.calc_incidence_c4()
        self.calc_incidence_rm()
        self.calc_incidence_kf()
        self.calc_incidence_op()
        
    # C2: Incidence matrix of regions to edges.
    # C2[i,j] says whether region i is incident to edge j.
    def calc_incidence_c2(self):
        adt = self.adt
        b1 = [[0 for j in range(2)] for i in range(self.n_arcs+1)]
        r = 0
        for i in range(1, self.n_arcs + 1):
            if b1[i][0] == 0:
                k = i
                r += 1
                self.c2[r][i-1] = 1
                b1[i][0] = 1
                dd = 1
                while adt.jump(adt.wrap(k+(dd+1)/2)) != i:
                    if dd == 1:
                        dd1 = adt.quad(adt.wrap(k+1))[3]
                        k = adt.wrap(adt.jump(adt.wrap(k+1)) + (dd1-1)/2)
                    else:
                        dd1 = -adt.quad(k)[3]
                        k = adt.wrap(adt.jump(k) + (dd1-1/2))
                    dd = dd1
                    self.c2[r][k] = 1
                    if dd == 1:
                        b1[k][0] = 1
                    else:
                        b1[k][1] = 1
        for i in range(1,self.n_arcs + 1):
            if b1[i][1] == 0:
                k = i
                dd = -1
                r += 1
                self.c2[r][i] = 1
                b1[i][1] = 1
                while adt.jump(adt.wrap(k+(dd+1)/2)) != adt.wrap(i+1):
                    if dd == 1:
                        dd1 = adt.quad(adt.wrap(k+1))[3]
                        k = adt.wrap(adt.jump(adt.wrap(k+1)) + (dd1-1)/2)
                    else:
                        dd1 = -adt.quad(k)[3]
                        k = adt.wrap(adt.jump(k) + (dd1-1/2))
                    dd = dd1
                    self.c2[r][k] = 1
                    if dd == 1:
                        b1[k][0] = 1
                    else:
                        b1[k][1] = 1
        return

    # C3: Incidence of regions to crossings.
    # C3[i,0-3] lists the regions around crossing i, clockwise.
    def calc_incidence_c3(self):
        adt = self.adt
        for i in range(1,self.n_regs+1):
            for j in range(1,self.n_arcs+1):
                if self.c2[i][j] == 1:
                    if self.c2[i][adt.wrap(adt.jump(j)-1)] == 1:
                        self.c3[j][0] = i
                    if self.c2[i][adt.jump(j)] == 1:
                        self.c3[j][1] = i
                if self.c2[i][adt.wrap(j-2)] == 1:
                    if self.c2[i][adt.jump(j)] == 1:
                        self.c3[j][2] = i
                    if self.c2[i][adt.wrap(adt.jump(j)-1)] == 1:
                        self.c3[j][3] = i
        return
    
    # ER: Incidence of edges to regions.
    # ER[i,j] = k if edges i and j are incident to region k. 
    def calc_incidence_er(self):
        for i in range(1,self.n_arcs):
            for j in range(i+1, self.n_arcs+1):
                for k in range(1,3):
                    reg1 = self.c3[i][k]
                    if self.c2[reg1][j] == 1:
                        self.er[i][j] = reg1
                        self.er[j][i] = reg1
        return

    # C4: Edges meeting at crossing.
    # C4[i,j] = 1 if edges i and j meet at a crossing.
    def calc_incidence_c4(self):
        adt = self.adt
        for i in range(1,self.n_arcs+1):
            self.c4[i][adt.jump(j)] = 1
            self.c4[i][adt.wrap(adt.jump(i)-1)] = 1
            self.c4[i][adt.jump(adt.wrap(i+1))] = 1
            self.c4[i][adt.wrap(adt.jump(adt.wrap(i+1))-1)] = 1
        return
    
    # RM: Edges shared by adjacent regions
    def calc_incidence_rm(self):
        adt = self.adt
        c3 = self.c3
        for i in range(1,self.n+1,2):
            self.rm[c3[i][1]][c3[i][2]] = i
            self.rm[c3[i][2]][c3[i][1]] = i
            self.rm[c3[i][2]][c3[i][3]] = adt.jump(i)
            self.rm[c3[i][3]][c3[i][2]] = adt.jump(i)
        return
    
    def calc_incidence_kf(self):
        adt = self.adt
        c3 = self.c3
        odd,even,sign,orient = adt.quad(i)
        for i in range(1,self.n_arcs+1):
            self.kf[c3[i][0]][i] = -orient * sign
            self.kf[c3[i][1]][i] = orient * sign
            self.kf[c3[i][2]][i] = -orient * sign
            self.kf[c3[i][3]][i] = orient * sign
        return
    
    def calc_incidence_op(self):
        for i in range(1,self.n_regs):
            for j in range(i+1,self.n_regs+1):
                if (self.rm[i][j] == 0):
                    self.op[i][rm[i][j]] = j
                    self.op[j][rm[i][j]] = i
        return
    
    def draw_graph(self):
        #pos = arf_layout(self.g)
        pos = graph_tool.draw.sfdp_layout(self.g, C=0.5, gamma=0.5)
        # pos = radial_tree_layout(self.g,0)
        # pos = fruchterman_reingold_layout(self.g)
        # pos = sfdp_layout(self.g)
        graph_tool.draw.graph_draw(self.g, pos=pos, vertex_text=self.g.vertex_index, vertex_color=self.wtype, vertex_fill_color=self.vtype)
        #graph_draw(self.g, pos=pos, vertex_text=self.g.vertex_index, vertex_fill_color=self.vtype, output="complex.png")
