import numpy as np
import random

N = 500
E = []
C = []

# Printing number of vertices
print(N,end="\n")

# Choosing whether vertices are children or adults
for i in range(N):
    sample = random.random()
    if (sample >= 0.5):
        C.append(i)

# Printing out vertices that are children
for i in range(len(C)):
    if (i == len(C) - 1):
        print(str(C[i]),end="\n")
    else:
        print(str(C[i]),end=" ")

# Choosing which edges are in the graph
for i in range(N):
    for j in range(N):
        sample = random.random()
        if (i != j):
            if (sample >= 0.5):
                E.append((i,j))

mat = [np.zeros(N,dtype=np.int) for i in range(N)]

# Making a adjacency matrix of the edges
for f,s in E:
    mat[f][s] = 1

# Printing adjacency matrix
for i in range(len(mat)):
    for j in range(len(mat[0])):
        print(mat[i][j], end=" ")
    print("", end="\n")
