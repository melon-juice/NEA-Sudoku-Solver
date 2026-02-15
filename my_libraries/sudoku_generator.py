# imports random, converter_grid_format, and Sudoku_Solver_using_MRV

import random # used to remove random cells from the solved grid
              # used to randomly substitute/swap numbers
from .converter_grid_format import convert_grid
from .Sudoku_Solver_using_MRV import main as solve_sudoku_MRV # used to check grid is solveable

def get_random_grid():
    """Gets a random grid from the archive and converts it to 2d list format"""
    try:
        with open("./SingleStringGridArchive.txt", "r", encoding="utf-8") as file: ########open('./Source/Documents/hello.txt')
            random_line="hello world"
            while len(random_line)!=81: # ensures the random line selected isn't simply a line break with no contents
                random_line=random.choice(file.readlines()).strip() # random line selected
                random_grid=convert_grid(random_line) # grid converted to 2d format
            
        random_solved_grid=solve_sudoku_MRV(random_grid)[0] # attempts to solve grid. If the imported content was corrupted, this line will raise an exception
        return random_solved_grid
    
    except Exception as e:
        print("Error encountered:",e)

def number_shuffle(grid):
    """Each number in the input grid is swapped with a random number 1-9 (it may be kept the same)
    This is done to make the grid feel slightly different to the human user"""

    old_list=[1, 2, 3, 4, 5, 6, 7, 8, 9]
    new_list=random.sample(old_list,k=9) # new_list is a different shuffle each time. eg: [6, 1, 9, 4, 8, 5, 2, 7, 3]

    for row_index in range(9):
        for col_index in range(9):
            
            digit=grid[row_index][col_index]
            if digit!=0:
                new_num=new_list[old_list.index(digit)]
                grid[row_index][col_index]=new_num # swaps old number with corresponding new number
    return grid

def generate_sudoku(full_grid, difficulty="easy"):
    """Random cells are removed from the sudoku grid until it has as few digits as possible whislt still having exactly 1 solution."""

    if difficulty=="easy":
        iterations=43
    elif difficulty=="medium":
        iterations=random.randint(44,52)
    elif difficulty=="hard":
        iterations=random.randint(53,59)

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
        if len(solutions)!=1: # sudoku no longer valid
            #print("Not solveable, iteration no.",i) # used for debugging
            grid[row][column]=num_temp # cell is changed back
            iterations+=1 # iterations is incremented again

    grid=number_shuffle(grid)
    return grid

def main(difficulty_level):
    """retrieves a random unsolved sudoku from the grid archive and manipulates it to generate a fresh, new grid"""
    grid=get_random_grid()
    return generate_sudoku(grid, difficulty_level)