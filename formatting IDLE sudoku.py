#sudoku game

board=[" "," ",8," "," "," "," "," "," ",
       4,9," ",1,5,7," "," ",2,
       " "," ",3," "," ",4,1,9," ",
       1,8,5," ",6," "," ",2," ",
       " "," "," "," ",2," "," ",6," ",
       9,6," ",4," ",5,3," "," ",
       " ",3," "," ",7,2," "," ",4,
       " ",4,9," ",3," "," ",5,7,
       8,2,7," "," ",9," ",1,3]

thickdash=3*"\u2550"
thindash=3*"\u2500"

print("\u2554"+3*(thickdash+"\u2564"+thickdash+"\u2564"+thickdash+"\u2566"),
          "\n\u2551",board[0],"\u2502",board[1],"\u2502", board[2],"\u2551",board[4],"\u2502",board[5],"\u2502",board[6],"\u2551",board[7],"\u2502",board[8],"\u2502",board[9],"\u2551",
          "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u256B"),
          "\n\u2551",board[10],"\u2502",board[11],"\u2502", board[12],"\u2551",board[13],"\u2502",board[14],"\u2502",board[15],"\u2551",board[16],"\u2502",board[17],"\u2502",board[18],"\u2551",
          "\n\u255F"+3*(thindash+"\u253C"+thindash+"\u253C"+thindash+"\u256B"),
          "\n\u2551",board[19],"\u2502",board[20],"\u2502", board[21],"\u2551",board[22],"\u2502",board[23],"\u2502",board[24],"\u2551",board[25],"\u2502",board[26],"\u2502",board[27],"\u2551",
          "\n\u2560"+3*(thickdash+"\u256A"+thickdash+"\u256A"+thickdash+"\u256C"))

