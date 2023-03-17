import sudoku
import numpy as np

class SudokuBoard:
    """
    The SudokuBoard class is responsible for creating and managing the board.
    """
    def __init__(self, difficulty : float = 0.1, seed : int = None):
        self.difficulty = difficulty
        self.seed = seed

        
        self.board = None
        self.solution = None
        self.locked = None
        
        self._initialize_board()
        
    def _initialize_board(self):
        """Initializes the board and board solution as numpy arrays"""
        s = sudoku.Sudoku(3, seed=self.seed).difficulty(self.difficulty)
        self.starting_board = np.array(s.board)
        self.board = np.array(s.board)
        self.solution = np.array(s.solve().board)
        self.locked = np.array([[None for i in range(10)] for i in range(10)])
        self.lock(self.board)

    
    # def get_cell(self, row : int, col : int, cellwise : bool = False):
    #     """Gets the value of a cell"""
    #     if cellwise:
    #         sx = (row % 3) * 3
    #         sy = (col % 3) * 3
            
    #         cx = col % 3
    #         cy = col // 3
            
    #         cell_value = self.board[sy + cy][sx + cx]
            
    #         return cell_value
        
    #     else:
    #         return self.board[row][col]
    
        
    def set_cell(self, row : int, col : int, value : int | None, cellwise : bool = False):
        """Sets the value of a cell"""
        if cellwise:
            
            sx = (row % 3) * 3
            sy = (col % 3) * 3
            
            cx = col % 3
            cy = col // 3
            
            self.board[sy + cy][sx + cx] = value
            
        else:
            self.board[row][col] = value
            
    
    def lock(self, itemToLock : list):
        """
        Locks a list. For examples makes sure that if a cell is locked then it cannot be changed
        """
        for row, val in enumerate(itemToLock):
            for col, val in enumerate(itemToLock[row]):
                if val is not None:
                    self.locked[row][col] = 0
            
    
    def check_if_locked(self, row : int, col : int, locked : bool = False):
        """Checks if a index in a list is locked. If so then actions cannot be performed on said list"""
        if row > 9 or row < 0 or col > 9 or col < 0:
            print("ERROR")
            
            
        else:
            if self.locked[row][col] == 0:
                locked = True
            
            return locked
        
if __name__ == "__main__":
    sb = SudokuBoard()
    locked = sb.check_if_locked(10, 10)
