# graph_nim
python implementation of the graph nim game.

Computes nimber of a arbitrary graph given a list of the adjacency matrix of the graph's connected components. 
To make use of memoization, call the method as:

nimberDict=dict()
nimber=Game([thisG], nimberDict).calculateNimber()
