## not my code!

from func_timeout import func_timeout, FunctionTimedOut # used to output a timeout error when necessary
import time

def some_func():
    while True:
        print("Hello world")


try:
    start_time=time.time()
    func_timeout(2, some_func) # Timeout after 2 seconds
    
except FunctionTimedOut:
    elapsed_time=time.time()-start_time
    print("The subroutine timed out after 2 seconds.")

print(elapsed_time)


import tkinter
from tkinter import font
root = tkinter.Tk()
print(font.families())
    
