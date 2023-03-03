from sudoku import Sudoku
import newgui
import math
import sys
import menu


# def remake_grid(grid):
#     new_grid = [[],[],[],[],[],[],[],[],[]]
#     for j in range(9):
#         adjuster_value = (((math.ceil((j+1)/3))-1)*3)
#         for i in range(9):
#             checker = i+1
#             listValue = (math.ceil(checker/3)-1 + adjuster_value)
#             if grid[j][i] == None:
#                 grid[j][i] = 0
#             new_grid[listValue].append(grid[j][i])
#     return new_grid
            
def chooseDifficulty():
    chosenDifficulty = int(input("Choose a difficulty from 1-4:\n"))
    chosenDifficulty -= 1
    difficulty_list = [0.5, 0.6, 0.7, 0.8]
    return difficulty_list[chosenDifficulty]

if __name__ == '__main__':
    
    # app = menu.QApplication(sys.argv)
    # main_menu = menu.SelectionMenu()
    # main_menu.show()
    
    chosen_difficulty = chooseDifficulty()
    
    app = newgui.QApplication(sys.argv)
    window = newgui.Window(chosen_difficulty)
    window.show()
    
    sys.exit(app.exec())

    
                
