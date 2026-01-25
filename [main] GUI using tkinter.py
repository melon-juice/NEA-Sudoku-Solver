import tkinter
from tkinter import messagebox
import time # used to track time elapsed by solver algorithm
from func_timeout import func_timeout, FunctionTimedOut # used to output a timeout error when necessary
from my_libraries.Sudoku_Solver_using_MRV import main as solve_sudoku_MRV
from my_libraries.sudoku_generator import main as generate_sudoku

class CreateApp(tkinter.Tk): # equivalent of using root=tkinter.Tk()
    def __init__(self):
        super().__init__()
        self.title("Sudoku Solver")
        self.geometry("380x450")
        self.resizable(False, False)
        self.validatecommand=(self.register(self.validate_number),"%P") # moved to parent class so that it is applied to all user inputs
                                        # handles input validation using Tcl
                                        # the "%P" part stands for the expected result before validating
        self.create_menu()
        
    def validate_number(self, P):
        """Only allows a single digit in the inculsive range 1-9 OR an empty string"""
        # essentially checks for single digit, then excludes 0
        return (P.isdigit() and len(P)==1 and P!="0") or P==""

    def show_frame(self,frame_name):
        """switches between frames by raising them to the top"""
        frame=self.frames[frame_name]
        frame.tkraise() # frame is sent to the top, making it the frame that the user views

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

    def draw3x3grid(self, container, cells_dict, row, column, bgcolour, grid):
        for i in range(3):
            for j in range(3):

                digit=grid[row+i][column+j] # retrieves data value within the 2D list grid
                e=tkinter.Entry(container, width=5, bg=bgcolour, justify="center", 
                                validate="key", validatecommand=self.validatecommand, borderwidth=2)
                                
                if digit!=0: # number 1-9
                    e.insert(0, str(digit)) # digit added to UI display and made readonly
                    e.config(state="readonly",readonlybackground=bgcolour, fg="#016257", relief="flat")
                
                # the following updates the correspondinf position within the dictionary and UI
                e.grid(row=row+i, column=column+j, sticky="nsew", padx=1, pady=1, ipady=5)     
                cells_dict[(row+i,column+j)]=e # dictionary is updated

    def draw9x9grid(self,container,cells_dict,grid=None):
        """grid display method used to show the grid in a consistent way.
        container is used to determine the correct frame to draw into.
        If a specific grid is passed in, it will be displayed, or else an empty grid is displayed."""
        
        if grid==None: # default to empty grid if none provided
            grid=[[0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0]]
        
        for widget in container.winfo_children(): # it's important to get rid of any existing widgets in the container, for game refreshes
            widget.destroy()
        cells_dict.clear()
        
        colour="#e3e3e3"
        for rowNo in range(0,9,3):
            for colNo in range(0,9,3):
                self.draw3x3grid(container, cells_dict, rowNo, colNo, colour, grid) # relevant paramteters are passed into 3x3 drawer
                if colour=="#e3e3e3":
                    colour="#bababa"
                else:
                    colour="#e3e3e3"

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
        self.cells={}
        self.display_runtime_bool=tkinter.IntVar()

        
        self.header=tkinter.Label(self, text="Input your incomplete grid here:", font=("Consolas",12))
        self.header.grid(row=0, column=0, columnspan=2, pady=15)

        self.grid_frame=tkinter.Frame(self) # initailaises grid_frame, where the grid will be placed
        self.grid_frame.grid(row=1, column=0, padx=20, pady=5)
        self.draw9x9grid(self.grid_frame,self.cells)

        # the following creates the controls: checkbox for timer / solve button
        tkinter.Checkbutton(self, text="Display runtime", variable=self.display_runtime_bool, width=15, height=2).place(x=220, y=380)
        tkinter.Button(self, text="Clear", bg="light grey", command=lambda: self.draw9x9grid(self.grid_frame, self.cells),
                       width=10, height=2).place(x=30, y=380)
        tkinter.Button(self, text="Test for\nSolutions", bg="turquoise", command=self.solve_grid, width=10, height=2).place(x=130, y=380)
    
    def get_board(self):
        """Returns the current state of the GUI board as a 2D list, ready for solving."""
        board=[]
        for row in range(9):
            row_temp=[]
            for column in range(9):
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
    
        solutions_list=[]
        start_time=time.time() # timer begins
        
        try:
            solutions_list=func_timeout(4.5, solve_sudoku_MRV,args=(current_board,)) # Solve library called, with a timeout after 4.5 seconds

            # if the algorithm reaches this part of the code, it means a timeout did not occur and the solver algorithm was successful                                                                         
            messagebox.showinfo("Solution found!",f"The solver algorithm found {len(solutions_list)} solutions.") 
            elapsed_time=time.time()-start_time

        except FunctionTimedOut:
            messagebox.showerror("Solver Error", f"The solver took more than 4.5 seconds.\nYour input is unlikely to have a single solution.")
            print("The subroutine timed out after 3 seconds.")

        except Exception as e:
            messagebox.showerror("Solver Error", f"An error ocurred when attempting to solve.\nDetails: {e}")


        if len(solutions_list)==0:
                messagebox.showerror("No solutions", "Check your inputs and try again.")
        else:
            print(f"\nTotal solutions found: {len(solutions_list)}")
            for solution in solutions_list:
                for line in solution:
                    print(line) # must later update this to show solution in GUI
            if self.display_runtime_bool.get()==1: # "display runtime" box is checked
                    print(f"\nTime elapsed: {elapsed_time:.4f} seconds")
            

