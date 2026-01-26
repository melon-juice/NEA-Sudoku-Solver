import tkinter
from tkinter import messagebox # used to output appropriate messages to the user
import time # used to track time elapsed by solver algorithm
import webbrowser # used for hyperlink in 'about' page
from func_timeout import func_timeout, FunctionTimedOut # used to output a timeout error when necessary
from my_libraries.Sudoku_Solver_using_MRV import main as solve_sudoku_MRV
from my_libraries.sudoku_generator import main as generate_sudoku
import my_libraries.StackClass as undo_stack

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
        self.app_menu.add_command(label="About", command=self.open_about)
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
                    e.config(state="readonly",readonlybackground=bgcolour, fg="#008B7B", relief="flat")
                
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
        
        for widget in container.winfo_children(): # this gets rid of any existing widgets in the container, for game refreshes
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

    def get_board(self,cells_dict):
        """Returns the current state of the GUI board as a 2D list, ready for solving."""
        board=[]
        for row in range(9):
            row_temp=[]
            for column in range(9):
                digit=cells_dict[(row, column)].get()
                if digit=="": # empty cells are appended as zeroes, to match my sudoku solver logic
                    row_temp.append(0)
                else:
                    row_temp.append(int(digit))
            board.append(row_temp)
        return board
        
    # the following methods handle when a user selelcts a menu option

    def go_home(self):
        if messagebox.askokcancel("Confirm", "Close current window?"):
            self.destroy()
            game=WelcomeWindow()
            game.mainloop()

    def open_tutorial(self):
        TutorialPage=Tutorial()
        TutorialPage.mainloop()

    def open_about(self):
        AboutPage=About()
        AboutPage.mainloop()

    def exit_app(self):
        if messagebox.askokcancel("Confirm", "Close app?"):
            self.destroy()

    def open_SolverWindow(self):
        self.destroy()
        SudokuSolverApp=SolverWindow()
        SudokuSolverApp.mainloop()

    def open_GameWindow(self):
        self.destroy()
        SudokuGameApp=GameWindow()
        SudokuGameApp.mainloop()

    def open_github_link(self):
        try:
            webbrowser.open_new("https://github.com/melon-juice") # opens github account
        except Exception as e:
            print(f"Error opening link: {e}")


class WelcomeWindow(CreateApp):

    def __init__(self):
        super().__init__()
        self.title("Home")
        self.geometry("320x250")
        tkinter.Label(self, text="Welcome to the Sudoku App", font=("Consolas", 14, "bold"), fg="#008B7B").pack(pady=15)
        tkinter.Button(self, text="Play Sudoku", bg="light grey", command=self.open_GameWindow, width=15, height=2).pack(pady=10)
        tkinter.Button(self, text="Solve my puzzle", bg="light grey", command=self.open_SolverWindow, width=15, height=2).pack(pady=10)
        tkinter.Label(self, text="Select an option to get started!").pack(padx=20, pady=20)

class About(CreateApp):
    def __init__(self):
        super().__init__()
        self.geometry("320x250")
        tkinter.Label(self, text="About this App", font=("Consolas",12,"bold")).pack(pady=20)
        my_text="""This app was developed by [redacted]\nfor an A-level Computer Science NEA.\nStarted: November 2025\nCompleted: January 2026
\n\nIf you'd like to see more of my projects:"""
        tkinter.Label(self, text=my_text).pack()
        tkinter.Button(self, text="see my GitHub", command=self.open_github_link, cursor="hand2").pack()

