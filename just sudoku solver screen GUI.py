import time
import tkinter
from my_libraries.Sudoku_Solver_using_MRV import main as solve_sudoku_MRV

root=tkinter.Tk()
root.title("Sudoku Solver")
root.geometry("350x350")

##########################################
cells={}
grid_frame = tkinter.Frame(root)
grid_frame.grid(row=1, column=0, padx=20, pady=5)

def ValidateNumber(P):
    out=(P.isdigit() or P=="") and len(P)<2 
    return out

reg=root.register(ValidateNumber)

def draw3x3grid(row, column, bgcolour):
    for i in range(3):
        for j in range(3):
            e=tkinter.Entry(grid_frame, width=5, bg=bgcolour, justify="center", validate="key", validatecommand=(reg,"%P"))
            e.grid(row=row+i+1, column=column+j+1, sticky="nsew", padx=1, pady=1, ipady=5)     
            cells[(row+i+1, column+j+1)]=e

def draw9x9grid():
    colour="light grey"
    for rowNo in range(1,10,3):
        for colNo in range(0,9,3):
            draw3x3grid(rowNo, colNo, colour)
            if colour=="light grey":
                colour="silver"
            else:
                colour="light grey"
###############################################

draw9x9grid()
timer_bool=tkinter.IntVar()
tkinter.Checkbutton(root, text="Display runtime", variable=timer_bool).grid(row=2, column=0, sticky="w", padx=20)

def get_board():
    """Returns the current state of the GUI board as a 2D list, ready for solving."""
    board=[]
    for row in range(2,11):
        row_temp=[]
        for column in range(1,10):
            digit=cells[(row, column)].get()
            if digit=="": # empty cells are appended as zeroes, to match my sudoku solver logic
                row_temp.append(0)
            else:
                row_temp.append(int(digit))
        board.append(row_temp)
    return board

def solve_grid():

    if all(all(cell==0 for cell in row) for row in get_board()): # checks the board definitely has some inputs
        print("Board empty! Cannot solve.")
        return
    
    start_time=time.time() # timer begins
    solutions_list=[] 

    try:
        print("Board to solve:")
        for line in get_board():
            print(line)
            
        solutions_list=solve_sudoku_MRV(get_board())
    except Exception as e:
        print("\nError occurred during solving:", e)
        return

    if timer_bool.get()==1: # "display runtime" box is checked
        elapsed_time=time.time()-start_time
        print(f"\nTime elapsed: {elapsed_time:.4f} seconds")

    if len(solutions_list)==0:
        print("\nNo Solutions were found for this puzzle!")
    else:
        print(f"\nTotal solutions found: {len(solutions_list)}")
        for solution in solutions_list:
            for line in solution:
                print(line)
        

solve_button=tkinter.Button(root, text="Solve", bg="light grey", command=solve_grid)
solve_button.grid(row=2, column=0, pady=10)

tkinter.mainloop()
