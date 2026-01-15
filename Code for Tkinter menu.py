from tkinter import *
from tkinter import messagebox

root=Tk()

def go_home():
    if messagebox.askokcancel("Confirm","Close current window?"):
        #closes current window
        #opens home window
        print("Home page requested")

def open_tutorial():
    #open tutorial window
    print("Tutorial page requested")

def open_tricks():
    #open tricks page
    print("Sudoku tricks page requested")
      
def create_menu(root):
    menubar=Menu(root)
    app_menu=Menu(menubar, tearoff=0)
    menubar.add_cascade(label ="Menu", menu=app_menu)
    app_menu.add_command(label ="Home", command=go_home)
    app_menu.add_command(label ="Tutorial", command=open_tutorial)
    app_menu.add_command(label ="Sudoku Tricks", command=open_tricks)
    app_menu.add_separator()
    app_menu.add_command(label ="Exit App",
        command=lambda: messagebox.askokcancel("Confirm","Close app?") and root.destroy())
    root.config(menu=menubar)

create_menu(root)
root.mainloop()
