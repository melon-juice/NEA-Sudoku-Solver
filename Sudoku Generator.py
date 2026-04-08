#from my_libraries.converter_grid_format import convert_grid
from my_libraries.Sudoku_Solver_using_MRV import main as solve_sudoku_MRV # used to check grid is solveable
from my_libraries.UNICODEformatting import display as UnicodeDisplay
from my_libraries.GridArchive import SudokuGrids

import random # used to remove random cells from the solved grid
              # used to randomly substitute/swap numbers

def number_shuffle(grid):
    """Each number in the input grid is swapped with a random number 1-9 (it may be kept the same)
    This is done to make the grid feel slightly different to the human solver"""

    old_list=[1, 2, 3, 4, 5, 6, 7, 8, 9]
    new_list=random.sample(old_list,k=9) # new_list is a different shuffle each time. eg: [6, 1, 9, 4, 8, 5, 2, 7, 3]

    print("\n\tEach            ",old_list)
    print("\tIs replaced with",new_list,"\n")


    for row_index in range(9):
        for col_index in range(9):
            
            digit=grid[row_index][col_index]
            if digit!=0:
                new_num=new_list[old_list.index(digit)]
                grid[row_index][col_index]=new_num # swaps old number with corresponding new number
 
    return grid

def generate_sudoku(full_grid, difficulty):
    """Random cells are removed from the sudoku grid until it has as few digits as possible whislt still having exactly 1 solution."""

    if difficulty=="easy":
        iterations=43
    elif difficulty=="medium":
        iterations=random.randint(44,52)
    elif difficulty=="hard":
        iterations=random.randint(53,59)
    #print(f"There are {iterations} blank cells.")

    grid=full_grid # a copy is made in case the algorithm needs to reference / revert to the full grid

    for i in range(iterations):

        num_temp=0
        # generate random coordinates
        while num_temp==0:
            row=random.randint(0,8)
            column=random.randint(0,8)
            num_temp=grid[row][column]

        grid[row][column]=0 # this coordinate is switched for an empty cell

        solutions=solve_sudoku_MRV(grid)
        if len(solutions)!=1:
            #print("Not solveable, iteration no.",i) # used for debugging
            grid[row][column]=num_temp # cell is changed back
            iterations+=1 # iterations is incremented again
            
    return grid

##def main():
##    archive_num=random.randint(3,25)
##    random_unsolved_grid=SudokuGrids(archive_num)
##    grid=solve_sudoku_MRV(random_unsolved_grid)[0] # retrieves a random unsolved sudoku from my grid archive and solves it
##    return generate_sudoku(grid,"easy")

# remove the following: it is just for debugging

archive_num=random.randint(3,25)
random_unsolved_grid=SudokuGrids(archive_num)
grid=solve_sudoku_MRV(random_unsolved_grid)[0] # retrieves a random unsolved sudoku from my grid archive and solves it

print("\nBefore Number Shuffle:")
new=generate_sudoku(grid,"easy")
UnicodeDisplay(new)

print("\nAfter Number Shuffle:")
shuffled=number_shuffle(new)
UnicodeDisplay(shuffled)
