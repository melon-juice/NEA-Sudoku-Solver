from my_libraries.UNICODEformatting import display as UnicodeDisplay
from my_libraries.StackClass import Stack
from my_libraries.GridArchive import SudokuGrids # imports different empty grids that can be tested when debugging
import copy # used to store *multiple solutions* for a particular sudoku grid input

# This file solves a sudoku grid inputted, provided that:
### The grid is passed in as a 2D list
### The 'blank' squares are denoted by 0
    
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
    return True

def dfs_solution_finder(grid, edits_counter, backtracks_counter, solved_grids): # default state of recursive_call causes initialiation
    """recursive function to solve sudoku grid"""

    found_valid_move=False

    for row_index in range(9):
        for col_index in range(9):
            if grid[row_index][col_index]==0: #if the square is empty
                                
                for i in range(1,10):
                    if allowed(grid,y=row_index,x=col_index,test_num=i):
                    
                        grid[row_index][col_index]=i # the algorithm commits the first *valid* change detected
                        edits_counter[0]+=1
                        found_valid_move=True
                        dfs_solution_finder(grid, edits_counter, backtracks_counter, solved_grids) # recursive call
                        grid[row_index][col_index]=0

                    if not found_valid_move:
                        backtracks_counter[0]+=1

                return # IMPORTANT: exits the recursive call after trying all valid inputs
    
    # if the algorithm reaches this point, it means a solution has been found!
    solved_grids.append(copy.deepcopy(grid))
                    
 
def main():
    """calls dfs_solution_finder()"""
    
    sudoku_grid=SudokuGrids(13)
    print("You entered:")
    UnicodeDisplay(sudoku_grid)
    solutions_list=[]
    edits_counter=[0] # mutable global variable
    backtracks_counter=[0]
    dfs_solution_finder(sudoku_grid, edits_counter, backtracks_counter, solutions_list)

    print(edits_counter[0],"edits were made, and",backtracks_counter[0],"backtracks were made.")
    if len(solutions_list)==0:
        print("No Solutions were found for this puzzle!")
    else:
        print(f"Total solutions found: {len(solutions_list)}")
        for solution in solutions_list:
            UnicodeDisplay(solution)
    
main()
