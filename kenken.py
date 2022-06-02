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