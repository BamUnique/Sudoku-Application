from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QGroupBox, QStackedWidget, QComboBox

class DifficultySelection(QMainWindow):
    def __init__(self):
        super().__init__()
        
        
        self.difficulty_dict = {"Easy": 0.5, "Medium": 0.6, "Hard": 0.7, "Expert": 0.8}
        self.choose_difficulty_selection = QComboBox(self)
        self.choose_difficulty_selection.addItems(["Easy", "Medium", "Hard", "Expert"])
        # self.choose_difficulty_selection.move()
        
        
