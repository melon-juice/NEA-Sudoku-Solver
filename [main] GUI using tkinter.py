# python imports
import tkinter # used to create Graphical User Interface (GUI)
from tkinter import messagebox # used to output appropriate messages to the user within the GUI
import time # used to track time elapsed by my sudoku solver algorithm
from func_timeout import func_timeout, FunctionTimedOut # used to output a timeout error when necessary

# custom file imports
from my_libraries.Sudoku_Solver_using_MRV import main as solve_sudoku_MRV
from my_libraries.sudoku_generator import main as generate_sudoku
from my_libraries.converter_grid_format import convert_grid # used to add new grids to the archive
import my_libraries.StackClass as undo_stack # enables 'undo' feature

class CreateApp(tkinter.Tk): # equivalent of using root=tkinter.Tk()
    """This is the parent class of the entire sudoku app.
    The constructor:
        > sets the default title & dimensions for any windows made in child classes
        > adds a drop-down menu to the top left corner of every window
        > implements input validation for all inputs in the app
    The methods in this class are ones used by multiple different child classes and are placed here for reusability."""

    def __init__(self):
        super().__init__()
        self.title("Sudoku App")
        self.geometry("380x450")
        self.resizable(False, False)
        self.__create_menu()
        self._validatecommand=(self.register(self._validate_number),"%P") # applies to all user inputs in the app
                                                                        # handles input validation using Tcl
                                                                        # the "%P" part stands for the expected result before validating
    
    def _validate_number(self, P): # input validation used consistently throughout the whole app
        """Only allows a single digit in the inculsive range 1-9 OR an empty string"""
        if (P.isdigit() and len(P)==1 and P!="0") or P=="":
            return True
        else:
            return False

    def _show_frame(self, frame_name):
        """Switches between frames by raising them to the top - used throughout the app to hide/show widgets"""
        frame=self.frames[frame_name]
        frame.tkraise() # frame is sent to the top, making it the frame that the user views

    def __create_menu(self):
        """dropdown elements: Home / Tutorial / Sudoku Tricks // Exit App"""
        self.menubar=tkinter.Menu(self)
        self.app_menu=tkinter.Menu(self.menubar, tearoff=0)
    
        self.app_menu.add_command(label="Home", command=self._go_home)
        self.app_menu.add_command(label="Tutorial", command=self._open_tutorial)
        self.app_menu.add_command(label="About", command=self._open_about)
        self.app_menu.add_separator()
        self.app_menu.add_command(label="Exit App", command=self._exit_app)

        self.menubar.add_cascade(label="Menu", menu=self.app_menu)
        self.config(menu=self.menubar)


    """The following four methods (go_home,open_tutorial,open_about,exit_app) each handle when a user selects a menu option"""

    def _go_home(self):
        if messagebox.askokcancel("Confirm", "Close current window?"):
            self.destroy()
            game=WelcomeWindow()
            game.mainloop()

    def _open_tutorial(self):
        TutorialPage=Tutorial()
        TutorialPage.mainloop()

    def _open_about(self):
        AboutPage=About()
        AboutPage.mainloop()

    def _exit_app(self):
        if messagebox.askokcancel("Confirm", "Close app?"):
            self.destroy()

    """The following two methods (draw3x3grid,draw9x9grid) are used together to display a sudoku grid to the user"""

    def __draw3x3grid(self, container, cells_dict, row, column, bgcolour, grid):
        """displays a block of 9 cells"""
        for i in range(3):
            for j in range(3):
                digit=grid[row+i][column+j] # retrieves data value within the 2D list grid

                cell_value_var=tkinter.StringVar()
                # StringVar command tracks changes to the cell and in turn updates cells_dict(defined at the end of this method)
                e=tkinter.Entry(container, width=5, bg=bgcolour, justify="center",
                                textvariable=cell_value_var, validate="key", # validatecommand is triggered by the press key event
                                validatecommand=self._validatecommand, borderwidth=2)
                
                if digit!=0: # number 1-9
                    e.insert(0, str(digit)) # digit added to UI display and made readonly
                    e.config(state="readonly",readonlybackground=bgcolour, fg="#008B7B", relief="flat")
                else:
                    if isinstance(container.master, GeneratedGame): # checks if the board is part of the generated game window
                        # this means the user has manually inserted a value, so the record_move method is called
                        # changes are stored, in case the user later presses 'undo'
                        cell_value_var.trace_add("write", lambda *args, row_temp=row+i, col_temp=column+j, cell_temp=cell_value_var:
                                                container.master._record_move(row_temp, col_temp, cell_temp))
                        # 'write' mode means the event (in this case, record_move) is triggered when the field is modified
                
                e.grid(row=row+i, column=column+j, sticky="nsew", padx=1, pady=1, ipady=5) # updates the corresponding position within the user interface
                cells_dict[(row+i,column+j)]=e # grid dictionary is updated

    def _draw9x9grid(self,container,cells_dict,grid=None):
        """displays a grid of 9 blocks - using draw3x3grid method (above).
        The parameter 'container' is passed in to determine the correct frame to draw into.
        If a grid is passed in, it will be displayed, otherwise an empty grid is displayed."""
        
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
        
        # the following gets rid of any existing widgets in the container where the grid will be drawn,
        # preventing unused widgets from overlaying and causing the game to function unexpectedly.
        for widget in container.winfo_children(): 
            widget.destroy()
        cells_dict.clear() # cell dictionary reset
        
        colour="#e3e3e3"
        for rowNo in range(0,9,3):
            for colNo in range(0,9,3):
                self.__draw3x3grid(container, cells_dict, rowNo, colNo, colour, grid) # relevant paramteters are passed into 3x3 block drawer
                # background colour switched to visually show where blocks begin/end
                if colour=="#e3e3e3":
                    colour="#bababa"
                else:
                    colour="#e3e3e3"

    def _get_board(self,cells_dict):
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

    """The following two methods (open_SolverWindow,open_GameWindow) are called if the user selects "play sudoku" or "solve my puzzle".
    Each method creates an object of the appropriate class to open a new window, and closes down the welcome window."""

    def _open_SolverWindow(self):
        self.destroy()
        SudokuSolverApp=SolverWindow()
        SudokuSolverApp.mainloop()

    def _open_GameWindow(self):
        self.destroy()
        SudokuGameApp=GameWindow()
        SudokuGameApp.mainloop()


