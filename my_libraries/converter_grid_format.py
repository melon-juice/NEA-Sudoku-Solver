def convert_grid(grid):
    """converts format of grid between array (used during algorithm implementation)
    and single line (for storage)"""

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