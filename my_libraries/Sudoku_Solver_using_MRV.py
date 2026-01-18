import copy # used to store *multiple solutions* for a particular sudoku grid input

# This file solves a sudoku grid inputted, provided that:
### The grid is passed in as a 2D list
### The 'blank' squares are denoted by 0

def UnicodeDisplay(grid):
    board=[]
    for row in range(9):
        for col in range(9):
            if grid[row][col]==0:
                board.append(" ")
            else:
                board.append(grid[row][col])

    thickdash=3*"\u2550"
    thindash=3*"\u2500"

    print("\u2554"+3*(thickdash+"\u2564"+thickdash+"\u2564"+thickdash+"\u2557"),
    "\n\u2551",board[0],"\u2502",board[1],"\u2502", board[2],"\u2551",board[3],"\u2502",board[4],"\u2502",board[5],"\u2551",board[6],"\u2502",board[7],"\u2502",board[8],"\u2551",
    "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u2562"),
    "\n\u2551",board[9],"\u2502",board[10],"\u2502", board[11],"\u2551",board[12],"\u2502",board[13],"\u2502",board[14],"\u2551",board[15],"\u2502",board[16],"\u2502",board[17],"\u2551",
    "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u2562"),
    "\n\u2551",board[18],"\u2502",board[19],"\u2502", board[20],"\u2551",board[21],"\u2502",board[22],"\u2502",board[23],"\u2551",board[24],"\u2502",board[25],"\u2502",board[26],"\u2551",
    "\n\u2560"+3*(thickdash+"\u256A"+thickdash+"\u256A"+thickdash+"\u2563"),
        
    "\n\u2551",board[27],"\u2502",board[28],"\u2502", board[29],"\u2551",board[30],"\u2502",board[31],"\u2502",board[32],"\u2551",board[33],"\u2502",board[34],"\u2502",board[35],"\u2551",
    "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u2562"),
    "\n\u2551",board[36],"\u2502",board[37],"\u2502", board[38],"\u2551",board[39],"\u2502",board[40],"\u2502",board[41],"\u2551",board[42],"\u2502",board[43],"\u2502",board[44],"\u2551",
    "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u2562"),
    "\n\u2551",board[45],"\u2502",board[46],"\u2502", board[47],"\u2551",board[48],"\u2502",board[49],"\u2502",board[50],"\u2551",board[51],"\u2502",board[52],"\u2502",board[53],"\u2551",
    "\n\u2560"+3*(thickdash+"\u256A"+thickdash+"\u256A"+thickdash+"\u2563"),

    "\n\u2551",board[54],"\u2502",board[55],"\u2502", board[56],"\u2551",board[57],"\u2502",board[58],"\u2502",board[59],"\u2551",board[60],"\u2502",board[61],"\u2502",board[62],"\u2551",
    "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u2562"),
    "\n\u2551",board[63],"\u2502",board[64],"\u2502", board[65],"\u2551",board[66],"\u2502",board[67],"\u2502",board[68],"\u2551",board[69],"\u2502",board[70],"\u2502",board[71],"\u2551",
    "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u2562"),
    "\n\u2551",board[72],"\u2502",board[73],"\u2502", board[74],"\u2551",board[75],"\u2502",board[76],"\u2502",board[77],"\u2551",board[78],"\u2502",board[79],"\u2502",board[80],"\u2551",
    "\n\u255A"+3*(thickdash+"\u2567"+thickdash+"\u2567"+thickdash+"\u255D"))

def convert_grid(grid):
    """converts format of grid between array (used during algorithm implementation) and single line (for storage)"""

    if type(grid)==list: # 2d array -> single line
        single_line=""
        for row in grid:
            for element in row:
                single_line+=str(element)
        return single_line

    else: # single line -> 2d array
        grid_list=[[],[],[],[],[],[],[],[],[]]
        for i in range(9):
            j=i*9
            for digit in grid[j+0:j+9]:
                grid_list[i].append(int(digit))

        return grid_list

def MRV_cell(grid):
    """Finds the best next coordinate for the dfs_solution_finder function,
    by trying to find the cell that has the lowest allowed_count.
    This is done by improving lowest_options to the lowest it can be."""
    
    best_square=None
    lowest_options=10 # The function seeks an advancement/improvement on this number (lowest_options can be set to anything above 9)

    for row_index in range(9):
        for col_index in range(9):
            if grid[row_index][col_index]==0:
                
                allowed_count=0
                for i in range(1, 10):
                    if allowed(grid,y=row_index,x=col_index,test_num=i):
                        allowed_count+=1
                
                if allowed_count<lowest_options:
                    lowest_options=allowed_count
                    best_square=(row_index,col_index)
                
                ###print("The best square is",best_square,"with",lowest_options,"options") # used for debugging

                # if a square has only 1 option, take it immediately
                if lowest_options==1:
                    return best_square
                    
    return best_square

def allowed(grid,x,y,test_num):
    #checks for conflicts with rows and columns
    #returns boolean TRUE if test_num can be in (x,y) else FALSE
    #'message' variable stores a string that can be returned during debugging

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
    return True # I can also return message when debugging

def dfs_solution_finder(grid, solved_grids): # default state of recursive_call causes initialiation
    """recursive function to solve sudoku grid"""

    next_square=MRV_cell(grid) ###
    if not next_square: # if nothing was returned by MRV_cell() function, then there are no empty squares left
        solved_grids.append(copy.deepcopy(grid)) # (a solution has been found!)
        return
    row_index,col_index=next_square

    for i in range(1,10):
        if allowed(grid,y=row_index,x=col_index,test_num=i):
            
            grid[row_index][col_index]=i # the algorithm commits a change for the square specified by the MRV_cell() function
            dfs_solution_finder(grid, solved_grids) # recursive call

            grid[row_index][col_index]=0 # cell set to empty again (backtracking occurs)
    
def main(sudoku_grid): # external input here

    """calls dfs_solution_finder()"""
    solutions_list=[] # mutable global list
    dfs_solution_finder(sudoku_grid, solutions_list)
    return solutions_list

