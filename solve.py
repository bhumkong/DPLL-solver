#!/usr/bin/python

import sys
import signal
import itertools

TRUE = 1
FALSE = -1
UNKNOWN = 0

f = open(sys.argv[1])
lines = f.readlines()
f.close()

# parsing
start = int()
for i in range(len(lines)):
    if lines[i][0] == 'p':
        start = i
        break

words = lines[start].split()
nbvar, nbclauses = int(words[2]), int(words[3])
clauses = [[int(x) for x in lines[i].split()[:-1]] for i in range(start + 1, start + 1 + nbclauses)]
# parsing finished

variables = [UNKNOWN] * nbvar
variables_forced = [False] * nbvar
stack = [] 

merged = list(itertools.chain.from_iterable(clauses))
unique = set(merged)


def get_sign(x):
    if x > 0:
        return 1
    else:
        return -1


def remove_pure(clauses):
    unassigned_variables = [v for v in unique if variables[v * get_sign(v) - 1] == UNKNOWN]

    for num in unassigned_variables:
        if (-num not in unassigned_variables):
            sign = get_sign(num)
            num *= sign
            assign(num - 1, sign)


def assign(var_number, value = None):
    if not 0 <= var_number < len(variables):
        raise ValueError("var_number is out of bounds")

    if variables[var_number] != UNKNOWN and value is None:
        raise ValueError("already assigned")

    if value is None:
        variables[var_number] = TRUE
    else:  # forced assignment
        if value not in range(-1, 2, 2):  # [-1, 1]
            raise ValueError("value is out of bounds")
        variables[var_number] = value
        variables_forced[var_number] = True

    stack.append(var_number)


def resolve_conflict():
    if len(stack) == 0:
        return False

    flag = False

    while len(stack) > 0:
        last = stack.pop()
        if variables_forced[last]: 
            variables_forced[last] = False
            variables[last] = UNKNOWN
        else:
            flag = True
            break

    if flag:
        assign(last, variables[last] * -1)  # swap variable
        return True
    else:
        return False  # all variables were forced, nothing to swap, conflict cannot be resolved


var_changed = bool()


def clause_satisfied(clause):
    unknown_counter = 0

    for num in clause:  # num = number of variable (1 = x1, 2 = x2, ..)
        if num == 0:
            raise ValueError("clause cannot contain zeros")
        sign = get_sign(num)
        num *= sign   # make num positive to serve as an index
        if variables[num - 1] == sign:  # if variable №num is assigned and it is TRUE
            return TRUE  # than the whole clause is satisfied (cause it's disjunction)

        if variables[num - 1] == UNKNOWN:
            unknown_counter += 1
            last_unknown = num - 1
            last_unknown_sign = sign

    if unknown_counter == 0:  # if all variables are false
        return FALSE
    else:
        if unknown_counter == 1:
            assign(last_unknown, last_unknown_sign)  # unit propagation
            global var_changed
            var_changed = True
            return TRUE

        return UNKNOWN


def satisfied():
    finished = True

    remove_pure(clauses)

    for clause in clauses:
        it_is_satisfied = clause_satisfied(clause)

        if it_is_satisfied == FALSE:
            if resolve_conflict():
                return satisfied()  # conflict resolved, conflict variable flipped, check again
            else:
                return FALSE

        if it_is_satisfied == UNKNOWN:
            finished = False

    if finished:
        return TRUE
    else:
        return UNKNOWN


def check_sat():
    global var_changed
    var_changed = False
    sat = satisfied()

    if sat == TRUE:
        result = [TRUE if v == UNKNOWN else v for v in variables]
        print ("v"),
        for x in range(nbvar):
            print ((x + 1) * result[x])
        print (0)
        print ("SATISFIABLE")
        exit()

    if sat == FALSE:
        print ("UNSATISFIABLE")
        exit()

    if var_changed:
        check_sat()


def signal_handler(signal_number, frame):
    print("UNKNOWN")
    exit()

signal.signal(signal.SIGINT, signal_handler)

check_sat()
while True:
    for i in range(nbvar):
        if variables[i] != UNKNOWN:
            continue
        assign(i)
        check_sat()

