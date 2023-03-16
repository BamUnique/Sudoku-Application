from PyQt6.QtWidgets import QGroupBox, QMainWindow, QApplication, QGridLayout, QSpinBox, QSizePolicy, QPushButton, QLabel
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont
import sys
from random import randrange
from sudoku import Sudoku
import logging

class Window(QMainWindow):
    
    difficulty_list = {"Easy": 0.5, "Medium": 0.6, "Hard": 0.7, "Expert": 0.8}
        
    def __init__(self, given_difficulty, loaded_account = None):
        super().__init__()
        
        self.hint_mode = False
        self.testing_val = False
        self.error_cell_list = {}
        
        if loaded_account is not None:
            self.account_data = loaded_account
            self.logged_in = True
        
        self.setWindowTitle('Sudoku Grid')
        self.setGeometry(100, 100, 450, 450)
        
        puzzle = self.getBoard(given_difficulty, 100)
        solved_puzzle = puzzle.solve()
        
        self.unsolved_board = puzzle.board
        self.solved_board = solved_puzzle.board
        
        self.difficulty = given_difficulty
        
        self.button = QPushButton('Check Solve', self)
        self.button.clicked.connect(self.checkBoard)
        
        self.timer_label = QLabel('00:00', self)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setFont(QFont('Arial', 20))
        
        self.buttonGrid = QGridLayout()
        self.buttonGrid.addWidget(self.button, 0, 0)
        self.buttonGrid.addWidget(self.timer_label, 0, 1)
        self.buttonGrid.setSpacing(10)
        
        #Creates times and runs the function to update every 0.1 seconds as if i run it every second sometimes the timer messes up the time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)
        self.start_time = None
        
        self.makeGrid()
        self.setBoard()
        
        self.reset_button = QPushButton("Reset Board", self)
        self.reset_button.move(450, 50)
        self.reset_button.clicked.connect(self.reset_board)
        
        self.difficulty_label = QLabel("NONE", self)
        self.difficulty_label.setFont(QFont('Arial', 20))
        self.difficulty_label.move(int(550-(self.difficulty_label.width())), 20)
        self.difficulty_label.adjustSize()
        
        self.personal_best_time = QLabel("None", self)
        self.personal_best_time.setFont(QFont('Arial', 18))
        self.personal_best_time.move(550, 200)
        
        self.testing_button = QPushButton("Testing", self)
        self.testing_button.move(500, 100)
        self.testing_button.clicked.connect(lambda: self.setup_board("Expert"))
        
        self.hint_button = QPushButton("Hint", self)
        self.hint_button.move(500, 140)
        self.hint_button.clicked.connect(lambda :setattr(self, 'hint_mode', True))
        
        self.testing_button2 = QPushButton("Conflicting Values", self)
        self.testing_button2.move(500, 160)
        self.testing_button2.clicked.connect(lambda :setattr(self, 'testing_val', True))
        
    def setup_board(self, difficulty):
        self.solved_board = None
        difficulty_num = self.difficulty_list[difficulty]
        seed = randrange(sys.maxsize)
        
        self.set_difficulty_label(difficulty)
        board = self.getBoard(difficulty_num, seed)
        self.applyBoard(board.board)
        self.solved_board = board.solve().board
        
        self.timer.start()

    
    def set_difficulty_label(self, difficulty_text):
        self.difficulty_label.setText(difficulty_text)
        
                
    def getBoard(self, difficulty, seed):
        puzzle = Sudoku(3, seed=seed).difficulty(difficulty)
        return puzzle
    
    
    def applyBoard(self, board):
        for row_index, current_row in enumerate(board):
            for col_index, value in enumerate(current_row):
                
                if value is not None:
                    cell = self.returnCell(col_index, row_index)
                    
                    if cell is not None:
                        cell.setValue(value)
                        cell.setReadOnly(True)
                        cell.setStyleSheet("background-color: #bab7b6; color: black;")
                        
        
    def returnCell(self, col : int, row : int) -> QSpinBox:
        """
        Returns the cell of position row, col in the sudoku grid.

        Args:

        Returns:
            QSpinBox: cell of position row, col
        """
        
        inner_row = row // 3
        inner_col = col // 3
        inner_group_box = self.outer_grid_layout.itemAtPosition(inner_row, inner_col).widget()
        
        cell_row = row % 3
        cell_col = col % 3
        
        cell_name = f"spinBox_{cell_row}_{cell_col}"
        cell = inner_group_box.findChild(QSpinBox, cell_name)
        
        return cell
    
    
    def reset_board(self):
        for row in range(9):
            for col in range(9):
                cell = self.returnCell(col, row)
                
                if cell is not None:
                    cell.setReadOnly(False)
                    cell.setStyleSheet("background-color: white; color: black;")
                    cell.setValue(0)
        self.timer_label.setText("00:00")
        self.start_time = None
        self.timer.stop() 

        
    # Runs this function every time that the timer see's that 0.1 seconds has passes
    def update(self):
        if self.start_time is None:
            self.start_time = QDateTime.currentDateTime()
            
        self.elapsed = self.start_time.secsTo(QDateTime.currentDateTime())
        minutes = self.elapsed // 60
        seconds = self.elapsed % 60
        
        time_str = f"{minutes:02}:{seconds:02}"
        self.timer_label.setText(time_str)
        
    
    def splitStyleSheet(self, style_sheet : str) -> str:
        """
        Returns the style_sheet but split into background_color and color variables.

        Args:
            style_sheet (str): Style sheet of an object given in text form.

        Returns:
            background_color (str): background color of the style sheet.
            color (str): color value of the style sheet.
        """
        style_sheet = style_sheet[18:]
        index = str.find(style_sheet, " color: ")
        color = style_sheet[index+8:len(style_sheet)-1]

        return style_sheet[:index-1], color
        
    
    def adjustConflicting(self, cell : QSpinBox, style_sheet : str, conflicting : bool):
        """
        Determines whether the cell needs to have the value color changed to red or black.

        Args:
            cell (QSpinBox): cell that needs to have its color changed.
            style_sheet (str): cells style_sheet
            conflicting (bool): True if the cell is a conflicting value, False if not.
        """
        
        background_color, color = self.splitStyleSheet(style_sheet)
        if color != "#1962ff":
            if conflicting:
                cell.setStyleSheet(f"background-color: {background_color}; color: red;")
            else:
                cell.setStyleSheet(f"background-color: {background_color}; color: black;")
            
    
    
    def checkCellContainer(self, cell : QSpinBox, error_cell_siblings : list):
        """
        Returns the value of all the cells in the parent of the cell given as a list.

        Args:
            cell (QSpinBox): cell being checked with its siblings.
            error_cell_sibling (list): List that will contain the cell siblings.

        Returns:
            valueList (list): list of all values.
            cell.parent().objectName(): name of the parent container.
        """
        
        x, y = map(int, cell.parent().objectName().split("_")[1:])
        for row in range(3):
            for col in range(3):
                cell_sibling = self.returnCell((col+(3*y)), (row+(3*x)))
                if cell_sibling != cell:
                    if cell_sibling.value() == cell.value():
                        self.adjustConflicting(cell, cell.styleSheet(), True)
                        self.adjustConflicting(cell_sibling, cell_sibling.styleSheet(), True)
                        if cell_sibling not in error_cell_siblings:
                            error_cell_siblings.append(cell_sibling)
                        
        return error_cell_siblings
                
        
        
    def checkConflicting(self):
        self.conflicted = False
        error_cell_siblings = []
        if self.testing_val:
            sender = self.sender()
            cell_name = sender.objectName()
            cell_parent = sender.parent().objectName() 
            
            x_factor, y_factor = map(int, cell_parent.split("_")[1:])
            cell_row, cell_col = map(int, cell_name.split("_")[1:])
            cell_row, cell_col = cell_row+(3*x_factor), cell_col+(3*y_factor)
            
            cell = self.returnCell(cell_col, cell_row)
            
            if cell.objectName() in self.error_cell_list:
                for cell_obj in self.error_cell_list[cell.objectName()]:
                    self.adjustConflicting(cell_obj, cell_obj.styleSheet(), False)
                    
            check_value = cell.value()
            
            
            for row in range(9):
                if row != cell_row:
                    cell_sibling = self.returnCell(cell_col, row)
                    value = cell_sibling.value()
                    if check_value == value:
                        self.adjustConflicting(cell, cell.styleSheet(), True)
                        self.adjustConflicting(cell_sibling, cell_sibling.styleSheet(), True)
                        self.conflicted = True
                        error_cell_siblings.append(cell_sibling)
            
            for col in range(9):
                if col != cell_col:
                    cell_sibling = self.returnCell(col, cell_row)
                    value = cell_sibling.value()
                    if check_value == value:
                        self.adjustConflicting(cell, cell.styleSheet(), True)
                        self.adjustConflicting(cell_sibling, cell_sibling.styleSheet(), True)
                        self.conflicted = True
                        error_cell_siblings.append(cell_sibling)
                        
            error_cell_siblings = self.checkCellContainer(cell, error_cell_siblings)
                
            if self.conflicted:
                self.error_cell_list[f"{cell.objectName()}"] = error_cell_siblings
            else:
                self.adjustConflicting(cell, cell.styleSheet(), False)
            self.conflicted = False
        
        
    def hint(self):
        if self.hint_mode:
            sender = self.sender()
            cell_name = sender.objectName()
            
            cell_parent = sender.parent().objectName()
            x_factor = int(cell_parent[14:15])
            y_factor = int(cell_parent[16:17])
            
            cell_row, cell_col = map(int, cell_name.split("_")[1:])
            cell_row , cell_col = cell_row + (3*x_factor), cell_col + (3*y_factor)
            
            cell = self.returnCell(cell_col, cell_row)

            if not cell.isReadOnly():
                cell.setValue(self.solved_board[cell_row][cell_col])
                cell.setStyleSheet("background-color: white; color: #1962ff;")
                cell.setReadOnly(True)
            
            self.hint_mode = False
        
        
    def makeGrid(self):
        central_widget = QGroupBox(self)
        # central_widget.setFixedSize(450, 450)
        self.setCentralWidget(central_widget)
        
        self.cell_size = (45, 45)
        
        self.outer_grid_layout = QGridLayout()
        self.outer_grid_layout.setSpacing(0)
        self.outer_grid_layout.addLayout(self.buttonGrid, 3, 3, alignment=Qt.AlignmentFlag.AlignBottom)
        

        central_widget.setLayout(self.outer_grid_layout)
        
        for i in range(3):
            for j in range(3):
                inner_group_box = QGroupBox(central_widget)
                inner_group_box.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                self.inner_group_box_layout = QGridLayout()
                self.inner_group_box_layout.setSpacing(0)
                self.inner_group_box_layout.setContentsMargins(0, 0, 0, 0)
                inner_group_box.setLayout(self.inner_group_box_layout)
                inner_group_box.setObjectName(f"cellContainer_{i}_{j}")
                self.outer_grid_layout.addWidget(inner_group_box, i, j, alignment=Qt.AlignmentFlag.AlignCenter)
                
                for x in range(3):
                    for y in range(3):
                        cell = QSpinBox()
                        cell.setStyleSheet("background-color: white; color: black;")
                        cell.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
                        cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        cell.setFixedSize(*self.cell_size)
                        cell.setFont(QFont('Arial', 20))
                        cell.setSpecialValueText(" ")
                        cell.setMaximum(9)
                        # cell.valueChanged.connect(self.setBoard)
                        cell.setObjectName(f"spinBox_{x}_{y}")
                        self.inner_group_box_layout.addWidget(cell, x, y)
                        cell.editingFinished.connect(self.hint)
                        cell.valueChanged.connect(self.checkConflicting)
                        
                        
    
    def checkBoard(self):
        currentGrid = [[],[],[],[],[],[],[],[],[]]
        for row in range(9):
            for col in range(9):
                cell = self.returnCell(col, row)
                if cell is not None:
                    currentGrid[row].append(cell.value())
        for i in range(9):
            print(*currentGrid[i])  
        if currentGrid == self.solved_board:
            logging.info("Puzzle is solved")
            self.timer.stop()
        else:
            logging.info("Puzzle is not solved")
                
    def setCell(self, row: int, col: int, value: int):
        
        # calculate the position of the inner group box containing the cell
        inner_row = row // 3
        inner_col = col // 3
        inner_group_box = self.outer_grid_layout.itemAtPosition(inner_row, inner_col).widget()
        
        cell_row = row % 3
        cell_col = col % 3

        cell_name = f"spinBox_{cell_row}_{cell_col}"
        cell = inner_group_box.findChild(QSpinBox, cell_name)

        if cell is not None:
            if value is not None:
                cell.setValue(value)
                if value != 0:
                    cell.setReadOnly(True)
                    cell.setStyleSheet("background-color: #bab7b6; color: black;")

  
    def setBoard(self):
        for i in range(9):
            for j in range(9):
                self.setCell(i, j, self.unsolved_board[i][j])
    
    
    
if __name__ == '__main__':
    
    level = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)
    
    app = QApplication(sys.argv)
    sudoku = Window(0.6)
    sudoku.setCell(3, 1, 5)
    

    sudoku.show()
    
    sys.exit(app.exec())