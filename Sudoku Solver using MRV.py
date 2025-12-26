from my_libraries.UNICODEformatting import display as UnicodeDisplay
from my_libraries.StackClass import Stack
from my_libraries.GridArchive import SudokuGrids # imports different empty grids that can be tested when debugging
import copy # used to store *multiple solutions* for a particular sudoku grid input

# This file solves a sudoku grid inputted, provided that:
### The grid is passed in as a 2D list
### The 'blank' squares are denoted by 0

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
                
                #########print("The best square is",best_square,"with",lowest_options,"options")

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
    return True

def dfs_solution_finder(grid, edits_counter, backtracks_counter, solved_grids): # default state of recursive_call causes initialiation
    """recursive function to solve sudoku grid"""

    next_square=MRV_cell(grid) ###
    if not next_square: # if nothing was returned by MRV_cell() function, then there are no empty squares left
        solved_grids.append(copy.deepcopy(grid)) # (a solution has been found!)
        return

    row_index,col_index=next_square
    found_valid_move=False ###

    for i in range(1,10):
        if allowed(grid,y=row_index,x=col_index,test_num=i):
            
            grid[row_index][col_index]=i # the algorithm commits a change for the square specified by the MRV_cell() function
            edits_counter[0]+=1
            found_valid_move=True
            dfs_solution_finder(grid, edits_counter, backtracks_counter, solved_grids) # recursive call

            grid[row_index][col_index]=0 # cell set to empty again (backtracking occurs)
        
        if not found_valid_move:
            backtracks_counter[0]+=1
    
def main():
    """calls dfs_solution_finder()"""
    sudoku_grid=SudokuGrids(1)
    print("You entered:")
    UnicodeDisplay(sudoku_grid)
    solutions_list=[]

    backtracks_counter=[0]
    edits_counter=[0] # mutable global variables

    dfs_solution_finder(sudoku_grid, edits_counter, backtracks_counter, solutions_list)

    print(edits_counter[0],"edits were made, and",backtracks_counter[0],"backtracks were made.")
    if len(solutions_list)==0:
        print("No Solutions were found for this puzzle!")
    else:
        print(f"Total solutions found: {len(solutions_list)}")
        for solution in solutions_list:
            UnicodeDisplay(solution)
    

main()
