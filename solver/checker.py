def check(graph, children, solution):
    used = set()
    for cycle in solution:
        for i in range(len(cycle)):
            if cycle[i] in used:
                return False
            else:
                used.add(cycle[i])
            if cycle[(i+1) % len(cycle)] not in graph[cycle[i]]:
                return False

    return True
