from graph_adjacency import Graph
import numpy as np
import pandas as pd
import copy
import math
import networkx as nx

def mex(L):
    if L==[0]: return 1
    newL=list(set(L))
    newL.sort()
    for i in range(len(newL)):
        if newL[i]!=i: return i
    return len(newL)

def codifyMatrix(matrix):
    return(str(flatten(matrix)))

                            ##            ##
                            ## GAME CLASS ##
                            ##            ##


class Game(object):

    def __init__(self, graphs, nimberDict, graphBank=set()): #graphs=graph list
        self.connected_components=set(graphs)
        self.nimberDict=nimberDict
        self.graphBank=graphBank

    def calculateNimber(self):
        nimbers=[]
        for component in self.connected_components:
            nimbers.append(self.calculateTreeNimber(component))
        while len(nimbers)>=2:
            nim1=nimbers.pop()
            nim2=nimbers.pop()
            nimbers.append(nim1^nim2) #nimsum
        return nimbers[0]

    def searchIsomorphisms(self, component):
        for graph in self.graphBank:
            if nx.is_isomorphic(graph.G, component.G):
                return graph.nimber
        return None

    def calculateTreeNimber(self, component):
        code=codifyMatrix(component.adj)
        if component.m==0:
            return 0 #terminal position: no edges
        elif component.isKayles:
            return calculateKayles(len(component.adj)-1)
        elif code in self.nimberDict:
            return self.nimberDict[code]
        iso_nimber = self.searchIsomorphisms(component)
        elif iso_nimber!=None:
            self.nimberDict[code]=iso_nimber
            return iso_nimber
        else:
            nextStates=[Game(i, self.nimberDict, self.graphBank) for i in component.get_next_states()]
            nimbers =[game.calculateNimber() for game in nextStates]
            nimber = mex(nimbers)
            self.nimberDict[code]=nimber
            return nimber

def addEdgeMatrix(matrix, i, j):
    matrix[i][j]=1
    matrix[j][i]=1

def createYGame(n, nimberDict=dict()): #inefficient but works.
    matrix=np.zeros((n,n))
    addEdgeMatrix(matrix, 0, n-1)
    addEdgeMatrix(matrix, 0, n-2)
    for i in range(n-3):
        addEdgeMatrix(matrix, i, i+1)
    return Game([Graph(matrix)], nimberDict)

def createPerfectBowlingGame(n, nimberDict):
    matrix=np.zeros((n,n))
    for i in range(n-1):
        addEdgeMatrix(matrix, i, i+1)
    return Game([Graph(matrix)], nimberDict)

def get_nth_tree_matrix(n, matrix): #balanced binary trees ordered by # of edges
    if n==0:
        return matrix
    else:
        if n>1:
            r=int(math.log((n-1), 2))
        else: r=1
        k=2**(r)-1-int((2**(r+1)-1-(n-1))/2)
        addEdgeMatrix(matrix, n, k)
        return get_nth_tree_matrix(n-1, matrix)

nimberDict=dict()
treeDict=dict()

for i in range(1,30):
    print i, createYGame(i, nimberDict).calculateNimber()

"""
#uncomment this to obtain csv's of binary trees between 1 to 100

for i in range(1, 100):
    mt=get_nth_tree_matrix(i, np.zeros((i+1, i+1), int))
    thisG=Graph(mt)
    thisNimber=Game([thisG], nimberDict).calculateNimber()
    print i, thisNimber
    treeDict[i]=thisNimber
    df1=pd.DataFrame.from_dict(nimberDict, "index")
    df2=pd.DataFrame.from_dict(treeDict, "index")
    df1.to_csv("dicts/treeclasses_newer.csv")
    df2.to_csv("dicts/treeDict_newer.csv")
"""
