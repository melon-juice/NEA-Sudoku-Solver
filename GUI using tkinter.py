import tkinter
#note: for the following line to work, I need to modify solver file name to Sudoku-Solver-using-MRV and put it in my_libraries
#from my_libraries.Sudoku-Solver-using-MRV import main as solve_sudoku

class CreateApp(tkinter.Tk): #equivalent of using root=tkinter.Tk()

    def __init__(self):
        super().__init__()
        # then set window size, text font, icon, name etc
        #eg: self.tkinter.title("Sudoku Solver")
        
    #WITHIN THE __INIT__ : create a menu bar
    # see other python file for this code!


# create widgets:

    #def display_board(): displays the interface_board as an array of empty fields
    #   define makeup of a 3x3 grid under name "block"
    #   display 3x3 array of "block"s - essentially the 9x9 grid

    #def get_board(): converts the interface_board to the 2d array format required for solving
    #   board=[]
    #   for i in range (9):  
    #       line=[]
    #       for each num in the row i of interface grid:
    #           line.append(num)
    #       board.append(line)
    #   return board

class SolverWindow():
    def __init__(self):
        super().__init__()


# def solve(): gets elements inputted by user using get_board// will output error message if unsolveable
#   grid=get_board
#   calls solve_sudoku !!! <- using "my_libraries.Sudoku-Solver-using-MRV", aka solve_sudoku"
#   displays grid appropriately within UI
#   ...or error message if applicable

#solveButton that will call the solve() function

SudokuSolverApp=CreateApp()
SudokuSolverApp.mainloop()