class WelcomeWindow(CreateApp):
    """This is the first window opened when the app starts.
    It features a welcome message and the user is presented with two options:
    > Play a generated sudoku game (GameWindow)
    > Use the sudoku solver to solve an existing puzzle (SolverWindow)."""

    def __init__(self):
        super().__init__()
        self.title("Sudoku App: Home")
        self.geometry("320x250")
        tkinter.Label(self, text="Welcome to the Sudoku App", font=("Consolas", 14, "bold"), fg="#008B7B").pack(pady=15)
        tkinter.Button(self, text="Play Sudoku", bg="light grey", command=self._open_GameWindow, width=15, height=2).pack(pady=10)
        tkinter.Button(self, text="Solve my puzzle", bg="light grey", command=self._open_SolverWindow, width=15, height=2).pack(pady=10)
        tkinter.Label(self, text="Select an option to get started!").pack(padx=20, pady=20)


class About(CreateApp):
    """This window is opened if the drop-down menu option 'About' is selected. Contains a few simple widgets."""
    
    def __init__(self):
        super().__init__()
        self.title("Sudoku App: About")
        self.geometry("320x250")
        tkinter.Label(self, text="About this App", font=("Consolas",12,"bold")).pack(pady=20)
        my_text="""This app was developed by Hajar Elkhatib\nfor an A-level Computer Science NEA.\nStarted: November 2025\nCompleted: February 2026"""
        tkinter.Label(self, text=my_text).pack()


class Tutorial(CreateApp):
    """This window is opened if the drop-down menu option 'Tutorial' is selected."""

    def __init__(self):
        super().__init__()
        self.title("Sudoku App: Tutorial")
        self.geometry("375x290")

        tkinter.Label(self, text="What is Sudoku?", font=("Consolas",12)).pack(pady=10)
        paragraph_one="""Sudoku is a logic-based number-placement puzzle.\nThe objective is to fill the 9x9 grid so that each row,
each column, and each 3×3 block contains all digits\nfrom 1 to 9 (inclusive) exactly once."""
        tkinter.Label(self, text=paragraph_one).pack()

        tkinter.Label(self, text="This app contains:", font=("Consolas",12)).pack(pady=10)
        paragraph_two="""\u2605 Solver: input an unsolved puzzle and find its solution
\u2605 Game: play sudoku at 3 different difficulty levels"""
        tkinter.Label(self, text=paragraph_two).pack()

        tkinter.Button(self, text="I'm ready to play a puzzle!", width=25, height=2, bg="light grey",
                       command=self._open_GameWindow).pack(pady=20)
        

