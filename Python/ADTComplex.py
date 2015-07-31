from ADT import *
from graph_tool.all import *

class ADTComplex:
    def __init__(self, adt):
        self.adt = adt
        self.g = Graph(directed = False)
        self.n = adt.number_crossings()
        self.n_arcs = 2*self.n
        self.n_regs = self.n + 2
        self.inf_reg = 0
        
        self.init_incidence()
        self.calc_incidence()
        self.init_neighbours()
        self.calc_neighbours()
    
    def init_incidence(self):
        self.c2 = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_regs+1)]
        self.c3 = [[0 for j in range(4)] for i in range(self.n)]
        self.er = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_arcs+1)]
        self.c4 = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_arcs+1)]
        self.rm = [[0 for j in range(self.n_regs+1)] for i in range(self.n_regs+1)]
        self.kf = [[0 for j in range(self.n+1)] for i in range(self.n_regs+1)]
        self.opp = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_regs+1)]
    
    def calc_incidence(self):
        self.calc_incidence_c2()
        self.calc_incidence_c3()
        self.calc_incidence_er()
        self.calc_incidence_c4()
        self.calc_incidence_rm()
        self.calc_incidence_kf()
        self.calc_incidence_opp()
        
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
    
    def calc_incidence_opp(self):
        for i in range(1,self.n_regs):
            for j in range(i+1,self.n_regs+1):
                if (self.rm[i][j] == 0):
                    self.opp[i][rm[i][j]] = j
                    self.opp[j][rm[i][j]] = i
        return
    
    def init_neighbours(self):
        self.done = [0 for i in range(2*self.n+1)]
        self.ccr = [[0] for i in range(self.n_regs+1)]
        self.rot1 = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_regs+1)]
        self.rot2 = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_regs+1)]
        self.newreg = [0 for i in range(self.n_regs + 1)]
        self.nb = [[0] for i in range(self.n+1)]
        return
    
    def eb(self,i,j):
        if j == 1:
            return self.adt.wrap(i+1)
        elif j == -1:
            return i
        else:
            raise TypeError("Unexpected sign: %d" % j)
    
    def be(self,i,j):
        if j == 1:
            return i
        elif j == -1:
            return self.adt.wrap(i-1)
        else:
            raise TypeError("Unexpected sign: %d" % j)
    
    def vertex_index(self,i):
        return (self.adt.quad(i)[0] + 1)/2
    
    def sign(self,i):
        return self.adt.quad(i)[2]
    
    def orient(self,i):
        return self.adt.quad(i)[3]
    
    def calc_neighbours(self):
        self.calc_neighbours_ccr()
        self.calc_neighbours_rot()
        self.calc_infinite_region()
        self.renumber_regions()
        self.calc_neighbours_nb()
        return
    
    def calc_neighbours_ccr(self):
        c2 = self.c2
        kf = self.kf
        adt = self.adt
        for reg in range(1,self.n_regs+1):
            cedge = 0
            while (c2[reg][cedge] == 0):
                cedge += 1
            fedge = cedge
            self.ccr[reg].append(cedge)
            dir = self.sign(cedge) * kf[reg][cedge]
            while True:
                node = self.eb(cedge,dir)
                if (c2[reg][adt.jump(node)] == 1):
                    cedge = adt.jump(node)
                else:
                    cedge = adt.wrap(adt.jump(node) - 1)
                self.ccr[reg].append(cedge)
                dir = self.sign(cedge) * kf[reg][cedge]
                if (cedge == fedge):
                    break
            self.ccr[reg][0] = length(self.ccr[reg]) - 1
        return
    
    def calc_neighbours_rot(self):
        ccr = self.ccr
        for reg in range(1,self.n_regs+1):
            for i in range(1,ccr[reg][0]+1):
                edge1 = ccr[reg][i]
                edge2 = ccr[reg][i+1]
                rot1[reg][edge1] = edge2
                rot2[reg][edge2] = edge1
        return
    
    def calc_infinite_region(self):
        nedge = 2
        ccr = self.ccr
        for reg in range(1,self.n_regs+1):
            if (ccr[reg][0] > nedge):
                self.inf_reg = reg
                nedge = ccr[reg][0]
    
    def renumber_regions(self):
        t = 0
        ccr = self.ccr
        for reg in range(1,self.n_regs+1):
            if reg != self.inf_reg and ccr[reg][0] != 2:
                t += 1
                self.newreg[reg] = t
        self.n_nodes = 3 * self.n + t + ccr[self.inf_reg][0]
        self.n_intnodes = 3 * self.n + t
        for reg in range(1,self.n_regs+1):
            if ccr[reg][0] == 2:
                self.twoedge[ccr[reg][1]] = reg
                self.twoedge[ccr[reg][2]] = reg
        return
    
    def calc_neighbours_nb(self):
        ccr = self.ccr
        inf = self.inf_reg
        kf = self.kf
        rot1 = self.rot1
        rot2 = self.rot2
        opp = self.opp
        c2 = self.c2
        ivertex = [0]
        done = self.done
        nb = self.nb
        n = self.n
        n_intnodes = self.n_intnodes
        n_arcs = self.n_arcs
        adt = self.adt
        newreg = self.newreg
        
        nedge = ccr[inf][0]
        for i in range(1,nedge+1):
            cedge = ccr[inf][i]
            dir = self.sign(cedge) * kf[inf][cedge]
            prevedge = rot2[inf][cedge]
            prevdir = self.sign(prevedge) * kf[inf][prevedge]
            cb = self.eb(cedge,-dir)
            ivertex.append(self.vertex_index(cb))
            node = self.vertex_index(cb)
            done[node] = 1
            
            nb[node][0] = [5,0,0,0,0,0]
            nb[node][1] = n + cedge
            nb[node][2] = n + adt.wrap(prevedge + prevdir)
            nb[node][3] = n + self.be(cb,-dir)
            nb[node][4] = n + prevedge
            nb[node][5] = n_intnodes + i
        
        for i in range(1,nedge+1):
            cedge = ccr[inf][i]
            node = n + cedge
            done[node] = 1
            dir = self.sign(cedge) * kf[inf][cedge]
            reg2 = opp[inf][cedge]
            if i == nedge:
                nbleft = n_intnodes + 1
            else:
                nbleft = n_intnodes + i + 1
            
            if ccr[reg2][0] == 2:
                nb[node] = [5,0,0,0,0,0]
                nb[node][1] = nbleft
                nb[node][3-dir] = self.vertex_index(adt.wrap(cedge+1))
                nb[node][3] = n + rot1[reg2][cedge]
                nb[node][3+dir] = self.vertex_index(cedge)
                nb[node][5] = n_intnodes + i
            else:
                nb[node] = [7,0,0,0,0,0,0,0]
                nb[node][1] = nbleft
                nb[node][4-2*dir] = self.vertex_index(adt.wrap(cedge+1))
                nb[node][3] = n + rot2[reg2][cedge]
                nb[node][4] = 3 * n + newreg[reg2]
                nb[node][5] = n + rot1[reg2][cedge]
                nb[node][4+2*dir] = self.vertex_index(cedge)
                nb[node][7] = n_intnodes + i
                
        for i in range(1,nedge+1):
            node = n_intnodes + i
            previdx = (nedge if i == 1 else i - 1)
            nextidx = (1 if i == nedge else i + 1)
            
            nb[node] = [5,0,0,0,0,0]
            nb[node][1] = n_intnodes + nextidx
            nb[node][2] = n + ccr[inf][i]
            nb[node][3] = ivertex[i]
            nb[node][4] = n + ccr[inf][previdx]
            nb[node][5] = n_intnodes + previdx
        
        for i in range(1,n+1,2):
            if done[self.vertex_index(i)] == 0:
                node = self.vertex_index(i)
                nb[node] = [4,0,0,0,0]
                nb[node][1] = n + i
                nb[node][3+self.orient(i)] = n + adt.jump(i)
                nb[node][3] = n + adt.wrap(i-1)
                nb[node][3-self.orient(i)] = n + adt.wrap(adt.jump(i) - 1)
        
        for cedge in range(1,n_arcs + 1):
            node = n + cedge
            if done[node] == 0:
                reg1 = 0
                while c2[reg1][cedge] == 0:
                    reg1 += 1
                reg2 = opp[reg1][cedge]
                
                if ccr[reg1][0] == 2:
                    reg1,reg2 = reg2,reg1
                dir = self.sign(cedge) * kf[reg1][cedge]
                
                if ccr[reg2][0] == 2:
                    nb[node] = [6,0,0,0,0,0,0]
                    nb[node][1] = n + rot1[reg1][cedge]
                    nb[node][3-dir] = self.vertex_index(adt.wrap(cedge+1))
                    nb[node][3] = n + rot2[reg2][cedge]
                    nb[node][3+dir] = self.vertex_index(cedge)
                    nb[node][5] = n + rot2[reg1][cedge]
                    nb[node][6] = 3 * n + newreg[reg1]
                else:
                    nb[node] = [8,0,0,0,0,0,0,0,0]
                    nb[node][1] = n + rot1[reg1][cedge]
                    nb[node][4-2*dir] = self.vertex_index(adt.wrap(cedge+1))
                    nb[node][3] = n + rot2[reg2][cedge]
                    nb[node][4] = 3 * n + newreg[reg2]
                    nb[node][5] = n + rot1[reg2][cedge]
                    nb[node][4+2*dir] = self.vertex(cedge)
                    nb[node][7] = n + rot2[reg1][cedge]
                    nb[node][8] = 3 * n + newreg[reg1]
        
        for reg in range(1,n_regs + 1):
            if reg != inf and ccr[reg][0] != 2:
                node = 3 * n + newreg[reg]
                nedge = ccr[reg][0]
                nb[node][0] = nedge
                for i in range(1,nedge+1):
                    nb[node][nedge+1-i] = n + ccr[reg][i]
        for i in range(1,n_nodes+1):
            valence = nb[i][0]
            if nb[i][valence+1] == 0:
                nb[i][valence+1] = nb[i][1]
        return
    
    def draw_graph(self):
        #pos = arf_layout(self.g)
        pos = graph_tool.draw.sfdp_layout(self.g, C=0.5, gamma=0.5)
        # pos = radial_tree_layout(self.g,0)
        # pos = fruchterman_reingold_layout(self.g)
        # pos = sfdp_layout(self.g)
        graph_tool.draw.graph_draw(self.g, pos=pos, vertex_text=self.g.vertex_index, vertex_color=self.wtype, vertex_fill_color=self.vtype)
        #graph_draw(self.g, pos=pos, vertex_text=self.g.vertex_index, vertex_fill_color=self.vtype, output="complex.png")
