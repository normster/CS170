import sys
import collections
import random
import Queue
import operator
import scc
import copy

CYCLES_PER_NODE = 10
DP_MAX_SIZE = 20
SKIPPED = (12, 15, 50, 102, 128, 154, 219, 238, 258, 352, 369, 409, 418, 429, 465)
SEARCH_ITERATIONS = 10
remVertMem = {}

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
        tmp = set()
        for i in range(num_nodes):
            if s[i] == '1':
                tmp.add(i)
        graph.append(tmp)
    return graph, children

def main(argv):
    if len(argv) != 1:
        print("Missing argument")
    else:
        if argv[0] == "all":
            for instance in range(1, 493):
                if instance not in SKIPPED:
                    solve(instance)
        else:
            solve(int(argv[0]))

def solve(instance):
    graph, children = read_graph("%d.in" % instance)
    nodes_left = [i for i in range(len(graph))]
    components = scc.scc(graph)
    solution = []
    for c in components:
        if not acyclic(graph, c):
            if len(c) > DP_MAX_SIZE:
                best_solution = None
                best_penalty = float("-inf")
                max_penalty = penalty_reduction(graph, [[n for n in c]], children)
                for _ in range(SEARCH_ITERATIONS):
                    solution, leftovers = random_solution(graph, c, children)
                    local_best = local_search(graph, c, children, solution, leftovers)
                    local_penalty = penalty_reduction(graph, local_best, children)
                    if local_penalty > best_penalty:
                        best_solution = local_best
                        best_penalty = local_penalty
                    if max_penalty == best_penalty:
                        break
                solution.extend(best_solution)
            else:
                solution.extend(dynamic_programming())
                remVertMem = {}

    print("Penalty for instance %d: %d" % (instance, penalty_overall(graph, solution, children)))

def acyclic(graph, component):
    if not component:
        return True

    S = collections.deque()
    start = component.pop()
    component.add(start)
    S.append(start)
    visited = set()
    while S:
        current = S.pop()
        if current in visited:
            return False
        else:
            visited.add(current)
            for neighbor in graph[current]:
                if neighbor in component:
                    S.append(neighbor)
    return True

def local_search(graph, component, children, solution, leftovers):
    current = copy.copy(solution)
    current_penalty = penalty_reduction(graph, current, children)
    
    while True:
        best_neighbor = None
        best_penalty = float("-inf")
        max_penalty = penalty_reduction(graph, [[n for n in component]], children)
        for cycle in current:
            nodes_left = set(cycle) | leftovers
            neighbor = dynamic_programming(graph, nodes_left, children)
            neighbor_penalty = penalty_reduction(graph, neighbor, children)
            if not best_neighbor or neighbor_penalty > best_penalty:
                best_neighbor = neighbor
                best_penalty = neighbor_penalty
        
        if best_penalty <= current_penalty or best_penalty == max_penalty:
            break
        else:
            current = best_neighbor
            current_penalty = best_penalty

    return current

def random_solution(graph, component, children):
    #TODO: fix iteration_order
    order = iteration_order(graph)
    nodes_left = copy.copy(component)
    solution = []
    for node in order:
          if node in nodes_left:
            #finding cycles starting at that node
            cycles = find_cycles_dfs(graph, node, nodes_left)
            #TODO: fix choose_cycle
            cycle = choose_cycle(cycles, children)
            #once we've incorporated a cycle into the solution, we remove the nodes from consideration
            solution.append(cycle)
            for nd in cycle:
                nodes_left.remove(nd)
    return solution, nodes_left

def dynamic_programming(graph, V, children):
    minOverVertices = []

    if not V:
        return []

    for v in V:
        cycles = bfs(graph, V, v)
        minOverCycles = []

        if (len(cycles) == 0):
            minOverCycles.append([penalty_overall(graph, V, children), []])
        else:
            for cycle in cycles:
                remainingVertices = list(set(V) - set(cycle))
                keyRemainingVertices = tuple(remainingVertices)
                if (keyRemainingVertices in remVertMem.keys()):
                    minOverCycles.append(remVertMem[keyRemainingVertices])
                else:
                    recurse = dynamic_programming(graph, remainingVertices, children)
                    minOverCycles.append([recurse[0], recurse[1] + [cycle]])

        minOverVertices.append(min(minOverCycles, key=lambda x:x[0]))

    optimalPenalty = min(minOverVertices,key=lambda x:x[0])
    remVertMem[tuple(V)] = optimalPenalty
    
    return optimalPenalty

def penalty_overall(graph, solution, children):
    resolved = set()
    penalty = 0
    for cycle in solution:
        for node in cycle:
            resolved.add(node)
    for i in range(len(graph)):
        if i not in resolved:
            if i in children:
                penalty += 2
            else:
                penalty += 1
    return penalty

def penalty_reduction(graph, solution, children):
    penalty = 0
    for cycle in solution:
        for node in cycle:
            if node in children:
                penalty += 2
            else:
                penalty +=1
    return penalty

def iteration_order(graph):
    num_nodes = len(graph)
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
        if len(current) <= 4:
            for neighbor in graph[tail]:
                if neighbor not in current and neighbor in nodes_left:
                    S.append(current + [neighbor])
    return cycles

def bfs(graph, nodes_left, node):
    #list of cycles for a particular node
    cycles = []
    q = Queue.Queue()
    q.put([node])
    while q.qsize() > 0:
        #current list of nodes in a prospective cycle
        current_thread = q.get()
        #accessing the tail
        tail = current_thread[-1]
        #checking if the tail has a backedge
        if node in graph[tail]:
            cycles.append(current_thread)
        if len(current_thread) <= 4:
            for neighbor in graph[tail]:
                if neighbor not in current_thread and neighbor in nodes_left:
                    q.put(current_thread + [neighbor])
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