class SolverWindow(CreateApp): # inherits from parent (CreateApp)
    """
    Solver window is one of two main windows in the app. It contains a grid where the user can enter their custom unsolved grid.
    The user can choose to:
    > attempt to solve (there is also a checkbox option to display runtime, which is used to monitor the solver algorithm's speed)
    > clear board
    
    When attempting to solve:
    1. Input validation is applied where appropriate, like ensuring that the grid has enough filled squares.
    > One solution is found: The filled grid is displayed in a read-only format.
        This means the inputted grid has exactly one solution - i.e. it is considered a 'good' puzzle, and it is added to the grid archive.
    > More than one solution is found: the first solution is displayed, and the user can proceed to view the next one.
    > The solver algorithm takes more than 4 seconds to respond: meaning it likely entered an ultra-deep recursive call.
        This means the inputted grid is unlikely to have a small number of solutions - a time-out message is displayed.
        This makes use of the func_timeout library to prevent crashes from occurring.
    """
    
    def __init__(self):
        super().__init__()
        self.title("Sudoku Solver")
        self.__display_runtime_bool=tkinter.IntVar() # boolean variable which monitors whether the 'display runtime' checkbox is checked
        tkinter.Label(self, text="Sudoku Solver", font=("Consolas",12)).grid(row=0, column=0, columnspan=2, pady=15)

        self.__grid_frame=tkinter.Frame(self) # initailaises grid_frame, where the grid will be placed (private)
        self.__grid_frame.grid(row=1, column=0, padx=20, pady=5)
        self._cells={}
        self._draw9x9grid(self.__grid_frame, self._cells)

        # the following creates the 'display runtime' checkbox and solve button
        tkinter.Checkbutton(self, text="Display runtime", variable=self.__display_runtime_bool, width=15, height=2).place(x=220, y=380)
        tkinter.Button(self, text="Clear", bg="light grey", command=lambda: self._draw9x9grid(self.__grid_frame, self._cells),
                       width=10, height=2).place(x=30, y=380)
        tkinter.Button(self, text="Test for\nSolutions", bg="turquoise", command=self._solve_grid, width=10, height=2).place(x=130, y=380)

    def _solve_grid(self):
        """Uses parent method get_board to read user input & uses MRV solver library to find solutions. 
        (The result of pressing the "Solve" button)"""

        current_board=self._get_board(self._cells)

        # the following structure counts the number of filled fields in the board
        zeroes_list=0 
        for row in current_board:
            for cell in row:
                if cell==0:
                    zeroes_list+=1
        if zeroes_list==81: # checks if the board is completely empty
            messagebox.showwarning("Board Empty!", "Please input your board before attempting to solve.")
            return
        if (81-zeroes_list)<17: # checks if the number of filled cells is under 17
            messagebox.showwarning("Too Few Clues!", "Please enter at least 17 numbers to avoid a crash.")
            return
    
        solutions_list=[] # created so that if the solver fails, a "solutions_list not defined" error does not occur
        start_time=time.time() # timer begins
        try:
            solutions_list=func_timeout(4, solve_sudoku_MRV,args=(current_board,)) # solve library called, with timeout after 4 seconds
            # a comma is added here to tell func_timeout not to unpack the array ↑
            
            # if the algorithm reaches this part of the code, it means a timeout did not occur and the solver algorithm was successful                                                                         
            elapsed_time=time.time()-start_time

        except FunctionTimedOut: # timeout message - this happens when the solver goes into a super deep recursive call
            messagebox.showerror("Solver Error", f"The solver took more than 4 seconds.\nYour input is unlikely to have a single solution.")
        except Exception as e: # any other exception. This is not expected, but is an extra precaution
            messagebox.showerror("Solver Error", f"An error ocurred when attempting to solve.\nDetails: {e}")

        if not solutions_list:
            messagebox.showinfo("No solutions", "Check your inputs and try again.")
            return
        
        # solution(s) found
        if self.__display_runtime_bool.get()==1: # "display runtime" box is checked
            messagebox.showinfo("Solution found!",f"\nTotal solutions found: {len(solutions_list)}\nTime elapsed: {elapsed_time:.3f} seconds")
        else:
            messagebox.showinfo("Solution found!",f"\nTotal solutions found: {len(solutions_list)}")

        self._draw9x9grid(self.__grid_frame, self._cells, solutions_list[0]) # first solution displayed in the solver window
        for cell_widget in self._cells.values(): 
            cell_widget.config(state="readonly") # makes the whole board read-only

        if len(solutions_list)>1: # The puzzle has more than one solution: the user is given the choice to view each one.
            for solution in solutions_list[1:]:
                if messagebox.showinfo("Multiple Solutions", "This puzzle has multiple solutions. Would you like to see the next one?"):
                    self._draw9x9grid(self.__grid_frame, self._cells, solution) # next solution is displayed
        
        else: # grid has one unique solution

            # The following code adds the new user-inputted grid to the archive file (as a single line)
            # ... so that it can be used in future to generate new puzzles

            already_in_file=False # boolean variable used to ensure the archive doesn't get updated with a duplicate
            try:
                with open(r"./my_libraries/SingleStringGridArchive.txt", "r", encoding="utf-8") as file:
                    single_line=convert_grid(current_board) # grid converted to single line
                    for file_line in file.readlines():
                        file_line=file_line.strip()
                        if single_line==file_line:
                            already_in_file==True # this means the grid won't be added to the archive
                    file.close()

                if not already_in_file:
                    with open(r"./my_libraries/SingleStringGridArchive.txt", "a", encoding="utf-8") as file:
                        file.writelines(single_line+"\n") # singline line grid is added to the end of the file
                        file.close()
                        
            except: # error whilst opening file - it may not be stored in the correct location.
                messagebox.showinfo("File Not Found","SingleStringGridArchive.txt could not be opened.\nProceeding without save.")
            

