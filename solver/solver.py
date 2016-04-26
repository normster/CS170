import sys, itertools


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


if __name__ == "__main__":
    main(sys.argv[1:]) 
