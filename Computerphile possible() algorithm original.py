import numpy as np

def possible(y,x,n):
    """
    *CODE BY COMPUTERPHILE ON YOUTUBE, COMMENTS BY HAJAR*
    Function checks whether a number is allowed in a particular grid position.
    inputs: coordinates(x,y) & number being tested(n)
    output: Boolean True/False
    """
    global gird
    for i in range(0,9):
        if grid[y][i]==n: #if any space in the row already takes on n
            return False
    for i in range(0,9):
        if grid[i][x]==n: #if any space in the column already takes on n
            return False
    x0=(x//3)*3 #lowest value of x within the same square
    y0=(y//3)*3 #lowest value of y within the same square
    for i in range(0,3):
        for j in range(0,3):
            if grid[y0+1][x0+j]==n: #if any space in the square already takes on n
                return False
    return True

grid = [
    [3, 0, 6, 5, 0, 8, 4, 0, 0],
    [5, 2, 0, 0, 0, 4, 0, 0, 0],
    [0, 8, 7, 0, 0, 0, 0, 3, 1],
    [0, 0, 3, 0, 1, 0, 0, 8, 0],
    [9, 0, 0, 8, 6, 3, 0, 0, 5],
    [0, 5, 0, 0, 9, 0, 6, 0, 0],
    [1, 3, 0, 0, 0, 0, 2, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 7, 4],
    [0, 0, 5, 2, 0, 6, 3, 1, 0]]

def solve():
    global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x]==0:
                for n in range(1,10):
                    if possible(y,x,n):
                        grid[y][x]=n
                        solve()
                        grid[y][x]=0
                return

    for line in grid:
        print("\t",line)
    input("More?") #inserts runtime break; user is given choice to continue
    #algorithm will output every possible solution
    
solve()
