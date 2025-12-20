def display(grid):
    board=[]
    for row in range(9):
        for col in range(9):
            if grid[row][col]==0:
                board.append(" ")
            else:
                board.append(grid[row][col])

    thickdash=3*"\u2550"
    thindash=3*"\u2500"

    print("\u2554"+3*(thickdash+"\u2564"+thickdash+"\u2564"+thickdash+"\u2557"),
    "\n\u2551",board[0],"\u2502",board[1],"\u2502", board[2],"\u2551",board[3],"\u2502",board[4],"\u2502",board[5],"\u2551",board[6],"\u2502",board[7],"\u2502",board[8],"\u2551",
    "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u2562"),
    "\n\u2551",board[9],"\u2502",board[10],"\u2502", board[11],"\u2551",board[12],"\u2502",board[13],"\u2502",board[14],"\u2551",board[15],"\u2502",board[16],"\u2502",board[17],"\u2551",
    "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u2562"),
    "\n\u2551",board[18],"\u2502",board[19],"\u2502", board[20],"\u2551",board[21],"\u2502",board[22],"\u2502",board[23],"\u2551",board[24],"\u2502",board[25],"\u2502",board[26],"\u2551",
    "\n\u2560"+3*(thickdash+"\u256A"+thickdash+"\u256A"+thickdash+"\u2563"),
        
    "\n\u2551",board[27],"\u2502",board[28],"\u2502", board[29],"\u2551",board[30],"\u2502",board[31],"\u2502",board[32],"\u2551",board[33],"\u2502",board[34],"\u2502",board[35],"\u2551",
    "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u2562"),
    "\n\u2551",board[36],"\u2502",board[37],"\u2502", board[38],"\u2551",board[39],"\u2502",board[40],"\u2502",board[41],"\u2551",board[42],"\u2502",board[43],"\u2502",board[44],"\u2551",
    "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u2562"),
    "\n\u2551",board[45],"\u2502",board[46],"\u2502", board[47],"\u2551",board[48],"\u2502",board[49],"\u2502",board[50],"\u2551",board[51],"\u2502",board[52],"\u2502",board[53],"\u2551",
    "\n\u2560"+3*(thickdash+"\u256A"+thickdash+"\u256A"+thickdash+"\u2563"),

    "\n\u2551",board[54],"\u2502",board[55],"\u2502", board[56],"\u2551",board[57],"\u2502",board[58],"\u2502",board[59],"\u2551",board[60],"\u2502",board[61],"\u2502",board[62],"\u2551",
    "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u2562"),
    "\n\u2551",board[63],"\u2502",board[64],"\u2502", board[65],"\u2551",board[66],"\u2502",board[67],"\u2502",board[68],"\u2551",board[69],"\u2502",board[70],"\u2502",board[71],"\u2551",
    "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u2562"),
    "\n\u2551",board[72],"\u2502",board[73],"\u2502", board[74],"\u2551",board[75],"\u2502",board[76],"\u2502",board[77],"\u2551",board[78],"\u2502",board[79],"\u2502",board[80],"\u2551",
    "\n\u255A"+3*(thickdash+"\u2567"+thickdash+"\u2567"+thickdash+"\u255D"))

##grid=[[0,0,0,0,0,7,5,0,0],
##    [7,0,0,1,0,0,0,4,0],
##    [5,0,0,0,0,0,2,0,0],
##    [0,0,1,3,9,0,0,0,8],
##    [3,0,0,7,8,6,0,0,4],
##    [8,0,0,0,4,1,7,0,0],
##    [0,0,8,0,0,0,0,0,9],
##    [0,5,0,0,0,3,0,0,1],
##    [0,0,4,6,0,0,0,0,0]]


##display(grid)



