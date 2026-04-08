import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Undo and Redo Example - tutorialkart.com")
root.geometry("400x200")

# Stack to store text history
undo_stack = [""]
redo_stack = []

# Function to update undo stack on text change
def on_text_change(event=None):
    current_text = entry_widget.get()
    if undo_stack[-1] != current_text:
        undo_stack.append(current_text)
    # Clear redo stack on new input
    redo_stack.clear()

# Function to handle undo
def undo_action(event=None):
    if len(undo_stack) > 1:
        redo_stack.append(undo_stack.pop())
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, undo_stack[-1])

# Function to handle redo
def redo_action(event=None):
    if redo_stack:
        text = redo_stack.pop()
        undo_stack.append(text)
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, text)

# Create an Entry widget
entry_widget = tk.Entry(root, width=40, font=("Arial", 12))
entry_widget.pack(pady=20)

# Capture every key press to track changes
entry_widget.bind("<KeyRelease>", on_text_change)

# Create Undo and Redo buttons
btn_undo = tk.Button(root, text="Undo", command=undo_action)
btn_undo.pack(side="left", padx=20)

btn_redo = tk.Button(root, text="Redo", command=redo_action)
btn_redo.pack(side="right", padx=20)

# Bind keyboard shortcuts
root.bind("<Control-z>", undo_action)
root.bind("<Control-y>", redo_action)

# Run the Tkinter event loop
root.mainloop()
