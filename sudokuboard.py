from PyQt6.QtWidgets import QGroupBox, QMainWindow, QApplication, QGridLayout, QSpinBox, QSizePolicy, QPushButton, QLabel, QDialog, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont
import sys
from random import randrange
from sudokumanager import SudokuBoard
from databasemanager import DatabaseManager

class Window(QMainWindow):
    
    difficulty_list = {"Easy": 0.6, "Medium": 0.6, "Hard": 0.7, "Expert": 0.8}
        
    def __init__(self, given_difficulty, loaded_account, currentWindow, pages_dict):
        super().__init__()
        
        self.hint_mode = False
        self.testing_val = False
        self.init_dialog = False
        self.error_cell_list = {}
        self.currentWindow = currentWindow
        self.pages_dict = pages_dict
        
        self.db = DatabaseManager()
        
        self.account_data = None
        
        if loaded_account is not None:
            self.account_data = loaded_account
            self.logged_in = True
        
        self.setWindowTitle('Sudoku Grid')
        self.setGeometry(100, 100, 450, 450)
        self.setFixedSize(618, 500)
    
        
        self.difficulty = given_difficulty

        self.button = QPushButton('Check Solve', self)
        self.button.clicked.connect(self.checkBoard)
        self.button.move(485, 450)
        
        self.back_button = QPushButton('⬅', self)
        self.back_button.setFont(QFont('Arial', 20))
        self.back_button.setGeometry(10, 5, 35, 42)
        self.back_button.clicked.connect(self.back)
        
        font = QFont("Arial", 20)
        font.setUnderline(True) # Adds underlines for TIME label
        self.time_label = QLabel("     Time       ", self)
        self.time_label.setFont(font)
        self.time_label.move(485, 56)
        font.setUnderline(False) # Removes underline for the timer
        self.timer_label = QLabel('00:00', self)
        # self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setFont(font)
        self.timer_label.move(515, 80)
        
        self.personal_best_time = QLabel('00:00', self)
        self.personal_best_time.setFont(font)
        self.personal_best_time.move(515, 140)
        
        font.setUnderline(True)
        self.best_time_label = QLabel(" Best Time      ", self)
        self.best_time_label.setFont(font)
        self.best_time_label.move(485, 116)

        #Creates times and runs the function to update every 0.1 seconds as if i run it every second sometimes the timer messes up the time
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)
        self.start_time = None
        
        self.makeGrid()
        
        font = QFont('Arial', 25)
        font.setUnderline(True)
        
        self.difficulty_label = QLabel("NONE", self)
        self.difficulty_label.setFont(font)
        self.difficulty_label.adjustSize()
        self.difficulty_label.move(190, 10)
        self.difficulty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
   
        
        self.hint_button = QPushButton("Hint", self)
        self.hint_button.setGeometry(485, 400, 70, 30)
        self.hint_button.clicked.connect(lambda :setattr(self, 'hint_mode', True))
        
        self.hint_number_button = QPushButton("3", self)
        self.hint_number_button.setGeometry(560, 400, 25, 30)
        
        if self.difficulty != 0:
            self.setup_board(self.difficulty)
        
    def setup_board(self, difficulty):
        self.testing_val = False
        self.reset_board()
        self.difficulty_index = difficulty[2]
        
        
        difficulty_num = difficulty[0]
        seed = randrange(sys.maxsize)
        self._sudoku = SudokuBoard(difficulty_num, seed)
        
        self.set_difficulty_label(difficulty[1])

        board = self._sudoku.board
        
        self.applyBoard(board)
        
        self.timer.start()
        self.testing_val = True
        
        self.hint_number_button.setText("3")

    
    def set_difficulty_label(self, difficulty_text):
        self.difficulty_label.setText(difficulty_text)
        self.difficulty_label.adjustSize()
        
        
    def back(self):
        self.currentWindow.setCurrentWidget(self.pages_dict["Difficulty Menu"])
    
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
            self._sudoku.set_cell(cell_row, cell_col, cell.value())
            
            # Check Row
            row_check, index_set = self._sudoku.check_row(cell_row, cell_col)
            if row_check:
                for pos_in_row in index_set:
                    self.adjustConflicting(cell=self.returnCell(pos_in_row, cell_row), style_sheet=self.returnCell(pos_in_row, cell_row).styleSheet(), conflicting=True)
                    self.conflicted = True
                    error_cell_siblings.append(self.returnCell(pos_in_row, cell_row))
            
            if cell.objectName() in self.error_cell_list:
                for cell_obj in self.error_cell_list[cell.objectName()]:
                    self.adjustConflicting(cell_obj, cell_obj.styleSheet(), False)
                    
            check_value = cell.value()
            
            col_check, index_set = self._sudoku.check_col(cell_row, cell_col)
            if col_check:
                for pos_in_col in index_set:
                    self.adjustConflicting(cell = self.returnCell(cell_col, pos_in_col), style_sheet=self.returnCell(cell_col, pos_in_col).styleSheet(), conflicting=True)
                    self.conflicted = True
                    error_cell_siblings.append(self.returnCell(cell_col, pos_in_col))
            
            # for col in range(9):
            #     if col != cell_col:
            #         cell_sibling = self.returnCell(col, cell_row)
            #         value = cell_sibling.value()
            #         if check_value == value:
            #             self.adjustConflicting(cell, cell.styleSheet(), True)
            #             self.adjustConflicting(cell_sibling, cell_sibling.styleSheet(), True)
            #             self.conflicted = True
            #             error_cell_siblings.append(cell_sibling)
                        
            error_cell_siblings = self.checkCellContainer(cell, error_cell_siblings)
                
            if self.conflicted:
                self.error_cell_list[f"{cell.objectName()}"] = error_cell_siblings
            else:
                self.adjustConflicting(cell, cell.styleSheet(), False)
            self.conflicted = False
        
        
    def hint(self):
        if self.hint_mode and self.hint_number_button.text() != "0":
            sender = self.sender()
            cell_name = sender.objectName()
            cell_parent = sender.parent().objectName()
            
            x_factor = int(cell_parent[14:15])
            y_factor = int(cell_parent[16:17])
            
            cell_row, cell_col = map(int, cell_name.split("_")[1:])
            cell_row , cell_col = cell_row + (3*x_factor), cell_col + (3*y_factor)
            
            cell = self.returnCell(cell_col, cell_row)
            
            if not self._sudoku.check_if_locked(cell_row, cell_col):
                self._sudoku.locked[cell_row][cell_col] = 0
                cell.setValue(self._sudoku.solution[cell_row][cell_col])
                cell.setStyleSheet("background-color: white; color: #1962ff;")
                cell.setReadOnly(True)
            
            self.hint_mode = False
            self.hint_number_button.setText(str(int(self.hint_number_button.text()) - 1))
        
        
    def makeGrid(self):
        central_widget = QGroupBox(self)
        central_widget.move(0, 46)
        # central_widget.setFixedSize(450, 450)
        # self.setCentralWidget(central_widget)
        self.cell_size = (45, 45)
        central_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        
        self.outer_grid_layout = QGridLayout()
        self.outer_grid_layout.setSpacing(0)
        # self.outer_grid_layout.addLayout(self.buttonGrid, 3, 3, alignment=Qt.AlignmentFlag.AlignBottom)

        

        central_widget.setLayout(self.outer_grid_layout)
        
        for i in range(3):
            for j in range(3):
                inner_group_box = QGroupBox(central_widget)
                inner_group_box.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                inner_group_box.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
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
                        
        central_widget.adjustSize()
                        
                        
    
    def checkBoard(self):
        if self._sudoku.check_if_solved():
            self.timer.stop()
            if self.account_data != None:
                if self.account_data[2][self.difficulty_index] == '00:00':
                    self.account_data[2][self.difficulty_index] = self.timer_label.text()
                else:
                    current_time = self.convert_time_to_seconds(self.account_data[2][self.difficulty_index])
                    new_time = self.convert_time_to_seconds(self.timer_label.text())
                    
                    if new_time < current_time:
                        self.account_data[2][self.difficulty_index] = self.timer_label.text()
                        self.game_completion_popup(True, None)
                    else:
                        self.game_completion_popup(False, None)
            else:
                self.game_completion_popup(False, False)
        else:
            print("Unsolved")

    
    def convert_time_to_seconds(self, timeToConvert):
        """_summary_

        Takes a time in the format "00:00" and converts it so time in seconds
        
        e.g turns "01:45" into 105
        """

        index = timeToConvert.find(":")
        minutes = int(timeToConvert[:index])
        seconds = int(timeToConvert[-2:])
        
        convertedTime = ((minutes * 60) + seconds)
        
        return convertedTime
        
    
    def game_completion_popup(self, new_best : bool, ask_login):
        if self.init_dialog != True:
            self.init_dialog = True
            update_score = None
            self.dialog = QDialog(self)
            self.dialog.setWindowTitle("Completion")
            
            self.dialog.setFixedSize(350, 300)
            
            self.main = QHBoxLayout(self.dialog)
            self.layout_names = QVBoxLayout(self.dialog)
            self.layout = QVBoxLayout(self.dialog)
            self.main.addLayout(self.layout_names)
            self.main.addLayout(self.layout)
            
            self.return_button = QPushButton("Return", self.dialog)
            self.return_button.clicked.connect(lambda: (self.currentWindow.setCurrentWidget(self.pages_dict["Main Menu"]), self.dialog.close()))
            
            self.play_again_button = QPushButton("Play Again", self.dialog)
            self.play_again_button.clicked.connect(lambda: (self.currentWindow.setCurrentWidget(self.pages_dict["Difficulty Menu"]), self.dialog.close()))
            
            self.layout_names.addWidget(self.return_button)
            self.layout.addWidget(self.play_again_button)
            
            self.congratulations_message = QLabel("Congratulations", self.dialog)
            self.congratulations_message2 = QLabel("Congratulations",self.dialog)
            self.layout.addWidget(self.congratulations_message)
            self.layout_names.addWidget(self.congratulations_message2)
            
            self.difficulty_title = QLabel("Difficulty")
            self.layout_names.addWidget(self.difficulty_title)
            self.difficulty_message = QLabel(f"{self.difficulty_label.text()}")
            self.difficulty_message.move(10, 10)
            self.layout.addWidget(self.difficulty_message)
            
            self.time_label = QLabel("Time", self.dialog)
            self.time_message = QLabel(self.timer_label.text(), self.dialog)
            self.time_message.move(0, 100)
            self.layout.addWidget(self.time_message)
            self.layout_names.addWidget(self.time_label)
            
        if self.account_data != None:
            
            self.pb = QLabel(self.account_data[2][self.difficulty_index], self.dialog)
        
        if ask_login != None:
            print("LOGIN!")
        
        if new_best:
            self.update_score()
            
        
        self.dialog.exec()
            
    
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

    
    def update_score(self):
        self.db.update_best_times(self.account_data[0], self.account_data[2])
        
        
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sudoku = Window(0, None, None, None)
    

    sudoku.show()
    
    sys.exit(app.exec())