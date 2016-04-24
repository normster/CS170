import numpy as np
import random, math

f = open('instance2.in', 'w')

f.write('498\n')
s = ''
for i in range(498):
    if random.random() > 0.5:
        s += '%d ' % i

s = s[:-1] + '\n'

f.write(s)

graph = np.zeros((498, 498))

for i in range(0, 498, 6):
    for j in range(i, i+5):
        for k in range(j+1, i+6):
            if random.random() <= 0.85:
                graph[j][k] = 1
            if random.random() <= 0.85:
                graph[k][j] = 1
        graph[j][j+1] = 1
    if i != 492:
        graph[i][i+6] = 1

graph[492][0] = 1

for i in range(498):
    s = ''
    for j in range(498):
        if graph[i][j]:
            s += '1 '
        else:
            s += '0 '
    s = s[:-1] + '\n'
    f.write(s)

f.close()
