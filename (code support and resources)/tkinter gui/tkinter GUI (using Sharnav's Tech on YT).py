from tkinter import *

root=Tk()
root.title("Sudoku Solver")
root.geometry("324x550")

label=Label(root,text="Fill in the numbers and click solve").grid(row=0,column=1,columnspan=10)
errLabel=Label(root,text="",fg="red")
errLabel.grid(row=15,column=1,columnspan=10,pady=5)

solvedLabel=Label(root,text="",fg="green")
solvedLabel.grid(row=15,column=1,columnspan=10,pady=5)

cells={}

def ValidateNumber(P):
    out=(P.isdigit()or P=="") and len(P)<2
    return out

reg=root.register(ValidateNumber)

def draw3x3grid(row,column,bgcolor):
    for i in range(3):
        for j in range(3):
            e=Entry(root,width=5,bg=bgcolor,justify="center",validate="key",validatecommand=(reg,"%P"))
            e.grid(row=row+i+1, column=column+j+1,sticky="nsew",padx=1,pady=1,ipady=5)     
            cells[(row+i+1,column+j+1)]=e

def draw9x9grid():
    color="#D0ffff"
    for rowNo in range(1,10,3):
        for colNo in range(0,9,3):
            draw3x3grid(rowNo,colNo,color)
            if color=="#D0ffff":
                color="#ffffd0"
            else:
                color="#D0ffff"

def clearValues():
    errLabel.configure(text="")
    solvedLabel.configure(text="")
    for row in range(2,11):
        for col in range(1,10):
            cell=cells[(row,col)]
            cell.delete(0,"end")

def getValues():
    board=[]
    errLabel.configure(text="")
    solvedLabel.configure(text="")
    for row in range(2,11):
        rows=[]
        for col in range(1,10):
            val=cells[(row,col)].get()
            if val=="":
                rows.append(0)
            else:
                rows.append(int(val))
                
        board.append(rows)


button=Button(root,command=getValues,text="Solve",width=10)
button.grid(row=30,column=1,columnspan=5,pady=20)

button=Button(root,command=clearValues,text="Clear",width=10)
button.grid(row=20,column=1,columnspan=5,pady=20)

draw9x9grid()
root.mainloop()
            
