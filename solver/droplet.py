import sys
import solver
import time
RAND_LOCAL = (244, 249, 344, 448, 456, 170, 288, 197, 378, 459, 462, 380, 465, 469, 479, 490)

def main(argv):
    #for i in range(int(argv[0]), int(argv[1])):
    for s in argv:
        i = int(s)
        out = open("solutions/%d.out" % i, "w")
        log = open("logs/%d.log" % i, "w")
        if i in RAND_LOCAL:
            solution, penalty, correct = solver.solve(i, log, True)
        else:
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
