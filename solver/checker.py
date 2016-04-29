def check(graph, solution, children):
    used = set()
    for cycle in solution:
        for i in range(len(cycle)):
            if cycle[i] in used:
                return "reused node " + str(cycle[i])
            else:
                used.add(cycle[i])
            if cycle[(i+1) % len(cycle)] not in graph[cycle[i]]:
                return "invalid edge from " + str(cycle[(i+1)%len(cycle)]) + " to " + str(cycle[i])

    return "ok"
