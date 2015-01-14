from ADT import *
from graph_tool.all import *

class ADTComplex:
    def __init__(self, adt):
        self.adt = adt
        self.g = Graph()
        self.nodes = []
        self.edges = []
        self.faces = []
        self.labels = []
        self.n = adt.number_crossings()
        n = self.n

        # Add nodes corresponding to crossings
        for i in range(n):
            self.nodes.append("v%02d" % i)
            self.labels.append("v%02d" % i)
            self.g.add_vertex()

        # Add nodes corresponding to arcs
        for i in range(n):
            odd, even, sign, orient = adt.quad(2*i+1)
            
            odd2, even2, sign2, orient2 = adt.quad(adt.wrap(odd+1))
            self.edges.append("e%02d%02d" % (i,(odd2-1)/2))
            self.labels.append("e%02d%02d" % (i,(odd2-1)/2))
            self.g.add_vertex()
            e = self.g.vertex(n+2*i)
            v = self.g.vertex(i)
            w = self.g.vertex((odd2-1)/2)
            self.g.add_edge(v,e)
            self.g.add_edge(e,w)
            
            odd3, even3, sign3, orient3 = adt.quad(adt.wrap(even+1))
            self.edges.append("e%02d%02d" % (i,(odd3-1)/2))
            self.labels.append("e%02d%02d" % (i,(odd3-1)/2))
            self.g.add_vertex()
            e = self.g.vertex(n+2*i+1)
            v = self.g.vertex(i)
            w = self.g.vertex((odd3-1)/2)
            self.g.add_edge(v,e)
            self.g.add_edge(e,w)

        # Add nodes corresponding to regions
        
    def crossing_index(self,n):
        odd = adt.quad(n)[0]
        return (odd-1)/2
    
    def edge_index(self,n,parity):
        if parity == 1 or parity.lower() in ["odd", "o"]:
            return 3*n
        elif parity == 0 or parity.lower() in ["even", "e"]:
            return 3*n+1
        else:
            raise TypeError("Parity should be [odd, o, 1] or [even, e, 0]")
     
    def draw_graph(self):
        pos = sfdp_layout(self.g)
        graph_draw(self.g, pos=pos, vertex_text=self.g.vertex_index)
