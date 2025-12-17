
# This file solves a sudoku grid inputted, provided that:
### The grid is passed in as a 2D list
### The 'blank' squares are denoted by 0
### The inputted sudoku grid is solveable

sudoku_grid=[[0,0,0,0,0,7,5,0,0],
            [7,0,0,1,0,0,0,4,0],
            [5,0,0,0,0,0,2,0,0],
            [0,0,1,3,9,0,0,0,8],
            [3,0,0,7,8,6,0,0,4],
            [8,0,0,0,4,1,7,0,0],
            [0,0,8,0,0,0,0,0,9],
            [0,5,0,0,0,3,0,0,1],
            [0,0,4,6,0,0,0,0,0]] # can input a different grid here

class Stack:
    """ Stack class used to stack up attempts.
    If a conflict is found in main(), then the stack is popped to restore the previous commit"""

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
    
def allowed(x,y,test_num):
    #checks for conflicts with rows and columns
    #returns boolean TRUE if test_num can be in (x,y) else FALSE
    #'message' variable stores a string that can be returned during debugging

    if grid[y][x]!=0: #this is redundant, as the main() code already performs a presence check.
        message="Selected square occupied."
        return False
    for i in range(0,9):
        if grid[y][i]==test_num: #if any space in the row already takes on n
            message=f"Conflict found in row at: ({y},{i})"
            return False
    for i in range(0,9):
        if grid[i][x]==test_num: #if any space in the column already takes on n
            message=f"Conflict found in column at: ({i},{x})"
            return False

    x_nought=(x//3)*3 #lowest value of x within the same square
    y_nought=(y//3)*3 #lowest value of y within the same square

    for i in range(0,3):
        for j in range(0,3):
            if grid[y_nought+i][x_nought+j]==test_num: # if any space in the square already takes on n
                message="Conflict found in square"
                return False
    message="No conflicts found!"
    return True

def dfs_solution_finder(grid, recursive_call=False): # default set to begin at (0,0) and no commits
    """recursive function to solve sudoku grid"""
    
    if not recursive_call:
        grid_state=Stack() # instatiation of a stack
        solved_grids=[] # creates list of solutions, currently empty
    grid_state.push(grid) # push current grid state

    print(grid_state.peek()) #used for debugging

    for row in grid:
        for col in row:
            if grid[row][col]==0:
                                
                for i in range(1,10):
                    if allowed(y=row,x=col,test_num=i):
                        
                        grid[row][col]=i # commits the first valid change detected
                        dfs_solution_finder(grid,[row,col],True)
                        grid[row][col]=0

                return #exits the recursive call after trying all valid inputs
    
    solved_grids.append(grid)
                    
                
                    
                        

def main():
    """calls dfs_solution_finder()"""
    dfs_solution_finder(sudoku_grid)
    #add new solution to the list of solutions????

main()
   

#procedure dfs(vertex v){
##visit(v); #so like add a new number to the grid (provided it is valid)
##for each neighbor u of v #if we look at the stack and the [0,1] index #make alist of valid numbers
##positions point to a vertex we have already vsiited, then we knowwwwww
##if u is undiscovered
##call dfs(u);}

# def dfs(graph, start, visited=None):
# if visited is None:
# visited = set()
# visited.add(start)
# print(start)
# for next in graph[start] - visited:
# dfs(graph, next, visited)
# return visited
"""The time complexity of DFS is O(V + E), where V is the number of vertices and E is the number of edges. 
The space complexity is O(V) due to the extra space required for the visited list 
and the stack in the recursive implementation."""
