import sys
import collections
import random
import Queue
import operator
import scc
import copy
import checker
import time

CYCLES_PER_NODE = 5
DP_MAX_SIZE = 10
#SKIPPED = (12, 15, 50, 102, 128, 154, 219, 238, 258, 352, 369, 409, 418, 429, 465)
SEARCH_ITERATIONS = 20
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
                solve(instance)
        else:
            solve(int(argv[0]))

def solve(instance, log_file=None):
    graph, children = read_graph("%d.in" % instance)
    nodes_left = [i for i in range(len(graph))]
    components = scc.scc(graph)
    solution = []
    if log_file:
        log_file.write("Found %d strongly connected components\n" % len(components))
    counter = 1
    for c in components:
        if log_file:
            log_file.write("\nCURRENTLY WORKING ON COMPONENT %d\n" % counter)
        counter += 1
        if not acyclic(graph, c):
            if len(c) > DP_MAX_SIZE:
                best_solution = None
                best_penalty = float("inf") # actual penalty in component
                for _ in range(SEARCH_ITERATIONS):
                    random_time0 = time.time()
                    tmp_solution, leftovers = random_solution(graph, c, children)
                    random_time1 = time.time()
                    if log_file:
                        log_file.write("New random solution with penalty in component: %d. Took %d sec\n" % (penalty_component(graph, children, tmp_solution, c), random_time1 - random_time0))
                    local_time0 = time.time()
                    local_best = local_search(graph, c, children, tmp_solution, leftovers)
                    local_time1 = time.time()
                    local_penalty = penalty_component(graph, children, local_best, c)
                    if log_file:
                        log_file.write("Local search improved penalty in component to: %d. Took %d sec\n" % (local_penalty, local_time1 - local_time0))
                    if local_penalty < best_penalty:
                        best_solution = local_best
                        best_penalty = local_penalty
                    if log_file:
                        log_file.write("Best solution reduces penalty in component to: %d\n" % best_penalty)
                    if best_penalty == 0:
                        break
                solution.extend(best_solution)
            else:
                dp_time0 = time.time()
                tmp = dynamic_programming(graph, c, children)
                dp_time1 = time.time()
                if log_file:
                    log_file.write("Dynamic programming solution found with score: %d. Took %d sec\n" % (tmp[0], dp_time1 - dp_time0))
                solution.extend(tmp[1])
                remVertMem = {}
        else:
            if log_file:
                log_file.write("Skipping acyclic component\n")

    print("Penalty for instance %d: %d" % (instance, penalty_overall(graph, children, solution)))
    return solution, penalty_overall(graph, children, solution), checker.check(graph, solution, children)

def acyclic(graph, component):
    return len(component) <= 1

def local_search(graph, component, children, solution, leftovers):
    leftovers = copy.copy(leftovers)
    current = copy.copy(solution)
    
    while True:
        best_neighbor = None
        best_penalty = float("inf") # actual penalty in component
        best_cycle_to_remove = None
        for cycle in current:
            nodes_left = set(cycle) | leftovers
            tmp = dynamic_programming(graph, nodes_left, children)
            new_cycles = tmp[1]
            base_solution = copy.copy(current)
            base_solution.remove(cycle)
            base_solution.extend(new_cycles)
            neighbor = base_solution # an actual neighboring solution
            neighbor_penalty = penalty_component(graph, children, neighbor, component) # actual penalty of actual neighbor in component
            # neighbor_penalty = tmp[0] # actual penalty of the new cycles as solution in component
            if not best_neighbor or neighbor_penalty < best_penalty:
                best_neighbor = neighbor
                best_penalty = neighbor_penalty
                best_cycle_to_remove = cycle

        # old_leftovers = copy.copy(leftovers)
        leftovers |= set(best_cycle_to_remove)
        leftovers -= solution_to_set(best_neighbor)
        if best_penalty >= penalty_component(graph, children, current, component):
            break
        elif best_penalty == 0:
            #current.remove(best_cycle_to_remove)
            #current.extend(best_neighbor)
            current = best_neighbor
            break
        else:
            #current.remove(best_cycle_to_remove)
            #current.extend(best_neighbor)
            current = best_neighbor

    return current

def solution_to_set(solution):
    retval = set()
    for cycle in solution:
        for node in cycle:
            retval.add(node)
    return retval

def random_solution(graph, component, children):
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
            if cycle:
                solution.append(cycle)
            for nd in cycle:
                nodes_left.remove(nd)
    return solution, nodes_left

def dynamic_programming(graph, V, children):
    minOverVertices = []

    if not V:
        return [0, []] 

    for v in V:
        cycles = bfs(graph, V, v)
        minOverCycles = []

        if (len(cycles) == 0):
            minOverCycles.append([penalty_component(graph, children, [], V), []])
        else:
            for cycle in cycles:
                remainingVertices = list(set(V) - set(cycle))
                keyRemainingVertices = tuple(remainingVertices)
                if keyRemainingVertices in remVertMem:
                    minOverCycles.append(remVertMem[keyRemainingVertices])
                else:
                    recurse = dynamic_programming(graph, remainingVertices, children)
                    minOverCycles.append([recurse[0], recurse[1] + [cycle]])

        minOverVertices.append(min(minOverCycles, key=lambda x:x[0]))

    optimalPenalty = min(minOverVertices,key=lambda x:x[0])
    remVertMem[tuple(V)] = optimalPenalty
    
    return optimalPenalty

'''
def penalty_dp(nodes_left, children):
    penalty = 0
    for node in nodes_left:
        if node in children:
            penalty += 2
        else:
            penalty += 1
    return penalty
'''

def penalty_overall(graph, children, solution):
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

def penalty_component(graph, children, solution, component):
    resolved = set()
    penalty = 0
    for cycle in solution:
        for node in cycle:
            resolved.add(node)
    for i in component:
        if i not in resolved:
            if i in children:
                penalty += 2
            else:
                penalty += 1
    return penalty

'''
def penalty_reduction(graph, solution, children):
    penalty = 0
    for cycle in solution:
        for node in cycle:
            if node in children:
                penalty += 2
            else:
                penalty +=1
    return penalty
'''

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
