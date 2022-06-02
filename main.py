from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from functools import partial
from sys import stderr, stdin
import csp
import rename

# @ product: creation of the variables' domains
# @ permutations: determine the satisfiability of an operation
from itertools import product, permutations

# @ reduce: determine the result of an operation
from functools import reduce
from random import seed, random, shuffle, randint, choice,randint
from time import time

# @ writer: output benchmarking data in a csv format
from csv import writer