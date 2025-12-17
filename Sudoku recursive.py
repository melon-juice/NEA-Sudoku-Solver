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

def possible(x_coord,y_coord,test_num):

    if grid[y_coord][x_coord]!=0:
        print("Selected square occupied.")
        return False
    
    for i in range(0,9):
        if grid[y_coord][i]==test_num: #if any space in the row already takes on n
            print(f"Conflict found in row at: ({y_coord},{i})")
            return False
    for i in range(0,9):
        if grid[i][x_coord]==test_num: #if any space in the column already takes on n
            print(f"Conflict found in column at: ({i},{x_coord})")
            return False

    x_nought=(x_coord//3)*3 #lowest value of x within the same square
    y_nought=(y_coord//3)*3 #lowest value of y within the same square

    for i in range(0,3):
        for j in range(0,3):
            if grid[y_nought+i][x_nought+j]==test_num: #if any space in the square already takes on n
                print("Conflict found in square")
                return False
    print("No conflicts found!")
    return True



def dfs_solution_finder():
    discovered_squares=[]
    stack=Stack()

    for row in sudoku_grid:
        for col in row:
            
            if sudoku_grid[row][col]==0: #empty square
                #adds square coordinates to 'discovered' list:
                discovered_squares.append([row,col])

                conflicts=0
                for i in range(1,9):
                    allowed=possible(x_coord=col,y_coord=row,test_num=i) #returns a boolean value
                    if allowed:
                        #the grid is updated and...
                        sudoku_grid[row][col]=i
                        #information about the change is pushed onto stack
                        new_solution.push([row,col,i])
                    else:
                        conflicts+=1
                if conflicts==9: #if all possible numbers cause conflicts
                    #backtrack
                   pass
                    
    return sudoku_grid
