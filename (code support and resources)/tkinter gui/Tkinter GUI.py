import tkinter as tk

window=tk.Tk()
window.title("SudokuSolver")
window.geometry("400x400")

greeting=tk.Label(text="Welcome to the Sudoku Solver!",font=("Yu Gothic",12))
greeting.grid(row=0,column=0,columnspan=10,pady=10,sticky="news")

#error message, initially empty but can be configured to display errors later
errLabel=tk.Label(window,text="",fg="red")
errLabel.grid(row=2,column=1,columnspan=10)

solvedLabel=tk.Label(window,text="",fg="green")
solvedLabel.grid(row=3,column=1,columnspan=10)



window.mainloop()



