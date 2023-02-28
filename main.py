from sudoku import Sudoku
import newgui
import math
import sys


def remake_grid(grid):
    new_grid = [[],[],[],[],[],[],[],[],[]]
    for j in range(9):
        adjuster_value = (((math.ceil((j+1)/3))-1)*3)
        for i in range(9):
            checker = i+1
            listValue = (math.ceil(checker/3)-1 + adjuster_value)
            if grid[j][i] == None:
                grid[j][i] = 0
            new_grid[listValue].append(grid[j][i])
    return new_grid
    

if __name__ == '__main__':
    
    puzzle = Sudoku(3).difficulty(0.6)
    app = newgui.QApplication(sys.argv)
    puzzleSolved = puzzle.solve()
    print(puzzleSolved)
    window = newgui.Window(puzzleSolved.board)
    for i in range(9):
        for j in range(9):
            window.setCell(i, j, puzzle.board[i][j])
    

    window.show()
    
    sys.exit(app.exec())

    
                