class Tutorial(CreateApp):
    def __init__(self):
        super().__init__()
        self.geometry("320x250")
        tkinter.Label(self, text="How to Play Sudoku", font=("Consolas",12,"bold")).pack(pady=20)
        my_text="""This is a tutorial on how to play sudoku..."""
        tkinter.Label(self, text=my_text).pack()
        tkinter.Button(self, text="I'm ready to play a puzzle!", width=25, height=2, bg="light grey",
                       command=self.open_GameWindow).pack(pady=15)

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

    def solve_grid(self):
        """Uses get_board to read user input & uses MRV solver library to find solutions. 
        (The result of pressing the "Solve" button)"""

        current_board=self.get_board(self.cells)

        # the following structure counts the number of filled fields in the board
        zeros_list=0 
        for row in current_board:
            for cell in row:
                if cell==0: zeros_list+=1
        if zeros_list==81: # checks if the board is completely empty
            messagebox.showerror("Board Empty!", "Please input your board before attempting to solve.")
            return
        if (81-zeros_list)<17: # checks if the number of filled cells is under 17
            messagebox.showwarning("Too Few Clues!", "Please enter at least 17 numbers to avoid a crash.")
            return
    
        solutions_list=[] # created so that if the solver fails, a "solutions_list not defined" error does not occur
        start_time=time.time() # timer begins
        try:
            solutions_list=func_timeout(4.5, solve_sudoku_MRV,args=(current_board,)) # solve library called, with a timeout after 4.5 seconds
            # if the algorithm reaches this part of the code, it means a timeout did not occur and the solver algorithm was successful                                                                         
            elapsed_time=time.time()-start_time

        except FunctionTimedOut: # timeout message - this happens when the solver goes into a super deep recursive call
            messagebox.showerror("Solver Error", f"The solver took more than 4.5 seconds.\nYour input is unlikely to have a single solution.")
            print("The subroutine timed out after 3 seconds.")
        except Exception as e: # any other exception. This is not expected, but is an extra precaution
            messagebox.showerror("Solver Error", f"An error ocurred when attempting to solve.\nDetails: {e}")

        if len(solutions_list)==0:
                messagebox.showerror("No solutions", "Check your inputs and try again.")
        else: # solution(s) found
            if self.display_runtime_bool.get()==1: # "display runtime" box is checked
                messagebox.showinfo("Solution found!",f"\nTotal solutions found: {len(solutions_list)}\nTime elapsed: {elapsed_time:.3f} seconds")
            else:
                messagebox.showinfo("Solution found!",f"\nTotal solutions found: {len(solutions_list)}")
            for solution in solutions_list:
                print(solution) # placeholder for now: must display in GUI
            

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
        self.resizable(True, True) # temporarily allows resizing
        self.geometry(size_string)
        self.resizable(False, False) # window dimensions are locked again
    
class OptionsScreen(tkinter.Frame): # inherits frame
    
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller
        self.controller.change_size("380x300")
        self.create_undo_stack()

        tkinter.Label(self, text="Select Difficulty:", font=("Consolas",12)).pack(pady=10)
        
        for level in ("easy","medium","hard"):
            level_button=tkinter.Button(self, text=level.title(), width=10, height=2, bg="light grey",
                    command=lambda l=level: self.begin_game(l))
            level_button.pack(padx=20, pady=(10))

        tkinter.Label(self, text="Note that loading the puzzle may take a moment.").pack(pady=(10))

    def create_undo_stack():
        pass

    def undo(self):
        pass

    def begin_game(self, difficulty_level):
        try:
            generated_grid=generate_sudoku(difficulty_level) # generated using library
            game_frame=self.controller.frames["GeneratedGame"]
            game_frame.starting_grid=generated_grid # saves the generated puzzle for future retrieval
            self.controller.draw9x9grid(game_frame.grid_container, game_frame.cells, generated_grid)
            game_frame.grid_container.pack(padx=20)
            self.controller.change_size("380x480")
            self.controller.show_frame("GeneratedGame")
            self.controller.start_time=time.time()
           
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
        tkinter.Button(button_frame, text="Clear Board", bg="light grey", command=lambda: self.controller.draw9x9grid(self.grid_container, self.cells, self.starting_grid),
                       width=10, height=2).pack(side="left", padx=10, expand=True)
        tkinter.Button(button_frame, text="Check\nSolution", bg="turquoise", command=self.check_solution, width=10, height=2).pack(side="left", padx=10, expand=True)
    
    def solve_grid(self):
        """Solves the generated puzzle to get the solution (used in check_solution to compare against the user's answer)
        This is a massively simplified version of the solve_grid method in the SolverWindow class."""
    
        solutions_list=[] # created so that if the solver fails, a "solutions_list not defined" error does not occur
        try:
            solutions_list=solve_sudoku_MRV(self.starting_grid) # solve library called
            # if the algorithm reaches this part of the code, it means a timeout did not occur and the solver algorithm was successful                                                                         
        except Exception as e: # the solver encountered an error
            messagebox.showerror("Solver Error", f"An error ocurred when attempting to find the answer.\nDetails: {e}")
            return
        return solutions_list[0]

    def check_solution(self):
        """Compares the user's input with the correct solution - which is found via solve_grid"""
        
        current_board=self.controller.get_board(self.cells)
        correct_solution=self.solve_grid()
    
        zeros_list=0 
        for row in current_board:
            for cell in row:
                if cell==0: zeros_list+=1
        if zeros_list!=0: # checks if the board is completely filled
            messagebox.showerror("Board Incomplete!", "Please fully input your answer before before attempting to check.")
            return
        
        if current_board==correct_solution:
            time_elapsed=time.time()-self.controller.start_time
            messagebox.showinfo("Solution Correct!", f"Congratulations! You finished in {time_elapsed}")
            self.controller.draw9x9grid(current_board) # makes the whole board read-only
        else:
            messagebox.showinfo("Solution Inorrect", f"Your solution isn't quite right.\nCheck your inputs and try again.")
        

        


game=WelcomeWindow()
game.mainloop()