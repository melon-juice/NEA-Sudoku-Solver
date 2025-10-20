#INCOMPLETE:
#This file solves a sudoku grid inputted, provided that:
###The grid is passed in as a 2D list
###The 'blank' squares are denoted by 0
###The inputted sudoku grid is solveable

global sudoku_grid = [] #grid here

class stack:
    #used to stack up attempts
    #if a conflict is found in main(),
        #then the stack is popped to restore the previous commit
    pass

def allowed(x,y,test_num):
    #checks for conflicts with rows and columns
    #returns boolean TRUE if test_num can be in (x,y) else FALSE
    pass

def main():
    #for column in grid:
        #for row in column:
            #if empty:
                #each num through (0-9):
                    #checked using allowed(column,row,num)
                    #if allowed() is true:
                        #set grid[row][column] as num
                        #push this commit to stack

main()


#Teacher's comments:
###Graphs: graph traversals (craig n dave) oop as opposed to modules
###Queues in oop class - to queue up the attempts in backtracking
###Tkinter or Pyqt for UI


