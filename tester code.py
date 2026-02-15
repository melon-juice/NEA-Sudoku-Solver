

with open(r"C:/Users/maria/OneDrive - Lancaster Girls' Grammar School/Python 6TH FORM/NEA-Sudoku-Solver/my_libraries/SingleStringGridArchive.txt", "r", encoding="utf-8") as file:
    single_line="090000060007015040004603100000000020900050003076000050000032600010500030050704209"
    for file_line in file.readlines():
        file_line=file_line.strip()
        print(file_line)
        if single_line==file_line:
            print("Already in file")            
    file.close()
