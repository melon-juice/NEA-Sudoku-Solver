def convert_grid(grid):
    """converts format of grid between array (used during algorithm implementation) and single line (for storage)"""

    if type(grid)==list: # 2d array -> single line
        single_line=""
        for row in grid:
            for element in row:
                single_line+=str(element)
        return single_line

    else: # single line -> 2d array
        grid_list=[[],[],[],[],[],[],[],[],[]]
        for i in range(9):
            j=i*9
            for digit in grid[j+0:j+9]:
                grid_list[i].append(int(digit))

        return grid_list


####driver code

# grid=[[7,9,4,0,8,6,3,1,0],
# [1,0,2,0,7,3,5,8,9],
# [0,5,0,0,9,2,0,0,0],
# [0,0,0,7,5,0,1,2,0],
# [0,0,7,3,0,0,0,9,6],
# [0,4,0,0,1,0,0,0,0],
# [4,3,0,0,0,0,0,5,1],
# [0,0,0,9,0,0,6,0,0],
# [6,0,1,0,3,0,0,0,0]]
# new=convert_grid(grid)

# print(new)
# print("///////")
# for line in grid:
#     print(line)
# print("///////")
# for line in convert_grid(new):
#     print(line)