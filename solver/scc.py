def scc(graph):
    V = len(graph)
    vertex_order = vertices_in_decreasing_post_order(graph)
    ccnum, postnum = dfs(graph, vertex_order)
    return ccnum

# input "graph" is an adjacency list
# outputs a list where if the i-th and j-th items have the same value, then vertex i and vertex j are in the same strongly connected component
def dfs(graph, vertex_order):
    V = len(graph)
    visited = [False for _ in range(V)]
    cc = 0
    ccnum = [None for _ in range(V)]
    post = [0]
    postnum = [None for _ in range(V)]

    def explore(graph, v):
        visited[v] = True
        previsit(v)
        for u in neighbors(graph, v):
            if not visited[u]:
                explore(graph, u)
        postvisit(v, post)

    def previsit(v):
        ccnum[v] = cc

    def postvisit(v, post):
        postnum[v] = post[0]
        #print 'v: %d, post: %d' % (v, postnum[v])
        post[0] += 1
        
    for v in vertex_order:
        if not visited[v]:
            explore(graph, v)
            cc += 1

    return ccnum, postnum

'''
def neighbors(graph, v):
    V = len(graph)
    neighbors_list = []
    for i in range(V):
        if graph[v][i] == 1:
            neighbors_list.append(i)
    return neighbors_list
'''

def neighbors(graph, v):
    return graph[v]

def vertices_in_decreasing_post_order(graph):
    V = len(graph)
    reverse_graph = transpose_graph(graph)
    ccnum, postnum = dfs(reverse_graph, range(V))
    return map(lambda x: x[0], sorted([(i, postnum[i]) for i in range(V)], key=lambda x: x[1], reverse=True))

def transpose_graph(graph):
    V = len(graph)
    reverse_graph = [set() for _ in range(V)]
    for v in range(V):
        for u in graph[v]:
            reverse_graph[u].add(v)
    return reverse_graph

g = [[0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 1], [0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0]]

gadj = [[], [0, 4], [1, 5], [1], [1], [2, 4]]

gadj = map(set, gadj)
