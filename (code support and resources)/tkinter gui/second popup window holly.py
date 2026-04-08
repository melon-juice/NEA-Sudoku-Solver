#second window

import tkinter as tk
def open_new_window():
   new_window = tk.Toplevel(root) # Create a new window
   new_window.title("Second Window")
   new_window.geometry("300x200")
   tk.Label(new_window, text="This is the second window").pack(pady=20)

# Main Window
root = tk.Tk()
root.title("Main Window")
root.geometry("400x300")
tk.Button(root, text="Open Second Window", command=open_new_window).pack(pady=20)
root.mainloop()
