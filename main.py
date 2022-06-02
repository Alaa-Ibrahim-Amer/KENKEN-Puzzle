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

class TheGUI(Frame):
    def __init__(self, master,a,b):
        """ Initializes the GUI for KenKen Game """
        self.root = master
        Frame.__init__(self, master) #Creates the frame
        # Creates the canvas that will display the game
        self.w = Canvas(master, width=1002, height=1003)
        self.mode = b #selected mode
        self.size = a #selected dimentions
        self.g= Generator(self.size) # create new puzzle
        self.solution = self.g.solution
        self.cliques = self.g.cliques
        self.flag = 1
        self.create_widgets()
        self.pack()
        self.w.pack()

    def create_widgets(self):
        """ Creates the widgets and canvas objects/components of the game in GUI """
        if (self.flag):
            self.w.create_rectangle(6, 6, self.size*100, self.size*100)  # Draws the rectangle onto canvas

        # Creates the puzzle board with all 25 cells in 5x5 grid
        self.sqlist = []


        for i in range(0, self.size*100, 100):
            for j in range(0, self.size*100, 100):
                x = j + 100
                y = i + 100
                self.sqlist.append(self.w.create_rectangle(j, i, x, y))
                #print("/////////")
                #print(j, i, x, y)

                # Display the numbers and operations of puzzle to canvas
        self.currentpuzzle = self.g.op_gui()
        self.boldline()
        x = 25
        y = 20
        for element in self.currentpuzzle:
            self.w.create_text(x, y, font="Arial 20 bold", text=element)
            y += 100

            if y == (self.size * 100 + 20):
                y = 20
                x += 100



        self.numbers = [[((i + j) % self.size) + 1 for i in range(self.size)] for j in range(self.size)]

        x = 50
        y = 60
        for m in range(len(self.numbers)):
            for n in range(len(self.numbers)):
                self.numbers[m][n] = self.w.create_text(x, y, font="Arial 30", text=" ")
                y += 100
            y = 60
            x += 100




        self.buttonlist = []
        self.btn_quit = Button(self, text="Surrender?")
        self.btn_quit.bind("<ButtonRelease-1>", self.surrend)
        self.btn_solve = Button(self, text="Solve with algorithm")
        self.btn_solve.bind("<ButtonRelease-1>", self.solve)
        self.btn_next = Button(self, text="Next Puzzle")
        self.btn_next.bind("<ButtonRelease-1>", self.next)
        self.btn_exit = Button(self, text="Exit")
        self.btn_exit.bind("<ButtonRelease-1>", self.click_Exit)

        self.btn_quit.pack(side=BOTTOM, fill=X, expand=YES)
        self.btn_next.pack(side=BOTTOM, fill=X, expand=YES)
        self.btn_exit.pack(side=BOTTOM, fill=X, expand=YES)
        self.btn_solve.pack(side=BOTTOM, fill=X, expand=YES)
        

        self.buttonlist.append(self.btn_quit)
        self.buttonlist.append(self.btn_next)
        self.buttonlist.append(self.btn_exit)
        self.buttonlist.append(self.btn_solve)

    def color_generate(self):
        colors = ["#d4d1df","#ffb3ba","#ffdfba","#ffffba","#baffc9","#bae1ff","#665D96","#80afa5","#766579","#f9d2fa"]
        return colors

    def boldline (self):
        self.sqlist = []

        for i in range(len(self.cliques)):
            members, operator, target = self.cliques[i]
            color = self.color_generate()
            for x in range(len(members)):
                x,y = members[x]
                p1 =( x - 1 )*100
                p3 = p1 + 100
                p2 = (y-1)*100
                p4 = p2 + 100
                #print("************")
                #print(p1,p2,p3,p4)

                self.sqlist.append(self.w.create_rectangle(p2,p1,p4,p3,fill=color[i%len(color)]))

    def click_Exit(self, event):
        """ Exits the KenKen game """
        exit()
