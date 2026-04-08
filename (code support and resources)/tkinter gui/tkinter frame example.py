import tkinter as tk

class PuzzleGameWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Puzzle Challenge")
        self.geometry("300x200")
        
        # This variable tracks the current frame being shown
        self.current_frame = None

        # Start by showing the Menu
        self.show_menu()

    def show_menu(self):
        """Builds and displays the difficulty selection menu."""
        # 1. Clear any existing frame
        if self.current_frame:
            self.current_frame.destroy()

        # 2. Create the container frame for the menu
        self.current_frame = tk.Frame(self)
        self.current_frame.pack(fill="both", expand=True)

        # 3. Add Menu Widgets
        tk.Label(self.current_frame, text="Select Difficulty", font=("Arial", 14)).pack(pady=20)

        # Pass specific arguments to the switch_to_puzzle method using lambda
        tk.Button(self.current_frame, text="Easy", 
                  command=lambda: self.switch_to_puzzle("Easy")).pack(pady=2)
        tk.Button(self.current_frame, text="Medium", 
                  command=lambda: self.switch_to_puzzle("Medium")).pack(pady=2)
        tk.Button(self.current_frame, text="Hard", 
                  command=lambda: self.switch_to_puzzle("Hard")).pack(pady=2)

    def switch_to_puzzle(self, difficulty):
        """Swaps the Menu frame for the Puzzle frame."""
        # 1. Clear the menu frame
        if self.current_frame:
            self.current_frame.destroy()

        # 2. Create the container frame for the puzzle
        self.current_frame = tk.Frame(self)
        self.current_frame.pack(fill="both", expand=True)

        # 3. Add Puzzle Widgets (Customized by difficulty)
        tk.Label(self.current_frame, text=f"{difficulty} Puzzle Mode", font=("Arial", 16, "bold")).pack(pady=20)
        
        puzzle_text = f"Solve this {difficulty.lower()} math problem..."
        tk.Label(self.current_frame, text=puzzle_text).pack(pady=10)

        # Example input area
        tk.Entry(self.current_frame).pack(pady=5)
        
        # Back Button to return to menu
        tk.Button(self.current_frame, text="Back to Menu", command=self.show_menu).pack(pady=20)


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x150")
        tk.Label(self, text="Main Application").pack(pady=20)
        tk.Button(self, text="Start Game", command=self.start_game).pack()

    def start_game(self):
        PuzzleGameWindow(self)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()