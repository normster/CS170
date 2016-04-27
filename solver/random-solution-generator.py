import sys, collections, itertools, random, copy
import Queue
def readGraph(filename):
	f = open("instances/" + filename, 'r')
	#create graph
	graph = []
	num_nodes = int(f.readline())
	children = f.readline().split()
	children = map(int, children)
	for _ in range(num_nodes):
		s = f.readline().split()
		tmp = []
		for i in range(num_nodes):
			if s[i] == '1':
				tmp += [i]
		graph.append(tmp)
	return graph, num_nodes,children


def main(argv):
	if len(argv) != 1:
		print("Please specify the input file name")
	else:
		graph, num_nodes, children = readGraph(argv[0])
		remainingNodes = [i for i in range(num_nodes)]
		penalty = randomSolution(graph, num_nodes, children, remainingNodes)

def randomSolution(graph, num_nodes, children, remainingNodes):

	nodeIterationOrder = randomizeNodeIterationOrder(graph, num_nodes)
	# for node in nodeIterationOrder:
	#  	if node in remainingNodes:
	#   		cycles = bfs(graph, node, remainingNodes)
	# #		cycle = chooseCycle(cycles)
	# #		for nd in cycle:
	# # 			remainingNodes.remove({nd})
	# # penalty = 0
	# # for node in remainingNodes:
	# # 	if node in children:
	# # 		penalty += 2
	# # 	else:
	# # 		penalty +=1
	# # return penalty



	
	
def randomizeNodeIterationOrder(graph, num_nodes):
	nodes = [i for i in range(num_nodes)]
	nodeIterationOrder = []
	while len(nodes) != 0:
		node = random.choice(nodes)
		nodeIterationOrder += [node]
		nodes.remove(node)
	return nodeIterationOrder

def bfs(graph, node, remainingNodes):
	cycles = []
	q = Queue.Queue()
	q.put([node])
	while q.qsize() > 0:
		currentThread = q.get()
		tail = currentThread[len(currentThread) - 1]
		if tail == node and len(currentThread) > 1:
			cycles += [currentThread[0: len(currentThread) - 1]]
		for n in graph[tail]:
		 	c = copy.copy(currentThread)
		 	if n in remainingNodes:
		 		c += [n]
		 		if len(c) <= 6:
		 			q.put(c)
	return cycles
	










		







	

	






if __name__ == "__main__":
    main(sys.argv[1:]) 