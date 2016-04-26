import sys, collections, itertools


def main(argv):
    if len(argv) != 2:
        print "Please specify input filename and number of iterations"
        return
    else:
        return solve(argv[0], argv[1])

def solve(filename, iterations):
    f = open("instances/" + filename, 'r')
    
    #create graph
    graph = []
    num_nodes = int(f.readline())
    children = f.readline().split()
    for _ in range(num_nodes):
        graph.append(f.readline().split())

    #find <5-cycles
    cycles = {}
    for i in range(2, 6):
        #l should be list of i-cycles
        #[(1, 2, 3), ...]
        l = []
        for j in range(num_nodes):
            if j not in closed:
                tmp = cycle(j, i, graph, num_nodes)

        cycles[i] = l

def cycle(node, depth, graph, num_nodes):
    S = collections.deque() 
    closed = set()
    S.append(node)
    
    while S is not empty:
        v = S.pop()
        closed.add(v)
        for i in range(node+1, num_nodes):
            if graph[v][i]:
                S.append(i)



if __name__ == "__main__":
    main(sys.argv[1:]) 
