import sys
import solver
import time

def main(argv):
    if len(argv) != 2:
        print "Missing arguments"
        return 
    
    for i in range(int(argv[0]), int(argv[1])):
        out = open("solutions/%d.out" % i, "w")
        log = open("logs/%d.log" % i, "w")
        solution, penalty, correct = solver.solve(i, log)
        tmp = ""
        for cycle in solution:
            for node in cycle:
                tmp += str(node) + ", "
            tmp = tmp[:-2]
            tmp += "; "
        tmp = tmp[:-2]
        out.write(tmp + "\n")
        log.write("Total penalty: %d\n" % penalty)
        if correct == "ok":
            log.write("SOLUTION IS VALID\n")
        else:
            log.write("ERROR SOLUTION IS NOT VALID, %s\n" % correct)
        out.close()
        log.close()

if __name__ == "__main__":
    main(sys.argv[1:])
