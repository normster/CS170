
def generateGreedyInstance():
	i = 0
	adjacencyList = []
	children =[]
	while i < 500:
		generateFlowers(i,adjacencyList,children)
		i+=25

	i = 0 
	while i < 475:
		adjacencyList[i] += [i+25]
		i+=25
	print(adjacencyList)

	f = open("INSTANCE1.txt","w")
	f.write("500\n")
	for child in children:
		f.write(str(child)+ " ")
	f.write("\n")
	for vertex in range(0,500):
		for v in range(0,500):
			if v in adjacencyList[vertex]:
				f.write("1 ")
			else:
				f.write("0 ")
		f.write("\n")
	f.close()





def generateFlowers(seed,adjacencyList,children):
	#creating flower centers
	for i in range(0,25):
		adjacencyList += [[]]
	for i in range(seed,seed+4):
		adjacencyList[i] += [i+1]
		children += [i]
	children += [seed+4]
	adjacencyList[seed+4] = [seed]

	adult = seed+5
	for i in range(seed,seed+5):
		vertex1 = i
		vertex2 = adult
		for j in range(0,4):
			adjacencyList[vertex1] += [vertex2]
			vertex1 = adult
			adult += 1
			vertex2 = adult
		vertex2 -=1 
		adjacencyList[vertex2] += [i]



		


generateGreedyInstance()