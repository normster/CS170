import solver
import checker
from ast import literal_eval
import os.path

# directory_name should contain individual solutions
def get_individual_solutions(directory_name):
    solutions = {}
    for i in range(1, 492 + 1):
        if os.path.isfile('%s/%d.out' % (directory_name, i)):
            with open('%s/%d.out' % (directory_name, i)) as f:
                sol_str = f.read()
                if sol_str == '' or sol_str == '\n':
                    solution = []
                else:
                    solution = [literal_eval('[' + x + ']') for x in sol_str.split('; ')]
                solutions[i] = solution
    return solutions

# get solutions from full solutions file
def get_solutions(directory_name):
    solutions = []
    solutions_dict = {}
    with open('%s/solutions.out' % directory_name) as f:
        for line in f:
            if 'None' in line:
                solution = []
            else:
                solution = [literal_eval('[' + ', '.join(x.split()) + ']') for x in line.split('; ')]
            solutions.append(solution)
    for i in range(492):
        solutions_dict[i + 1] = solutions[i]
    return solutions_dict

# solutions1 and solutions2 should be dictionaries of instance number to list of cycles
def weave_solutions(solutions1, solutions2):
    log = {} # each element in form (instance, better solution number (1 or 2), better solution, penalty difference)
    for i in range(1, 492 + 1):
        if i not in solutions1 and i not in solutions2:
            log[i] = (i, None, None, None)
        elif i not in solutions2:
            log[i] = (i, 1, solutions1[i], None)
        elif i not in solutions1:
            log[i] = (i, 2, solutions2[i], None)
        else:
            g, c = solver.read_graph('%d.in' % i)
            penalty_diff = solver.penalty_overall(g, c, solutions1[i]) - solver.penalty_overall(g, c, solutions2[i])
            if penalty_diff >= 0:
                log[i] = (i, 1, solutions1[i], penalty_diff)
            else:
                log[i] = (i, 2, solutions2[i], -penalty_diff)
    return log

def extract_sol_from_log(log):
    solutions = []
    for i in range(1, 492 + 1):
        solutions.append(log[i][2])
    found_invalid = False
    for i in range(1, 492 + 1):
        g, c, = solver.read_graph('%d.in' % i)
        if checker.check(g, solutions[i - 1], c) != 'ok':
            found_invalid = True
            print 'Solution %d is invalid' % i
    if not found_invalid:
        print 'All weaved solutions are valid'
        for i in range(1, 492 + 1):
            if log[i][3] > 0 and log[i][3] != None:
                if log[i][1] == 1:
                    print 'Original solution for %d better by %d' % (i, log[i][3])
                elif log[i][1] == 2:
                    print 'New solution for %d better by %d' % (i, log[i][3])
    return solutions
