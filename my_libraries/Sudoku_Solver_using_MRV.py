import pickle # file handling: used to store multiple solutions for a particular sudoku grid input
import os # used to import ListOfSolutions pickle (binary) file
library_directory=os.path.dirname(os.path.abspath(__file__))
absolute_path_to_solutions_list=os.path.join(library_directory, "ListOfSolutions.pkl")

def MRV_cell(grid):
    """This function finds the best next coordinate for the dfs_solution_finder,
    by identifying the cell in the grid that has the most constraints i.e., lowest allowed_count.
    The function does this by iterating through all cells on the board and seeking to improve 'lowest_options' to the lowest it can be.
    This is an implementation of the Minimum Remaining Values heuristic."""
    
    best_square=None
    lowest_options=10 # The function seeks an advancement/improvement on this number
    # (here, lowest_options can be set to anything above 9, and the program will work as expected)

    for row_index in range(9):
        for col_index in range(9):
            if grid[row_index][col_index]==0: # iterates through every empty cell in the grid
                
                allowed_count=0
                for i in range(1, 10):
                    if allowed(grid, y=row_index, x=col_index, test_num=i):
                        allowed_count+=1

                # a more optimal cell is found: one with more contsraints
                if allowed_count<lowest_options: 
                    lowest_options=allowed_count
                    best_square=(row_index, col_index)

                # if a square has only 1 option, take it immediately
                if lowest_options==1:
                    return best_square
                
    return best_square

def allowed(grid, x, y, test_num):
    """This function verifies if 'test_num' is allowed to go in the cell at grid(x)(y) by following this rule:
        'Each row, each column, and each 3×3 block should contain all digits from 1 to 9 (inclusive) exactly once.'
    It does this by checking for conflicts within the corresponding row, column and 3x3 block.
    Boolean TRUE is returned if test_num *can* be in (x,y) and FALSE if it *cannot*."""

    for i in range(0,9):
        if grid[y][i]==test_num: # if any cell in the row already takes on test_num
            return False
    for i in range(0,9):
        if grid[i][x]==test_num: # if any cell in the column already takes on test_num
            return False

    x_nought=(x//3)*3 # lowest value of x within the same square
    y_nought=(y//3)*3 # lowest value of y within the same square

    for i in range(0,3):
        for j in range(0,3):
            if grid[y_nought+i][x_nought+j]==test_num: # if any cell in the 3x3 block already takes on test_num
                return False

    return True  # no conflicts found

def dfs_solution_finder(grid):
    """Recursive function to solve sudoku grid"""

    next_square=MRV_cell(grid)
    if not next_square: # if nothing was returned by MRV_cell() function, then there are no empty squares left
        # ...therefore a solution has been found!
        solved_grids=pickle.load(open(absolute_path_to_solutions_list, "rb"))
        solved_grids.append(grid)
        pickle.dump(solved_grids, open(absolute_path_to_solutions_list, "wb"))
        return
    
    row_index,col_index=next_square

    for i in range(1,10):
        if allowed(grid, y=row_index, x=col_index, test_num=i):
            
            grid[row_index][col_index]=i # the algorithm commits a change for the cell specified by the MRV_cell() function
            dfs_solution_finder(grid) # recursive call

            grid[row_index][col_index]=0 # cell set to empty again (backtracking occurs)
    
def main(sudoku_grid): # external input here
    """calls dfs_solution_finder()"""
    pickle.dump([], open(absolute_path_to_solutions_list, "wb")) # initialised as empty
    dfs_solution_finder(sudoku_grid)
    solved_grids=pickle.load(open(absolute_path_to_solutions_list, "rb"))
    return solved_grids
    
#         print(len(solved_grids))
#         for grid in solved_grids:
#             for line in grid:
#                 print(line)
#             print("...")
    
# main([[5,0,1,0,7,2,0,0,0],
# [6,0,9,0,0,0,0,0,0],
# [8,0,7,5,4,0,6,0,3],
# [4,9,6,0,0,7,8,0,0],
# [0,0,3,0,0,4,0,0,6],
# [2,1,0,0,9,0,0,4,0],
# [0,6,0,0,0,0,0,0,8],
# [0,0,5,0,6,3,4,2,9],
# [0,0,4,0,2,8,5,6,1]])