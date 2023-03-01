from PyQt6.QtWidgets import QGroupBox, QMainWindow, QApplication, QGridLayout, QSpinBox, QSizePolicy, QPushButton, QLabel
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont
import sys

class Window(QMainWindow):
    def __init__(self, solvedBoard):
        super().__init__()
        
        self.setWindowTitle('Sudoku Grid')
        self.setGeometry(100, 100, 450, 450)
        self.solved_board = solvedBoard
        
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
    # Runs this function every time that the timer see's that 0.1 seconds has passes
    def update(self):
        if self.start_time is None:
            self.start_time = QDateTime.currentDateTime()
            
        elapsed = self.start_time.secsTo(QDateTime.currentDateTime())
        minutes = elapsed // 60
        seconds = elapsed % 60
        
        time_str = f"{minutes:02}:{seconds:02}"
        self.timer_label.setText(time_str)
        
        
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
                        cell.setObjectName(f"spinBox_{x}_{y}")
                        self.inner_group_box_layout.addWidget(cell, x, y)
                        
    def checkBoard(self):
        currentGrid = [[],[],[],[],[],[],[],[],[]]
        for row in range(9):
            for col in range(9):
                inner_row = row // 3
                inner_col = col //3
                inner_group_box = self.outer_grid_layout.itemAtPosition(inner_row, inner_col).widget()
                
                cell_row = row % 3
                cell_col = col % 3
                
                cell_name = f"spinBox_{cell_row}_{cell_col}"
                cell = inner_group_box.findChild(QSpinBox, cell_name)
                if cell is not None:
                    currentGrid[row].append(cell.value())
        print("Check Board")
        for i in range(9):
            print(*currentGrid[i])  
        if currentGrid == self.solved_board:
            print("SOLVED")
            self.timer.stop()
        else:
            print("NOT SOLVED")
        print("Checked Board")
                
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

    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sudoku = Window()
    sudoku.setCell(3, 1, 5)
    

    sudoku.show()
    
    sys.exit(app.exec())