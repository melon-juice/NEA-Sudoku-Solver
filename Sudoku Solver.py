
#INCOMPLETE:
#This file solves a sudoku grid inputted, provided that:
###The grid is passed in as a 2D list
###The 'blank' squares are denoted by 0
###The inputted sudoku grid is solveable

global sudoku_grid = [[0,0,0,0,0,7,5,0,0],
                      [7,0,0,1,0,0,0,4,0],
                      [5,0,0,0,0,0,2,0,0],
                      [0,0,1,3,9,0,0,0,8],
                      [3,0,0,7,8,6,0,0,4],
                      [8,0,0,0,4,1,7,0,0],
                      [0,0,8,0,0,0,0,0,9],
                      [0,5,0,0,0,3,0,0,1],
                      [0,0,4,6,0,0,0,0,0]] #grid here

class stack:
    
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
    
    #used to stack up attempts
    #if a conflict is found in main(),
        #then the stack is popped to restore the previous commit
    

def allowed(y,x,test_num):
    #checks for conflicts with rows and columns
    #returns boolean TRUE if test_num can be in (x,y) else FALSE
    pass

def dfs_solution_finder():
    new_solution=stack()
    
    for row in sudoku_grid:
        for col in row:
            if sudoku_grid[row][col]==0:
                for i in range(0,9):
                    if allowed(row,col,i):
                        sudoku_grid[row][col]=i #if allowed then commit
                        new_solution.push([row,col,i])
                if sudoku_grid[row][col]==0:
                    new_solution.pop()
                        

def main():
   #call dfs_solution_finder()
   #add new solution to the list of solutions

main()
   

#procedure dfs(vertex v){
##visit(v);
##for each neighbor u of v #if we look at teh stack and the [0,1] index
##positions point to a vertex we have already vsiited, then we knowwwwww
##if u is undiscovered
##call dfs(u);}
