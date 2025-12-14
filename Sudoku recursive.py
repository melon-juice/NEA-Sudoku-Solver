class Stack:
    
   def __init__(self):
        self.maxSize=60
        self.s=[None]*self.maxSize
        self.tosp=-1 #initialised as empty
        self.size=0

    def isEmpty(self):
        if self.size==0:
            return True
        return False

    def isFull(self):
        if self.size>=self.maxSize:
            return True
        return False

    def push(self,data):
        if self.isFull:
            self.tosp+=1
            self.s[self.tosp]=data
            self.size+=1
        else:
            print("Stack full- cannot add anything")

    def pop(self):
        if not self.isEmpty:
            data=self.s[self.tosp]
            del(data)
            self.tosp-=1
            self.size-=1
            return data
        else:
            print("Stack empty- nothing to pop")

    def find_size(self):
        return self.size

    def peek(self):
        return self.s[self.tosp]

def dfs_solution_finder():
    discovered_squares=[]
    stack=Stack()



    for row in sudoku_grid:
        for col in row:
            
            if sudoku_grid[row][col]==0:
                #adds square coordinates to 'discovered' list:
                discovered_squares.append([row,col])
                conflicts=0
                
                for i in range(1,9):
                    possible=allowed(row,col,i) #boolean value
                    if possible:
                        #the grid is updated and...
                        sudoku_grid[row][col]=i
                        #information about the change is pushed onto stack
                        new_solution.push([row,col,i])
                    else:
                        conflicts+=1
                if conflicts==9:
                    #backtrack
                    
    return sudoku_grid