class GameWindow(CreateApp):
    """
    Game window is the second of two main windows in the app. It utilises my sudoku generator library to generate puzzles for the player.
    The OptionsScreen frame of the Game Window is a choice screen of Easy / Medium / Hard .
    Upon clicking one of these options, the player raises a frame and triggers the generation of a new puzzle.
    The GeneratedGame frame contains:
    > an unsolved grid with some cells in a read-only format, and the rest as enterable fields
    > a 'check answer' button
        The grid is checked for any empty/unfilled cells; in which case an appropriate warning message is returned.
    > a clear board button
    > a 'return to difficulties' button
    > an undo button, which uses a stack data structure to keep track of changes made to the board (more detail given in that section of the code)
    """
    
    def __init__(self):
        super().__init__()
        self.title("Sudoku Game") # window title from parent class is overwritten
        
        # container is initialised to dynamically hold all frames within the game window
        container=tkinter.Frame(self)
        container.pack(fill="both", expand=True) # container expanded to fill the whole window
        container.grid_columnconfigure(0, weight=1) # contents of the contianer are centred
        container.grid_rowconfigure(0, weight=1)
        self.frames={} # all frames are managed in a dictionary

        # each frame is initialised and stored
        for F in (OptionsScreen, GeneratedGame):
            page_name=F.__name__  # retreives the string "OptionsScreen", etc.
            frame=F(parent=container, controller=self)
            self.frames[page_name]=frame # frame is stored in dictionary
            frame.grid(row=0, column=0, sticky="nsew") # the frame is placed in GUI grid (this line is necessary)
        self._show_frame("OptionsScreen") # the diffculty options page is placed at the top

    def _change_size(self, size_string):
        """Resizes window for switching between frames"""
        self.resizable(True, True) # temporarily allows resizing (in both x and y directions)
        self.geometry(size_string)
        self.resizable(False, False) # window dimensions are locked again
    

class OptionsScreen(tkinter.Frame): # inherits frame
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self._controller=controller
        self._controller._change_size("380x300")

        tkinter.Label(self, text="Select Difficulty:", font=("Consolas",12)).pack(pady=10)
        for level in ("easy","medium","hard"):
            level_button=tkinter.Button(self, text=level.title(), width=10, height=2, bg="light grey",
                    command=lambda: self.__begin_game(level)) # lambda function executes begin_game when button is pressed 
            level_button.pack(padx=20, pady=10)

        tkinter.Label(self, text="Note that loading the puzzle may take a moment.").pack(pady=10)

    def __begin_game(self, difficulty_level):
        try:
            generated_grid=generate_sudoku(difficulty_level) # sudoku puzzle generated using logic stored in library
            game_frame=self._controller.frames["GeneratedGame"]
            game_frame.starting_grid=generated_grid # saves the generated puzzle for future retrieval
            self._controller._draw9x9grid(game_frame.grid_container, game_frame._cells, generated_grid) # puzzle displayed
            game_frame.grid_container.pack(padx=20)
            self._controller._change_size("380x480")
            self._controller._show_frame("GeneratedGame") # this frame is raised, hiding the difficulties options frame
            self._controller.start_time=time.time() # timer begins
           
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate puzzle.\nDetails: {e}") 


