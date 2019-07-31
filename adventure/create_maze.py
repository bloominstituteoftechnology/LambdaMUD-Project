import random
import math

class Room:
    def __init__(self,i,j):
        self.i = i # Row
        self.j = j # Column
        self.north = True # True == Wall
        self.east = True # False == Wall
        self.south = True
        self.west = True
        self.visited = False

    def __repr__(self):
        return f"north:{self.north} east:{self.east} south:{self.south} west:{self.west}\n"

class Maze:
    def __init__(self,columns):
        self.columns = columns
        self.grid = []
        self.current = None
        self.gen_grid()
        self.gen_maze()

    def gen_grid(self):
        for i in range(self.columns):
            for j in range(self.columns):
                self.grid.append(Room(j,i))
        self.current = self.grid[0]

    def gen_maze(self):
        stack = []
        self.current.visited = True
        next_cell = self.check_neighboor()
        next_cell.visited = True
        stack.append(self.current)
        self.remove_walls(self.current,next_cell)
        self.current = next_cell
        def dfs():
            nonlocal stack
            if len(stack) == 0:
                return
            else:         
                next_cell = self.check_neighboor()
                if next_cell:
                    next_cell.visited = True
                    stack.append(self.current)
                    self.remove_walls(self.current,next_cell)

                    self.current = next_cell
                elif len(stack) > 0:
                    self.current = stack.pop()
                dfs()
        dfs()


    def remove_walls(self,a,b):
        x = a.i - b.i
        if x == 1:
            a.west = False
            b.east = False
        elif x == -1:
            a.east = False
            b.west = False

        y = a.j - b.j
        if y == 1:
            a.north = False
            b.south = False
        elif y == -1:
            a.south = False
            b.north = False

    def index_finder(self,i,j):
        if i < 0 or j < 0 or i > self.columns-1 or j > self.columns-1:
            return None
        else:
            return i + j * self.columns


    def check_neighboor(self):
        neighbors = []

        i = self.current.i 
        j = self.current.j

        top    = self.grid[self.index_finder(i, j - 1)] if self.index_finder(i, j - 1) else None
        right  = self.grid[self.index_finder(i + 1, j)] if self.index_finder(i + 1, j) else None
        bottom = self.grid[self.index_finder(i, j + 1)] if self.index_finder(i, j + 1) else None
        left   = self.grid[self.index_finder(i - 1, j)] if self.index_finder(i - 1, j) else None

        if top and not top.visited:
            neighbors.append(top)
        
        if right and not right.visited:
            neighbors.append(right)
        
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        
        if left and not left.visited:
            neighbors.append(left)
        
        if len(neighbors) > 0:
            r = math.floor(random.randint(0, len(neighbors)-1))
            return neighbors[r]
        else:
            return None
