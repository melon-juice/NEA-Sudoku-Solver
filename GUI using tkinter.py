import tkinter
from tkinter import messagebox
import time
from my_libraries.Sudoku_Solver_using_MRV import main as solve_sudoku_MRV

class CreateApp(tkinter.Tk): # equivalent of using root=tkinter.Tk()
    def __init__(self):
        super().__init__()
        
        self.title("Sudoku Solver")
        self.geometry("600x600")
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        self.menubar=tkinter.Menu(self)
        # dropdown elements: Home / Tutorial / Sudoku Tricks // Exit App
        self.app_menu=tkinter.Menu(self.menubar, tearoff=0)
        self.app_menu.add_command(label="Home", command=self.go_home)
        self.app_menu.add_command(label="Tutorial", command=self.open_tutorial)
        self.app_menu.add_command(label="Sudoku Tricks", command=self.open_tricks)
        self.app_menu.add_separator()
        self.app_menu.add_command(label="Exit App", command=self.exit_app)
        self.menubar.add_cascade(label="Menu", menu=self.app_menu)
        self.config(menu=self.menubar)

    # the following methods handle when a user selelcts a menu option

    def go_home(self):
        if messagebox.askokcancel("Confirm", "Close current window?"):
            print("Home page requested")

    def open_tutorial(self):
        print("Tutorial page requested")

    def open_tricks(self):
        print("Sudoku tricks page requested")

    def exit_app(self):
        if messagebox.askokcancel("Confirm", "Close app?"):
            self.destroy()

    def create_widgets(self): # can be overriden - or just not present in this class
        pass

class SolverWindow(CreateApp): # inherits from parent (CreateApp)
    
    def __init__(self):
        super().__init__()
        self.geometry("350x350")
        self.cells={}
        self.timer_bool=tkinter.IntVar()
        self.validatecommand=(self.register(self.validate_number),"%P") # handles input validation using Tcl
                                            # the "%P" part stands for the expected result before validating
        self.grid_frame=tkinter.Frame(self) # initailaises grid_frame, where the grid will be placed
        self.grid_frame.grid(row=1, column=0, padx=20, pady=20)
        self.draw9x9grid()
        # creates the controls: checkbox for timer / solve button
        tkinter.Checkbutton(self, text="Display runtime", variable=self.timer_bool).grid(row=2, column=0, sticky="w", padx=20)
        tkinter.Button(self, text="Solve", bg="light grey", command=self.solve_grid).grid(row=2, column=0, pady=10)
    
    def validate_number(self, P):
        """Only allows a single digit in the inculsive range 1-9 OR an empty string"""
        # essentially checks for single digit, then excludes 0
        return (P.isdigit() and len(P)==1 and P!="0") or P==""

    def draw3x3grid(self, row, column, bgcolour):
        for i in range(3):
            for j in range(3):
                e=tkinter.Entry(self.grid_frame, width=5, bg=bgcolour, justify="center", validate="key", validatecommand=self.validatecommand)
                e.grid(row=row+i+1, column=column+j+1, sticky="nsew", padx=1, pady=1, ipady=5)     
                self.cells[(row+i+1, column+j+1)]=e

    def draw9x9grid(self):
        colour="light grey"
        for rowNo in range(1,10,3):
            for colNo in range(0,9,3):
                self.draw3x3grid(rowNo, colNo, colour)
                if colour=="light grey":
                    colour="silver"
                else:
                    colour="light grey"

    def get_board(self):
        """Returns the current state of the GUI board as a 2D list, ready for solving."""
        board=[]
        for row in range(2,11):
            row_temp=[]
            for column in range(1,10):
                digit=self.cells[(row, column)].get()
                if digit=="": # empty cells are appended as zeroes, to match my sudoku solver logic
                    row_temp.append(0)
                else:
                    row_temp.append(int(digit))
            board.append(row_temp)
        return board

    def solve_grid(self):
        """Uses get_board to read user input & uses MRV solver library to find solutions. 
        (The result of pressing the "Solve" button)"""
        
        current_board=self.get_board()

        if all(all(cell==0 for cell in row) for row in current_board): # checks the board definitely has some inputs
            messagebox.showerror("Board Empty", "Input your board before clicking 'Solve'.")
            return
        
        flat_list = [item for sublist in current_board for item in sublist if item!=0] ##hmmm
        if len(flat_list)<17:
            messagebox.showwarning("Too Few Clues", "Please enter at least 17 numbers to avoid a crash.")
            return
    
        start_time=time.time() # timer begins
        solutions_list=[]
        try:              
            solutions_list=solve_sudoku_MRV(current_board) ### key line
            if self.timer_bool.get()==1: # "display runtime" box is checked
                elapsed_time=time.time()-start_time
                print(f"\nTime elapsed: {elapsed_time:.4f} seconds")
        except Exception as e:
            messagebox.showerror("Solver Error", f"The solver crashed or timed out.\nDetails: {e}")
        
        if len(solutions_list)==0:
            messagebox.showerror("No solutions", "Check your inputs and try again.")
        else:
            print(f"\nTotal solutions found: {len(solutions_list)}")
            for solution in solutions_list:
                for line in solution:
                    print(line) # must later update this to show solution in GUI
            
# def solve(): gets elements inputted by user using get_board// will output error message if unsolveable
#   grid=get_board
#   calls solve_sudoku !!! <- using "my_libraries.Sudoku-Solver-using-MRV", aka solve_sudoku"
#   displays grid appropriately within UI
#   ...or error message if applicable

#solveButton that will call the solve() function

SudokuSolverApp=SolverWindow()
SudokuSolverApp.mainloop()
