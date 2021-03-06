import sys
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from functools import partial
from sys import stderr, stdin
import csp
import kenken

# @ product: creation of the variables' domains
# @ permutations: determine the satisfiability of an operation
from itertools import product, permutations

# @ reduce: determine the result of an operation
from functools import reduce
from random import seed, random, shuffle, randint, choice,randint
from time import time

# @ writer: output benchmarking data in a csv format
from csv import writer
# arguments
debugmode = sys.argv[1]

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
        self.t1 = 0
        self.t2 = 0
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

        self.btn_exit.pack(side=BOTTOM, fill=X, expand=YES)
        self.btn_next.pack(side=BOTTOM, fill=X, expand=YES)
        self.btn_quit.pack(side=BOTTOM, fill=X, expand=YES)
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
    
    def surrend(self, event):
        """ Shows the solution to the user if gives up on current puzzle """
        #solution = self.kenken.surrender(self.counter)  # Calls the surrender method of the KenKen object
        #solution = self.g.generate()
        # Display the solution to the user
        for row in range(len(self.solution)):
            for column in range(len(self.solution)):
                self.w.itemconfigure(self.numbers[row][column], text=self.solution[row][column])
    
    def modesolver(self):
        ken = kenken.Kenken(self.size, self.cliques)

        if self.mode == 1:
            print("Using BT algorithm to solve the puzzle")
            #print()
            self.t1 = time() 
            assignment = csp.backtracking_search(ken)
            self.t2 = time()
            #print(assignment)
            l= ken.display(assignment)   

        	
        elif self.mode == 2:
            print("Using FC algorithm to solve the puzzle")
            #print()
            self.t1 = time() 
            assignment = csp.backtracking_search(ken,inference=csp.forward_checking)
            self.t2 = time() 
            #print(assignment)
            l = ken.display(assignment)
        elif self.mode == 3:        
            print("Using MAC algorithm to solve the puzzle")
            #print()
            self.t1 = time() 
            assignment = csp.backtracking_search(ken,inference=csp.mac)
            self.t2 = time() 
            #print(assignment)
            l = ken.display(assignment)
            #print("l is" + str(l))
        else:
            print("Error in selected algorithm!!!!")
        return l

    def solve(self, event):
        """ Shows the solution to the user if gives up on current puzzle """
        #solution = self.kenken.surrender(self.counter)  # Calls the surrender method of the KenKen object
        #solution = self.g.generate()
        # Display the solution to the user
        index = 0
        x = self.modesolver()
        for row in range(self.size):
            for column in range(self.size):
                #print("iterator in x" + str(x[index]))
                #print(str(index))
                #print("column" + str(column) )
                self.w.itemconfigure(self.numbers[row][column], text=x[index])
                index += 1

    def next(self, event):
        self.root.destroy()
        root2 = Tk()  # Initializes the root menu for game to appear
        root2.title("Set size and mode")
        root2.geometry("650x710")
        ff = pre_Gui(root2)

        var1 = IntVar()
        size2, var1 = ff.i(var1)  # Initializes the graphics to display the game
        # print(size)
        root2.mainloop()  # Runs the game

        root3 = Tk()  # Initializes the root menu for game to appear
        root3.title("KenKen")
        root3.geometry("650x710")
        fff = TheGUI(root3, int(size2.get()), var1.get())  # Initializes the graphics to display the game
        # f1.create_widgets()

        root3.mainloop()  # Runs the game
         
 # first gui 
 

class pre_Gui(Frame):
    def __init__(self, master):
        """ Initializes the GUI for KenKen Game """
        self.root = master
        Frame.__init__(self, master)  # Creates the frame
        # Creates the canvas that will display the game
        self.w = Canvas(master, width=1002, height=1003)
        self.var = IntVar()
        self.w.pack()
        self.pack()

    #**not used ** function used to be called in set button
    def storeSize(num1):
        n1 = int(num1.get())
        #print("first" + str(n1))
        return n1

    def i(self,var):
        number1 = StringVar()
        self.var=var
        l1 = Label(self.root, text="Enter the size of KenKen").place(x=20, y=60)
        t1 = Entry(self.root, textvariable=number1).place(x=200, y=60)

       #for set button
       # returnSize = partial(storeSize, number1)
       # b1 = Button(root, text="Set", command=returnSize).place(x=200, y=300)

        b2 = Button(self.root, text="Continue", command=self.root.destroy).place(x=250, y=300)

        self.r1 = Radiobutton(self.root, text="Backtracking", variable=self.var, value=1, command=self.viewSelected).place(x=100, y=160)
        self.r2 = Radiobutton(self.root, text="Backtracking with forward checking", variable=self.var, value=2,command=self.viewSelected).place(x=100, y=180)
        self.r3 = Radiobutton(self.root, text="Backtracking with arc consistency", variable=self.var, value=3,command=self.viewSelected).place(x=100, y=200)

        return number1 , self.var


    def viewSelected(self):
        choice  = self.var.get()
        selected = 0
        if choice == 1:
            output = "Backtracking"
            selected = 1
        elif choice == 2:
            output =  "Backtracking with forward checking"
            selected = 2
        elif choice == 3:
            output =  "Backtracking with arc consistency"
            selected = 3
        else:
            output = "Invalid selection"
        #return messagebox.showinfo('PythonGuides', f'You Selected {output}.'), self.var
        return self.var

