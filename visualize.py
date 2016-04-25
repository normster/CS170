import networkx as nx
import sys
import matplotlib.pyplot as plt

inputFile = open(sys.argv[1])

M = []
E = []

for i,line in enumerate(inputFile):
    if (i == 0):
        N = int(line.split(" ")[0])
    elif (i == 1):
        C = [int(i) for i in line.rstrip().split(" ")]
    else:
        M.append([int(i) for i in line.rstrip().split(" ")])

G = nx.Graph()

for i in range(N):
    G.add_node(i)

for i in range(len(M)):
    for j in range(len(M[0])):
        if (M[i][j] == 1):
            E.append((i,j))

for f,s in E:
    G.add_edge(f,s)

color_map = []
for node in G:
    if (node in C):
        color_map.append('red')
    else:
        color_map.append('blue')

nx.draw(G,node_color = color_map, with_labels=True)
plt.show()
