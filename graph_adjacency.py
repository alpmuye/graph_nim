import numpy as np
import copy
import itertools
import networkx as nx

from itertools import chain, combinations

def powerset_generator(i):
    for ss in chain.from_iterable(combinations(i, r) for r in range(len(i)+1)):
        yield set(ss)

def DFS(matrix, vertex): #matrix*vertex -> vertex list
    visited=set()
    visited.add(vertex)
    while True:
        visitedThisRound=set()
        for v1 in visited:
            for v2 in np.flatnonzero(matrix[v1]): #gets indexes of all edges
                if v2 not in visited:
                    visitedThisRound.add(v2)
        if len(visitedThisRound)==0: break
        else: visited=visited.union(visitedThisRound)
    return sorted(list(visited))

matrix1=np.array([[0]])
matrix2=np.array([[0,1,1], [1,0,0], [1,0,0]])
matrix3=np.array([[0,1,0], [1,0,0], [0,0,0]])

assert(DFS(matrix1, 0)==[0])
assert(DFS(matrix2, 0)==[0,1,2])
assert(DFS(matrix2, 1)==[0,1,2])
assert(DFS(matrix2, 2)==[0,1,2])
assert(DFS(matrix3, 0)==[0,1])
assert(DFS(matrix3, 1)==[0,1])
assert(DFS(matrix3, 2)==[2])
#this needs more test cases with more meaningful graphs

def makeMove(matrix, move, vertex):
    newMatrix=copy.deepcopy(matrix)
    for edge in move:
        newMatrix[vertex][edge]=0
        newMatrix[edge][vertex]=0
    return newMatrix

def makelistlist(L):
    newL=[]
    for i in L:
        newL.append([i])
    return newL

def isKayles(sequence):
    if not seq[0:2]==[1,1]:
        return False
    else:
        for i in seq[2:len(seq)]:
            if i!=2: return False
        return True

assert(makelistlist([])==[])
assert(makelistlist([1,2,3])==[[1],[2],[3]])

class Graph(object):

    def __init__(self, mt):
        #assert(mt!=None)
        self.adj = np.array(mt) #adjacency matrix representation of the graph
        self.n = len(self.adj) # number of vxs
        self.m = np.count_nonzero(self.adj)/2 #number of edges (total degree/2)
        self.G=nx.from_numpy_matrix(np.matrix(mt))
        self.degree=[np.count_nonzero(self.adj[i]) for i in range(self.n)]
        self.degree.sort()
        self.nimber=None
        self.isKayles=isKayles(self.degree)

    def delete_edgeless_vertex(self): pass #later

    def addEdge(self, i, j):
        if self.adj[i][j]==0:
            self.m+=1
            self.adj[i][j]=1
            self.adj[j][i]=1
            self.degree=[np.count_nonzero(self.adj[i]) for i in range(self.n)]
            self.degree.sort()

    def get_all_isomorphisms(self): #graph->matrix list
        I=np.identity(self.n) #identity matrix of size self.n
        P=[np.vstack(i) for i in itertools.permutations(I)]#ALL permutation of I
        return [np.array(np.matrix(p)*self.adj*np.matrix(p).T) for p in P]

    def is_isomorphic_with(self, graph): #graph-> Boolean
        if (self.n!=graph.n) or (self.m!=graph.m): return False
        #if (self.degree!=graph.degree): return False

        # try all permutations
        # but do not try the permutations which do not match the vertex
        # degrees (well maybe do that later.)
        #
        #I=np.identity(self.n) #identity matrix of size self.n
        #P=[np.vstack(i) for i in itertools.permutations(I)]#ALL permutation of I

        #IF YOU CAN FIX THE P ABOVE SO IT DOESN'T HAVE n! matrixes, that would
        #be stellar.

        #for p in P:
            #if (np.array_equal(np.matrix(p)*graph.adj*np.matrix(p).T,
                                                    #np.matrix(self.adj))):
            #    return True #FOUND A BIJECTION
        #else: return False

    def get_next_states(self): #graph -> graph list list
        nextStates=list()
        for i in range(self.n):
            vertex=self.adj[i]
            edges=np.flatnonzero(vertex)
            for move in powerset_generator(edges):
                if len(move)==0: continue #move cannot be the empty set.
                newMatrix=makeMove(self.adj, move, i)
                move.add(i)
                connected_components=list() #matrix list
                for edge in move:
                    cc = DFS(newMatrix, edge)
                    ccMatrix=newMatrix[makelistlist(cc), cc]
                    connected_components.append(Graph(ccMatrix))
                nextStates.append(connected_components)
        return nextStates

G1=Graph([[0,1,1],[1,0,0],[1,0,0]])
G2=Graph([[0,1,1],[1,0,0],[1,0,0]])
G3=Graph([[0,1,1],[1,0,0],[1,0,1]])

#assert(G1.is_isomorphic_with(G2)==True)
#assert(G2.is_isomorphic_with(G3)==False)



#for g in G1.get_next_states(): print(g) #I think only good way of testing this is
                                       #to set up different graphs, and print
                                       #the results and inspect them as I have
                                       #been doing.
