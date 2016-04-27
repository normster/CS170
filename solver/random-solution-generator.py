import sys, collections, itertools, random, copy
import Queue
import operator

CYCLES_PER_NODE = 10
DP_MAX_SIZE = 20
SKIPPED = (12, 15, 50, 102, 128, 154, 219, 238, 258, 352, 369, 409, 418, 429, 465)

#creating graph
def read_graph(filename):
    f = open("instances/" + filename, 'r')
    #create graph
    graph = []
    num_nodes = int(f.readline())
    children = set(f.readline().split())
    children = map(int, children)
    for _ in range(num_nodes):
        s = f.readline().split()
        tmp = []
        for i in range(num_nodes):
            if s[i] == '1':
                tmp += [i]
        graph.append(tmp)
    return graph, num_nodes, children


def main(argv):
    if len(argv) != 1:
        print("Missing command-line")
    else:
        if argv[0] == "all":
            for instance in range(1, 493):
                if instance not in SKIPPED:
                    graph, num_nodes, children = read_graph("%d.in" % instance)
                    nodes_left = [i for i in range(num_nodes)]
                    components = component_finder(graph, num_nodes)
                    solution = []
                    for c in components:
                        if not acyclic(c):
                            if size(c) > DP_MAX_SIZE:
                                solution += local_search(c)
                            else:
                                solution += dynamic_programming(c)

                    print("Penalty for instance %d: %d" % (instance, penalty(solution)))

        else:
            graph, num_nodes, children = read_graph(argv[0])
            # generating a remaining nodes variable to keep track of nodes which have not been used in cycles
            nodes_left = [i for i in range(num_nodes)]
            penalty = random_solution(graph, num_nodes, children, nodes_left)
            print("Penalty: " + str(penalty))

def local_search():
    current = random_solution()
    current_penalty = penalty(current)
    while True:
        best_neighbor = improve(current)
        best_penalty = penalty(best_neighbor)
        if best_penalty >= current_penalty:
            break

def random_solution(graph, num_nodes, children, nodes_left):
    #for now nodeIterationOrder is completely random
    order = iteration_order(graph, num_nodes)
    for node in order:
          if node in nodes_left:
              #finding cycles starting at that node
            cycles = find_cycles_dfs(graph, node, nodes_left)
               #choosing a completely random cycle
            cycle = choose_cycle(cycles, children)
            #once we've incorporated a cycle into the solution, we remove the nodes from consideration
            for nd in cycle:
                nodes_left.remove(nd)
    #return cycles used

def penalty():
    penalty = 0
    for node in nodes_left:
        if node in children:
            penalty += 2
        else:
            penalty +=1
    return penalty

def iteration_order(graph, num_nodes):
    nodes = [i for i in range(0,num_nodes)]
    weightVector = assign_weights(graph, nodes)
    sortedWeightVector = sorted(weightVector.items(), key=operator.itemgetter(1))
    nodeIterationOrder = []
    #print(sortedWeightVector)
    for tup in sortedWeightVector:
        nodeIterationOrder += [tup[0]]
    return nodeIterationOrder


def assign_weights(graph, nodes):
    weightVector = {}
    for node in nodes:
        weightVector[node] = 0
        for n in graph[node]:
            weightVector[node] += 1
    return weightVector

def find_cycles_dfs(graph, node, nodes_left):
    cycles = []
    num_cycles = 0
    S = collections.deque()
    S.append([node])
    while S and num_cycles < CYCLES_PER_NODE:
        current = S.pop()
        tail = current[-1]
        if node in graph[tail]:
            cycles.append(current)
            num_cycles += 1
        else:
            if len(current) <= 4:
                for neighbor in graph[tail]:
                    if neighbor not in current and neighbor in nodes_left:
                        S.append(current + [neighbor])
    return cycles

def bfs(graph, node, remainingNodes):
    #list of cycles for a particular node
    cycles = []
    q = Queue.Queue()
    q.put([node])
    while q.qsize() > 0:
        #current list of nodes in a prospective cycle
        currentThread = q.get()
        #accessing the tail
        tail = currentThread[len(currentThread) - 1]
        #checking if the tail has a backedge
        if tail == node and len(currentThread) > 1:
            cycles += [currentThread[0: len(currentThread) - 1]]
            #print("Cycle detected: " + str(cycles))
            continue
        elif tail in currentThread[1: len(currentThread) - 1]:
            # if we have a smaller cycle along the path, there's no point tracking it
            continue
        for n in graph[tail]:
             c = copy.copy(currentThread)
             if n in remainingNodes:
                 c += [n]
                 if len(c) <= 6:
                     q.put(c)

    #print("Done detecting")
    return cycles

def choose_cycle(cycles, children):
    cycle = []
    if len(cycles) != 0:
        cycle = random.choice(cycles)
    return cycle

def sample(dictionary, range):
    r = random.random(0, range)
    s = 0
    for key in dictionary.keySet():
        s += dictionary.get(k)
        if r <= s:
            return dictionary.get(k)

if __name__ == "__main__":
    main(sys.argv[1:])
