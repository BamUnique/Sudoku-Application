from PyQt6.QtWidgets import QGroupBox, QMainWindow, QApplication, QGridLayout, QSpinBox, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Sudoku Grid')
        self.setGeometry(100, 100, 450, 450)
        self.makeGrid()
        
        self.button = QPushButton('Check Solve', self)
        self.button.clicked.connect(self.checkBoard)
        
        buttonGrid = QGridLayout()
        buttonGrid.addWidget(self.button, 0, 0)

        
        
    def makeGrid(self):
        central_widget = QGroupBox(self)
        central_widget.setFixedSize(450, 450)
        self.setCentralWidget(central_widget)
        
        self.cell_size = (45, 45)
        
        self.outer_grid_layout = QGridLayout()
        self.outer_grid_layout.setSpacing(0)
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
        for row in range(9):
            for col in range(9):
                inner_row = row // 3
                inner_col = col //3
                inner_group_box = self.outer_grid_layout.itemAtPosition(inner_row, inner_col).widget()
                
                cell_row = row % 3
                cell_col = col % 3
                
                cell_name = f"spinBox_{cell_row}_{cell_col}"
        print("Check Board")
        
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