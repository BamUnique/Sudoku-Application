from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QGroupBox, QStackedWidget, QComboBox

class DifficultySelection(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.choose_difficulty_selection = QComboBox(self)
        self.choose_difficulty_selection.addItems(["Easy", "Medium", "Hard", "Expert"])
        # self.choose_difficulty_selection.move()
        
        
