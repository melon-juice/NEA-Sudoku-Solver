import tkinter
from tkinter import messagebox

# all "pages" are frames stacked in the same container


class application(tkinter.Tk): # class inherits fron tkinter.Tk
    def __init__(self):
        super().__init__()

        self.title("Main Menu")
        self.geometry("350x300")
        self.resizable(False, False)

        # a container is initialised to hold all frames
        container=tkinter.Frame(self)
        container.pack(fill="both", expand=True) # container expanded to fill the whole window
        self.frames={} # all frames are managed in a dictionary

        # each frame is initialised and stored
        for F in (log_in_menu, main_menu, staff_details, take_order, view_order):
            frame=F(parent=container,controller=self)
            self.frames[F]=frame # frame is stored in dictionary
            frame.grid(row=0,column=0,sticky="nsew") # frame is created (this line is necessary)
       
        self.show_frame(log_in_menu) # the log in page is placed at the top

    def show_frame(self,frame_name):
        """switches between frames by raising them to the top"""
        frame=self.frames[frame_name]
        frame.tkraise() # frame is sent to the top, making it the frame that the user views

#all pages/sub-pages inherit from tkinter.frame
#are all initialised inside main container
class log_in_menu(tkinter.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #staff id - then use id to retrieve from databse to compare passwords
        tkinter.Label(self, text="Enter staff ID:").grid(column=0, row=1, pady=5, padx=5)
        self.staffID_entry=tkinter.Entry(self)
        self.staffID_entry.grid(column=1,row=1)

        # password label and entry
        tkinter.Label(self, text="Password:").grid(column=0, row=4, pady=5, padx=5)
        #password_entry =tkinter.Entry(self)
        #version that hashes the entry
        self.password_entry =tkinter.Entry(self, show="*")
        self.password_entry.grid(column=1, row=4, pady=5, padx=5)

        # Login button - when pressed it runs login() function
        login_button =tkinter.Button(self, text="Login", command=self.log_in_btn_pressed, width=15, bg="#08F118")
        login_button.grid(column=1, row=5, pady=5, padx=5)

    def log_in_btn_pressed(self):
        staffID=self.staffID_entry.get()
        password = self.password_entry.get()
        print("id,pass from ENTRY;",staffID,password,"\n")

        messagebox.showinfo("Login Successful", "Welcome to the system!")
        self.controller.show_frame(main_menu)

class main_menu(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tkinter.Label(self, text="Welcome to the HOME page").grid(column=0, row=0)

        staff_details_btn =tkinter.Button(self, text="Staff Details",
            command=lambda: controller.show_frame(staff_details), width=20)
        staff_details_btn.grid(column=1, row=1, pady=5)

        take_order_btn =tkinter.Button(self, text="Take New Order",
            command=lambda: controller.show_frame(take_order), width=20)
        take_order_btn.grid(column=1, row=2, pady=5)

        view_orders_btn =tkinter.Button(self, text="View Current Orders",
            command=lambda: controller.show_frame(view_order), width=20)
        view_orders_btn.grid(column=1, row=3, pady=5)

        quit_button =tkinter.Button(self, text="Quit", command=controller.destroy, width=15, bg="#08F118")
        quit_button.grid(column=1, row=4, pady=5)

class staff_details(tkinter.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller=controller

        tkinter.Label(self, text="Welcome FIRSTNAME SURNAME").grid(column=0, row=0)
        tkinter.Label(self, text="View all details:").grid(column=0, row=1)
        tkinter.Label(self, text=" ").grid(column=0, row=2)

        back_btn =tkinter.Button(self, text="🏠 HOME",
            command=lambda: controller.show_frame(main_menu))
        back_btn.grid(column=1, row=3, pady=5)

class take_order(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label =tkinter.Label(self, text="Take order")
        label.grid(column=0, row=0)

        back_btn =tkinter.Button(self, text="🏠 HOME",
            command=lambda: controller.show_frame(main_menu))
        back_btn.grid(column=1, row=1, pady=5)

class view_order(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller=controller
       
        label =tkinter.Label(self, text="View Orders")
        label.grid(column=0, row=0)

        back_btn =tkinter.Button(self, text="🏠 HOME",
            command=lambda: controller.show_frame(main_menu))
        back_btn.grid(column=1, row=1, pady=5)

if __name__ == "__main__":
    app = application()
    app.mainloop()
