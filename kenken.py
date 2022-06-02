import csp 
import main 
from sys import stderr, stdin
from itertools import product, permutations
from functools import reduce
from random import seed, random, shuffle, randint, choice
from time import time
# @ writer: output benchmarking data in a csv format
from csv import writer

#########################################
# functions:
def parse(lines):
    # to parse the entered puzzle " user puzzle not the generated one"

    if isinstance(lines, str):
        lines = lines.splitlines(True)

    try:
        content = lines[0][:-1]
        size = int(content)
    except:
        print("Unable to determine board size [", content, "]", file=stderr)
        exit(11)

    cliques = []
    for line in lines[1:]:
        content = line[:-1]
        if content:
            try:
                clique = eval(content)
                cliques.append(clique)
            except:
                print("Malformed clique [", content, "]")
                exit(12)

    return size, cliques

def validate(size, cliques):

    outOfBounds = lambda xy: xy[0] < 1 or xy[0] > size or xy[1] < 1 or xy[1] > size

    mentioned = set()
    for i in range(len(cliques)):
        members, operator, target = cliques[i]

        cliques[i] = (tuple(set(members)), operator, target)

        members, operator, target = cliques[i]

        if operator not in "+-*/.":
            print("Operation", operator, "of clique", cliques[i], "is unacceptable", file=stderr)
            exit(1)

        problematic = list(filter(outOfBounds, members))
        if problematic:
            print("Members", problematic, "of clique", cliques[i], "are out of bounds", file=stderr)
            exit(2)

        problematic = mentioned.intersection(set(members))
        if problematic:
            print("Members", problematic, "of clique", cliques[i], "are cross referenced", file=stderr)
            exit(3)

        mentioned.update(set(members))

    indexes = range(1, size + 1)

    problematic = set([(x, y) for y in indexes for x in indexes]).difference(mentioned)

    if problematic:
        print("Positions", problematic, "were not mentioned in any clique", file=stderr)
        exit(4)
def RowXorCol(xy1, xy2):

    return (xy1[0] == xy2[0]) != (xy1[1] == xy2[1])
def conflicting(A, a, B, b):

    for i in range(len(A)):
        for j in range(len(B)):
            mA = A[i]
            mB = B[j]

            ma = a[i]
            mb = b[j]
            if RowXorCol(mA, mB) and ma == mb:
                return True

    return False
def satisfies(values, operation, target):

    for p in permutations(values):
        if reduce(operation, p) == target:
            return True

    return False

# operation
def operation(operator):
    """
    return the operation 
    """
    if operator == '+':
        return lambda a, b: a + b
    elif operator == '-':
        return lambda a, b: a - b
    elif operator == '*':
        return lambda a, b: a * b
    elif operator == '/':
        return lambda a, b: a / b
    else:
        return None 