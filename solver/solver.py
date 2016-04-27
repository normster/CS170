
import sys, collections, itertools


def main(argv):
    if len(argv) != 2:
        print "Please specify input filename and number of iterations"
        return
    else:
        graph, num_nodes = parse(argv[0])
        return solve(graph, num_nodes, argv[1])

def parse(filename):
    f = open("instances/" + filename, 'r')
    
    #create graph
    graph = []
    num_nodes = int(f.readline())
    children = f.readline().split()
    for _ in range(num_nodes):
        line = f.readline().split()
        tmp = set()
        for i in range(num_nodes):
            if line[i]:
                tmp.add(i)
        graph.append(tmp)

    return graph, num_nodes

def solve(graph, num_nodes, iterations):
    #find <5-cycles
    cycles = {}
    for i in range(5, 6):
        #l should be list of i-cycles
        #[(1, 2, 3), ...]
        l = []
        for j in range(num_nodes):
            #we always iterate through nodes in numerical order
            #when calling cycle() on node i, we only consider cycles using nodes >i
            l.extend(cycle(j, i, graph, num_nodes))

        cycles[i] = l
    
    #returns cycles for now for testing
    return cycles

def cycle(node, length, graph, num_nodes):
    retval = []
    S = collections.deque() 
    S.append([node])
    
    while S:
        v = S.pop()
        if len(v) == length:
            if node in graph[v[-1]]:
                retval.append(v)
        else:
            for adj in graph[v[-1]]:
                if adj > node:
                    S.append(v + [adj])

    return retval

if __name__ == "__main__":
    main(sys.argv[1:]) 