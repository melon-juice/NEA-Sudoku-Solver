from my_libraries.UNICODEformatting import display
from my_libraries.StackClass import Stack
from my_libraries.GridArchive import SudokuGrids # imports different empty grids that can be tested when debugging
import copy # used to store *multiple solutions* for a particular sudoku grid input

# This file solves a sudoku grid inputted, provided that:
### The grid is passed in as a 2D list
### The 'blank' squares are denoted by 0
### The inputted sudoku grid is solveable
    
def allowed(grid,x,y,test_num):
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

def dfs_solution_finder(grid, solved_grids): # default state of recursive_call causes initialiation
    """recursive function to solve sudoku grid"""

    for row_index in range(9):
        for col_index in range(9):
            if grid[row_index][col_index]==0: #if the square is empty
                                
                for i in range(1,10):
                    if allowed(grid,y=row_index,x=col_index,test_num=i):
                        
                        grid[row_index][col_index]=i # the algorithm commits the first *valid* change detected
                        dfs_solution_finder(grid,solved_grids) # recursive call
                        grid[row_index][col_index]=0

                return # IMPORTANT: exits the recursive call after trying all valid inputs
    
    # if the algorithm reaches this point, it means a solution has been found!
    solved_grids.append(copy.deepcopy(grid))
                    
 
def main():
    """calls dfs_solution_finder()"""
    sudoku_grid=SudokuGrids(0)
    print("You entered:")
    display(sudoku_grid)
    solutions_list=[]
    dfs_solution_finder(sudoku_grid,solutions_list)

    if len(solutions_list)==0:
        print("No Solutions were found for this puzzle!")
    else:
        print(f"Total solutions found: {len(solutions_list)}")
        for solution in solutions_list:
            display(solution)
    

main()

"""The time complexity of DFS is O(V + E), where V is the number of vertices and E is the number of edges. 
The space complexity is O(V) due to the extra space required for the visited list 
and the stack in the recursive implementation."""
