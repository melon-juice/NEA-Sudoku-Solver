from UNICODEformatting import display

def allowed(x,y,n):

    global grid
    
    if grid[y][x]!=0:
        print("Selected square occupied.")
        return False
    
    for i in range(0,9):
        if grid[y][i]==n: #if any space in the row already takes on n
            print(f"Conflict found in row at: ({y},{i})")
            return False
    for i in range(0,9):
        if grid[i][x]==n: #if any space in the column already takes on n
            print(f"Conflict found in column at: ({i},{x})")
            return False

    x0=(x//3)*3 #lowest value of x within the same square
    y0=(y//3)*3 #lowest value of y within the same square

    for i in range(0,3):
        for j in range(0,3):
            if grid[y0+i][x0+j]==n: #if any space in the square already takes on n
                print("Conflict found in block")
                return False
    print("No conflicts found!")
    return True

grid=[[3, 0, 6, 5, 0, 8, 4, 0, 0],
      [5, 2, 0, 0, 0, 0, 0, 0, 0],
      [0, 8, 7, 0, 0, 0, 0, 3, 1],
      [0, 0, 3, 0, 1, 0, 0, 8, 0],
      [9, 0, 0, 8, 6, 3, 0, 0, 5],
      [0, 5, 0, 0, 9, 0, 6, 0, 0],
      [1, 3, 0, 0, 0, 0, 2, 5, 0],
      [0, 0, 0, 0, 0, 0, 0, 7, 4],
      [0, 0, 5, 2, 0, 6, 3, 0, 0]]

print("\npick a square coordinate then a number to test if it is valid")
display(grid)

while True:

    #at this point, inputs are assumed to be valid (integers in range)
    y=int(input("\nselect row(zero-indexed): "))
    x=int(input("select column(zero-indexed): "))
    num=int(input("select number (1-9) to test: "))

    allowed(x,y,num)
    if input("again?(y/n) ").lower()!="y":
        break
