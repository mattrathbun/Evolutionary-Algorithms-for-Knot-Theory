from ADT import *

class ADTComplex:
    def __init__(self, adt):
        self.adt = adt
        self.n = adt.number_crossings()
        self.n_arcs = 2*self.n
        self.n_regs = self.n + 2
        self.n_nodes = 4*self.n + 2
        self.inf_reg = 0
        
        self.init_incidence()
        self.init_regions()
        self.calc_incidence()
        self.init_neighbours()
        self.calc_neighbours()
    
    def init_incidence(self):
        self.regs = [[0,'']]
        self.c2 = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_regs+1)]
        self.c3 = [[0 for j in range(5)] for i in range(self.n_arcs+1)]
        self.er = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_arcs+1)]
        self.c4 = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_arcs+1)]
        self.rm = [[0 for j in range(self.n_regs+1)] for i in range(self.n_regs+1)]
        self.kf = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_regs+1)]
        self.opp = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_regs+1)]
    
    def calc_incidence(self):
        # print "nc = %d" % (self.n)
        # print "nr = %d" % (self.n_regs)
        # print "np = %d" % (self.n_arcs)
        # self.printmatrix("orientations", [[self.orient(i) for i in range(1,self.n_arcs+1)]])
        # self.printmatrix("f", [[self.f(i) for i in range(1,self.n_arcs+1)]])
        # self.printmatrix("g", [[self.g(i) for i in range(1,self.n_arcs+1)]])
        # self.printmatrix("sign", [[self.sign(i) for i in range(1,self.n_arcs+1)]])
        # self.printmatrix("phi", [[self.adt.phi(i,r) for i in range(1,self.n_arcs+1)] for r in range(self.n_arcs+1)])
        self.calc_incidence_c2()
        self.calc_incidence_c3()
        self.calc_incidence_er()
        self.calc_incidence_c4()
        self.calc_incidence_rm()
        self.calc_incidence_kf()
        self.calc_incidence_opp()

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
    
    def init_regions(self):
        for i in range(1,self.n_arcs+1):
            for s in ['L', 'R']:
                rnames = self.region_names(i,s)
                if rnames not in self.regs:
                    self.regs.append(rnames)
        # for r in self.regs[1:]:
        #    print r
    
    # C2: Incidence matrix of regions to edges.
    # C2[i,j] says whether region i is incident to edge j.
    def calc_incidence_c2(self):
        for i in range(1,self.n_regs+1):
            for r in self.regs[i]:
                self.c2[i][r[0]] = 1
        self.printmatrix("c2", self.c2)
        return

    # C3: Incidence of regions to crossings.
    # C3[i,0-3] lists the regions around crossing i, clockwise.
    def calc_incidence_c3(self):
        adt = self.adt
        c2 = self.c2
        for i in range(1,self.n_regs+1):
            for j in range(1,self.n_arcs+1):
                if c2[i][j] == 1:
                    if c2[i][adt.wrap(adt.jump(j)-1)] == 1:
                        self.c3[j][1] = i
                    if c2[i][adt.jump(j)] == 1:
                        self.c3[j][2] = i
            for j in range(1,self.n_arcs+1):
                if c2[i][adt.wrap(j-1)] == 1:
                    if c2[i][adt.jump(j)] == 1:
                        self.c3[j][3] = i
                    if c2[i][adt.wrap(adt.jump(j)-1)] == 1:
                        self.c3[j][4] = i
        self.printmatrix("c3", self.c3)
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
        self.printmatrix("er", self.er)
        return

    # C4: Edges meeting at crossing.
    # C4[i,j] = 1 if edges i and j meet at a crossing.
    def calc_incidence_c4(self):
        adt = self.adt
        for i in range(1,self.n_arcs+1):
            self.c4[i][adt.jump(i)] = 1
            self.c4[i][adt.wrap(adt.jump(i)-1)] = 1
            self.c4[i][adt.jump(adt.wrap(i+1))] = 1
            self.c4[i][adt.wrap(adt.jump(adt.wrap(i+1))-1)] = 1
        self.printmatrix("c4", self.c4)
        return
    
    # RM: Edges shared by adjacent regions
    def calc_incidence_rm(self):
        adt = self.adt
        c3 = self.c3
        for i in range(1,self.n_arcs,2):
            self.rm[c3[i][1]][c3[i][2]] = i
            self.rm[c3[i][2]][c3[i][1]] = i
            self.rm[c3[i][2]][c3[i][3]] = adt.jump(i)
            self.rm[c3[i][3]][c3[i][2]] = adt.jump(i)
        self.printmatrix("rm", self.rm)
        return
    
    # KF: Checkerboard sign of regions.
    # KF[i,j] is the sign of crossing j as seen from region i.
    def calc_incidence_kf(self):
        adt = self.adt
        c3 = self.c3
        for i in range(1,self.n_arcs+1):
            f = self.f(i)
            g = self.g(i)
            self.kf[c3[i][1]][i] = -f * g
            self.kf[c3[i][2]][i] = f * g
            self.kf[c3[i][3]][i] = -f * g
            self.kf[c3[i][4]][i] = f * g
        self.printmatrix("kf", self.kf)
        return
    
    # OPP: Opposite regions with respect to edges
    # OPP[i,j] = k means that i and k are opposite regions with respect to edge j.
    def calc_incidence_opp(self):
        rm = self.rm
        for i in range(1,self.n_regs):
            for j in range(i+1,self.n_regs+1):
                if (rm[i][j] != 0):
                    self.opp[i][rm[i][j]] = j
                    self.opp[j][rm[i][j]] = i
        self.printmatrix("opp", self.opp)
        return
    
    def init_neighbours(self):
        self.done = [0 for i in range(self.n_nodes+1)]
        self.ccr = [[0] for i in range(self.n_regs+1)]
        self.rot1 = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_regs+1)]
        self.rot2 = [[0 for j in range(self.n_arcs+1)] for i in range(self.n_regs+1)]
        self.newreg = [0 for i in range(self.n_regs + 1)]
        self.nb = [[0] for i in range(self.n_nodes + 1)]
        self.twoedge = [0 for i in range(self.n_arcs+1)]
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
    
        return -self.adt.quad(i)[3]
        return -self.adt.quad(i)[3]
    def orient(self,i):
        return -self.adt.quad(i)[3]
        return -self.adt.quad(i)[3]
    
    def f(self,i):
        return -self.adt.f(i)
    
    def g(self,i):
        return (1 if i % 2 == 1 else -1)
    
    def calc_neighbours(self):
        self.calc_neighbours_ccr()
        self.calc_neighbours_rot()
        self.calc_infinite_region()
        self.renumber_regions()
        self.calc_neighbours_nb()
        return
    
    # CCR: For each region, list of incident edges in anticlockwise order.
    def calc_neighbours_ccr(self):
        print "calc_neighbours_ccr"
        c2 = self.c2
        kf = self.kf
        adt = self.adt
        for reg in range(1,self.n_regs+1):
            print "  region %d" % (reg), self.regs[reg]
            print "  ", adt.regions(self.regs[reg][0][0], self.regs[reg][0][1])
            cedge = 0
            while (c2[reg][cedge] == 0):
                cedge += 1
            fedge = cedge
            print "    append %d" % (cedge)
            self.ccr[reg].append(cedge)
            dir = self.g(cedge) * kf[reg][cedge]
            print "    dir = %d" % (dir)
            while True:
                node = self.eb(cedge,dir)
                print "    node = %d" % (node)
                if (c2[reg][adt.jump(node)] == 1):
                    cedge = adt.jump(node)
                else:
                    cedge = adt.wrap(adt.jump(node) - 1)
                print "    append %d" % (cedge)
                self.ccr[reg].append(cedge)
                dir = self.g(cedge) * kf[reg][cedge]
                print "    dir = %d" % (dir)
                if (cedge == fedge):
                    break
            self.ccr[reg][0] = len(self.ccr[reg]) - 2
        self.printmatrix("ccr", self.ccr,1,0)
        return
    
    # ROT:
    # ROT1[i,j] = k if edge k follows edge j clockwise around region i
    # ROT2[i,j] = k if edge j follows edge k clockwise around region j
    def calc_neighbours_rot(self):
        ccr = self.ccr
        for reg in range(1,self.n_regs+1):
            for i in range(1,ccr[reg][0]+1):
                edge1 = ccr[reg][i]
                edge2 = ccr[reg][i+1]
                self.rot1[reg][edge1] = edge2
                self.rot2[reg][edge2] = edge1
        self.printmatrix("rot1", self.rot1)
        self.printmatrix("rot2", self.rot2)
        return
    
    def calc_infinite_region(self):
        nedge = 2
        ccr = self.ccr
        for reg in range(1,self.n_regs+1):
            if (ccr[reg][0] > nedge):
                self.inf_reg = reg
                nedge = ccr[reg][0]
        # print "inf_reg = %d" % (self.inf_reg)
    
    def renumber_regions(self):
        # self.printmatrix("ccr", self.ccr,1,0)
        t = 0
        ccr = self.ccr
        for reg in range(1,self.n_regs+1):
            if (reg != self.inf_reg) and (ccr[reg][0] != 2):
                t += 1
                self.newreg[reg] = t
                # print "newreg[%d] = %d" % (reg,t)
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
            dir = self.g(cedge) * kf[inf][cedge]
            prevedge = rot2[inf][cedge]
            prevdir = self.g(prevedge) * kf[inf][prevedge]
            cb = self.eb(cedge,-dir)
            ivertex.append(self.vertex_index(cb))
            node = self.vertex_index(cb)
            done[node] = 1
            
            # print "prevedge = %d, prevdir = %d" % (prevedge,prevdir)
            nb[node] = [5,0,0,0,0,0,0]
            nb[node][1] = n + cedge
            nb[node][2] = n + adt.wrap(prevedge + prevdir)
            nb[node][3] = n + self.be(cb,-dir)
            nb[node][4] = n + prevedge
            nb[node][5] = n_intnodes + i
            # print "nb[%d] = " % (node), nb[node]
        
        for i in range(1,nedge+1):
            cedge = ccr[inf][i]
            node = n + cedge
            done[node] = 1
            dir = self.g(cedge) * kf[inf][cedge]
            reg2 = opp[inf][cedge]
            if i == nedge:
                nbleft = n_intnodes + 1
            else:
                nbleft = n_intnodes + i + 1
            
            if ccr[reg2][0] == 2:
                nb[node] = [5,0,0,0,0,0,0]
                nb[node][1] = nbleft
                nb[node][3-dir] = self.vertex_index(adt.wrap(cedge+1))
                nb[node][3] = n + rot1[reg2][cedge]
                nb[node][3+dir] = self.vertex_index(cedge)
                nb[node][5] = n_intnodes + i
                # print "nb[%d] = " % (node), nb[node]
            else:
                nb[node] = [7,0,0,0,0,0,0,0,0]
                nb[node][1] = nbleft
                nb[node][4-2*dir] = self.vertex_index(adt.wrap(cedge+1))
                nb[node][3] = n + rot2[reg2][cedge]
                nb[node][4] = 3 * n + newreg[reg2]
                nb[node][5] = n + rot1[reg2][cedge]
                nb[node][4+2*dir] = self.vertex_index(cedge)
                nb[node][7] = n_intnodes + i
                # print "nb[%d] = " % (node), nb[node]
                
        for i in range(1,nedge+1):
            node = n_intnodes + i
            previdx = (nedge if i == 1 else i - 1)
            nextidx = (1 if i == nedge else i + 1)
            
            nb[node] = [4,0,0,0,0,0]
            nb[node][1] = n_intnodes + nextidx
            nb[node][2] = n + ccr[inf][i]
            nb[node][3] = ivertex[i]
            nb[node][4] = n + ccr[inf][previdx]
            nb[node][5] = n_intnodes + previdx
            # print "nb[%d] = " % (node), nb[node]
        
        for i in range(1,n+1,2):
            if done[self.vertex_index(i)] == 0:
                node = self.vertex_index(i)
                nb[node] = [4,0,0,0,0,0]
                nb[node][1] = n + i
                nb[node][3+self.orient(i)] = n + adt.jump(i)
                nb[node][3] = n + adt.wrap(i-1)
                nb[node][3-self.orient(i)] = n + adt.wrap(adt.jump(i) - 1)
                # print "nb[%d] = " % (node), nb[node]
        
        for cedge in range(1,n_arcs + 1):
            node = n + cedge
            if done[node] == 0:
                reg1 = 0
                while c2[reg1][cedge] == 0:
                    reg1 += 1
                reg2 = opp[reg1][cedge]
                
                if ccr[reg1][0] == 2:
                    reg1,reg2 = reg2,reg1
                dir = self.g(cedge) * kf[reg1][cedge]
                
                if ccr[reg2][0] == 2:
                    nb[node] = [6,0,0,0,0,0,0,0]
                    nb[node][1] = n + rot1[reg1][cedge]
                    nb[node][3-dir] = self.vertex_index(adt.wrap(cedge+1))
                    nb[node][3] = n + rot2[reg2][cedge]
                    nb[node][3+dir] = self.vertex_index(cedge)
                    nb[node][5] = n + rot2[reg1][cedge]
                    nb[node][6] = 3 * n + newreg[reg1]
                else:
                    nb[node] = [8,0,0,0,0,0,0,0,0,0]
                    nb[node][1] = n + rot1[reg1][cedge]
                    nb[node][4-2*dir] = self.vertex_index(adt.wrap(cedge+1))
                    nb[node][3] = n + rot2[reg2][cedge]
                    nb[node][4] = 3 * n + newreg[reg2]
                    nb[node][5] = n + rot1[reg2][cedge]
                    nb[node][4+2*dir] = self.vertex_index(cedge)
                    nb[node][7] = n + rot2[reg1][cedge]
                    nb[node][8] = 3 * n + newreg[reg1]
                # print "nb[%d] = " % (node), nb[node]
        
        for reg in range(1,self.n_regs + 1):
            if reg != inf and ccr[reg][0] != 2:
                node = 3 * n + newreg[reg]
                nedge = ccr[reg][0]
                nb[node] = [nedge] + [0 for i in range(nedge+1)]
                for i in range(1,nedge+1):
                    # print "nb[%d] = " % (node), nb[node]
                    nb[node][nedge+1-i] = n + ccr[reg][i]
        
        for i in range(1,self.n_nodes+1):
            valence = nb[i][0]
            if nb[i][valence+1] == 0:
                nb[i][valence+1] = nb[i][1]
            # print "nb[%d]" % (i), nb[i]
        return
    
    def flower(self,i):
        return self.nb[i][1:]
    
    def valency(self,i):
        return self.nb[i][0]
    
    def printmatrix(self,name,m,sr=1,sc=1):
        print name
        for row in m[sr:]:
            for el in row[sc:]:
                print "%2d" % (el),
            print ""
        print ""
        return