# class generator
class Generator():
    def __init__(self, a):
        self.size = a
        self.cliques =[]
        self.solution = self.generate()
    def adjacent(self,xy1, xy2):
        """
        Checks wheither two positions represented in 2D coordinates are adjacent
        """
        x1, y1 = xy1
        x2, y2 = xy2

        dx, dy = x1 - x2, y1 - y2

        return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)

    def operation(self,operator):
        """
        A utility function used in order to determine the operation corresponding
        to the operator that is given in string format
        """
        if operator == '+':
            return lambda a, b: a + b
        elif operator == '-':
            return lambda a, b: abs(a - b)
        elif operator == '*':
            return lambda a, b: a * b
        elif operator == '/':
            return lambda a, b: a / b
        else:
            return None

    def generate(self):
        board = [[((i + j) % self.size) + 1 for i in range(self.size)] for j in range(self.size)]
        for _ in range(self.size):
            shuffle(board)
        for c1 in range(self.size):
            for c2 in range(self.size):
                if random() > 0.5:
                    for r in range(self.size):
                        board[r][c1], board[r][c2] = board[r][c2], board[r][c1]
        solution =board

        # (x,y) value
        # dictionary > key (x,y) : value (no. inside the cell)

        board = {(j + 1, i + 1): board[i][j] for i in range(self.size) for j in range(self.size)}
        #print (board)
        
        # sorted list of the positions (x,y)
        uncaged = sorted(board.keys(), key=lambda var: var[1])

        # list of cages
        # list of lists
        # target > 50 ope > * taple (1,)
        #self.cliques = []

        while uncaged:

            self.cliques.append([])  # list of list

            csize = randint(1, 4)  # cage size

            cell = uncaged[0]

            uncaged.remove(cell)

            self.cliques[-1].append(cell)

            for _ in range(csize - 1):  # belf random times

                adjs = [other for other in uncaged if self.adjacent(cell, other)]  # list of all adjacents to cell

                cell = choice(adjs) if adjs else None

                if not cell:
                    break

                uncaged.remove(cell)

                self.cliques[-1].append(cell)

            csize = len(self.cliques[-1])
            if csize == 1:
                cell = self.cliques[-1][0]
                self.cliques[-1] = ((cell,), '.', board[cell])
                continue
            elif csize == 2:
                fst, snd = self.cliques[-1][0], self.cliques[-1][1]
                if board[fst] / board[snd] > 0 and not board[fst] % board[snd]:
                    operator = "/"  # choice("+-*/")
                else:
                    operator = "-"  # choice("+-*")
            else:
                operator = choice("+*")

            target = reduce(self.operation(operator), [board[cell] for cell in self.cliques[-1]])

            self.cliques[-1] = (tuple(self.cliques[-1]), operator, int(target))

        #print (self.cliques)

        return solution

    def op_gui(self):
        puzzlelist = []
        cells =[]
        operators =[]
        targets=[]
        #self.generate()
        for i in range(len(self.cliques)):
            members, operator, target = self.cliques[i]
            targets.append(target)
            operators.append(operator)
            for x in range(len(members)):
                if (x == 0):
                    cells.append (members[x])
                  # puzzlelist.append(str(target)+str(operator))
        for i in range(self.size): # row
            for j in range(self.size): #col
                if  (len(cells) > 0) and (j+1,i+1) == cells[0] :
                    temp = cells[0]
                    cells.remove(temp)
                    puzzlelist.append(str(targets[0]) + str(operators[0]))
                    temp2 = operators[0]
                    operators.remove(temp2)
                    temp3 = targets[0]
                    targets.remove(temp3)
                else:
                    puzzlelist.append(' ')


            #print(cells)
        #print (puzzlelist)

        return puzzlelist

# performance 
def performance():
    size = 5
    # generate 100 boards
    gen = []
    for i in range(100):
        gen.append(Generator(size))
    
    t1 = time()
    for i in range(100):
        ken = kenken.Kenken(size, gen[i].cliques)
        assignment = csp.backtracking_search(ken)
    t2 = time()
    print("the backtracking algorithm "+str(t2-t1))
    #################################################
    #the second 
    t1 = time()
    for i in range(100):
        ken = kenken.Kenken(size, gen[i].cliques)
        assignment = csp.backtracking_search(ken,inference=csp.forward_checking)
    t2 = time()
    print("the backtracking with forward checking algorithm "+str(t2-t1))
    ####################################################
    t1 = time()
    for i in range(100):
        ken = kenken.Kenken(size, gen[i].cliques)
        assignment = csp.backtracking_search(ken,inference=csp.mac)
    t2 = time()
    print("the backtracking with arc consistency  algorithm "+str(t2-t1))
if __name__ == '__main__':
    #gather = kenken.gather(10, "kenken.csv")
    print("the debug mode is "+str(debugmode))
    if (debugmode == str(1)):
        performance()

    else:
        #gather(10, "kenken.csv")
        root = Tk()  # Initializes the root menu for game to appear
        root.title("Set size and mode")
        root.geometry("650x710")
        f=pre_Gui(root)
        
        var = IntVar()
        size , var = f.i(var)  # Initializes the graphics to display the game
        #print(size)
        root.mainloop()  # Runs the game

        root1 = Tk()  # Initializes the root menu for game to appear
        root1.title("KenKen")
        root1.geometry("650x710")
        f1 = TheGUI(root1,int(size.get()),var.get())  # Initializes the graphics to display the game
        #f1.create_widgets()

        root1.mainloop()  # Runs the game