class GeneratedGame(tkinter.Frame): # inherits frame
    
    def __init__(self,parent,controller):
        super().__init__(parent)
        self._controller=controller
        self._cells={} # initialised grid - this will be filled by draw9x9grid
        self.__undo_stack=undo_stack.Stack() # uses stack library to initialise undo stack
        self.__this_move_is_an_undo=False

        """The Generated game page has 3 main sections:
        > header_frame: contains return button to switch frames, and some simple text
        > grid_container: where generated puzzle goes
        > button_frame: contains buttons at the bottom of the screen to: undo / clear / check answer
        These sections are initialised seperately and hold widgets independently. This allows for easier formatting and debugging."""

        header_frame=tkinter.Frame(self)
        header_frame.pack(fill="x", pady=20)

        tkinter.Button(header_frame, text="<- Return to difficulties", width=20, height=1,
                       command=lambda:[self._controller._change_size("380x320"), controller._show_frame("OptionsScreen")]
                       ).pack(side="left", padx=20)
        tkinter.Label(header_frame, text="Try solving this!", font=("Consolas",12)).pack(side="left")
        
        self.grid_container=tkinter.Frame(self)
        self.grid_container.pack(pady=10)

        button_frame=tkinter.Frame(self)
        button_frame.pack(padx=20, pady=20, fill="x")

        tkinter.Button(button_frame, text="Undo", bg="light grey", command=self.__undo, width=10, height=2).pack(side="left", padx=10, expand=True)
        tkinter.Button(button_frame, text="Clear Board", bg="light grey", command=lambda: self._controller._draw9x9grid(self.grid_container, self._cells, self.starting_grid),
                       width=10, height=2).pack(side="left", padx=10, expand=True)
        tkinter.Button(button_frame, text="Check\nSolution", bg="turquoise", command=self.__check_solution, width=10, height=2).pack(side="left", padx=10, expand=True)
    
    def _solve_grid(self):
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

    def __check_solution(self):
        """Compares the user's input with the correct solution - which is found via the solve_grid method."""
        
        current_board=self._controller._get_board(self._cells) # calls method from CreateApp to retrieve what the user has entered.
        number_of_zeroes=0
        for row in current_board:
            for cell in row:
                if cell==0:
                    number_of_zeroes+=1
        if number_of_zeroes!=0: # checks if the board is completely filled
            messagebox.showerror("Board Incomplete!", "Please fully input your answer before before attempting to check.")
            return
        
        correct_solution=self._solve_grid() 
        # note: the way the sudoku generator works ensures the generated puzzle has one unique solution, so we don't need to worry about multiple vaild solutions.
        if current_board==correct_solution:
            time_elapsed=time.time()-self._controller.start_time # the user's solve time is calculated
            formatted_time=time.strftime("%M:%S", time.gmtime(time_elapsed)) # time formatted to minutes and seconds
            messagebox.showinfo("Solution Correct!", f"Congratulations! You finished in {formatted_time}!\nNavigate back to difficulties to generate a new puzzle.")
            # the whole board is set to read-only
            for cell_widget in self._cells.values():
                cell_widget.config(state="readonly")
        else:
            messagebox.showinfo("Solution Incorrect", f"That's not quite right.\nCheck your inputs and try again.")

    def _record_move(self, row_index, column_index, cell_value_var):
        """This method is triggered whenever a change is detected in the board. It first checks that the current move being performed isn't an 'undo'.
        If ok, it pushes the coordinate where the change occurred onto the undo stack. This method makes no changes to the GUI."""

        if self.__this_move_is_an_undo:
            return # ensures that the 'undo' move isn't pushed onto the stack
        
        value=cell_value_var.get()
        if value!="":
            self.__undo_stack.push((row_index, column_index)) # saves the coordinate where the change was made, so it can be cleared later
            #print(f"Recorded move at {row_index}, {column_index}") # for tracing the stack and debugging

    def __undo(self):
        """Checks that the current move being performed isn't an 'undo'. If ok, it pops the last updated coordinate from the undo_stack.
        The corresponding cell is cleared, and the user display is updated."""

        if self.__undo_stack.isEmpty():
            return
        
        self.__this_move_is_an_undo=True
        try:
            retreived_coordinate=self.__undo_stack.pop() # coordinate position popped
            if retreived_coordinate:
                entry_widget=self._cells[retreived_coordinate] # corresponding GUI widget found
                entry_widget.config(state="normal") # temporarily sets the widget type to normal to allow .delete()
                entry_widget.delete(0, tkinter.END) # coordinate cleared

        except Exception as e:
            messagebox.showerror("Undo Stack Error", f"An error ocurred when attempting to undo.\nDetails: {e}")
        finally:
            self.__this_move_is_an_undo=False


app=WelcomeWindow() # object of WelcomeWindow created - this is the initial welcome message pop-up
app.mainloop()