class GameWindow(CreateApp):
    
    def __init__(self):
        super().__init__()
        self.title("Sudoku Game")
        
        # a container is initialised to hold all my frames within the game window
        container=tkinter.Frame(self)
        container.pack(fill="both", expand=True) # container expanded to fill the whole window
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        self.frames={} # all frames are managed in a dictionary

        # each frame is initialised and stored
        for F in (OptionsScreen,GeneratedGame):
            page_name=F.__name__  # retreived the string "OptionsScreen", etc.
            frame=F(parent=container,controller=self)
            self.frames[page_name]=frame # frame is stored in dictionary
            frame.grid(row=0,column=0,sticky="nsew") # frame is placed (this line is necessary)
       
        self.show_frame("OptionsScreen") # the log in page is placed at the top

    def change_size(self, size_string):
        """Resizes window for switching between frames"""
        self.resizable(True, True) 
        self.geometry(size_string)
        self.update_idletasks() #### look into this
        self.resizable(False, False)
    
class OptionsScreen(tkinter.Frame): # inherits frame
    
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller
        self.controller.change_size("380x320")

        self.header=tkinter.Label(self, text="Select Difficulty:", font=("Consolas",12))
        self.header.pack(pady=10)
        
        for level in ("easy","medium","hard"):
            level_button=tkinter.Button(self, text=level.title(), width=10, height=2, bg="light grey",
                    command=lambda l=level: self.begin_game(l))
            level_button.pack(padx=20, pady=(10))

        tkinter.Label(self, text="Note that loading the puzzle may take a moment.").pack(pady=(10))

    def begin_game(self, difficulty_level):
        try:
            grid=generate_sudoku(difficulty_level) # generated using library
            game_frame=self.controller.frames["GeneratedGame"]
            self.controller.draw9x9grid(game_frame.grid_container, game_frame.cells, grid)
            game_frame.grid_container.pack(padx=20)
            self.controller.change_size("380x480")
            self.controller.show_frame("GeneratedGame")
           
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate puzzle.\nDetails: {e}") 

class GeneratedGame(tkinter.Frame): # inherits frame
    
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller
        self.cells={} # initialised grid - this will be filled by draw9x9grid

        header_frame=tkinter.Frame(self)
        header_frame.pack(fill="x", pady=20)

        tkinter.Button(header_frame, text="<- Return to difficulties", width=20, height=1,
                       command=lambda:[self.controller.change_size("380x320"), controller.show_frame("OptionsScreen")]
                       ).pack(side="left", padx=20)
        tkinter.Label(header_frame, text="Try solving this!", font=("Consolas",12)).pack(side="left")
        
        self.grid_container=tkinter.Frame(self)
        self.grid_container.pack(pady=10)

        button_frame=tkinter.Frame(self)
        button_frame.pack(padx=20, pady=20, fill="x")

        tkinter.Button(button_frame, text="Undo", bg="light grey", command=None, width=10, height=2).pack(side="left", padx=10, expand=True)
        tkinter.Button(button_frame, text="Clear Board", bg="light grey", command=None, width=10, height=2).pack(side="left", padx=10, expand=True)
        tkinter.Button(button_frame, text="Check\nSolution", bg="turquoise", command=None, width=10, height=2).pack(side="left", padx=10, expand=True)

# SudokuSolverApp=SolverWindow()
# SudokuSolverApp.mainloop()

SudokuGameApp=GameWindow()
SudokuGameApp.mainloop()
