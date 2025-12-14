from tkinter import *

root=Tk()
root.title("Sudoku Solver")
root.geometry("324x420")

label=Label(root,text="Fill in the numbers and click solve",pady=20)
label.grid(row=0,column=1,columnspan=10,sticky="news")
errLabel=Label(root,text="",fg="red")
errLabel.grid(row=15,column=1,columnspan=10)

solvedLabel=Label(root,text="",fg="green")
solvedLabel.grid(row=15,column=1,columnspan=10)

cells={}

def ValidateNumber(P):
    out=(P.isdigit()or P=="") and len(P)<2 
    return out

reg=root.register(ValidateNumber)

def draw3x3grid(row,column,bgcolour):
    for i in range(3):
        for j in range(3):
            e=Entry(root,width=5,bg=bgcolour,justify="center",validate="key",validatecommand=(reg,"%P"))
            e.grid(row=row+i+1,column=column+j+1,sticky="nsew",padx=1,pady=1,ipady=5)     
            cells[(row+i+1,column+j+1)]=e

def draw9x9grid():
    colour="#E2DAD2"
    for rowNo in range(1,10,3):
        for colNo in range(0,9,3):
            draw3x3grid(rowNo,colNo,colour)
            if colour=="#E2DAD2":
                colour="#D2E2E0"
            else:
                colour="#E2DAD2"

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


button=Button(root,command=getValues,text="Solve",width=10,bg="#E2DAD2",fg="#803938")
button.grid(row=16,column=6,columnspan=5,pady=10)

button=Button(root,command=clearValues,text="Clear",width=10,bg="#D2E2E0",fg="#388068")
button.grid(row=16,column=1,columnspan=5,pady=10)

draw9x9grid()
root.mainloop()
            
