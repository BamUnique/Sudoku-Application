from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QGroupBox, QStackedWidget, QComboBox, QFrame, QLabel
from PyQt6.QtGui import QFont, QTextFormat
from PyQt6.QtCore import Qt
import sys

class DifficultySelection(QMainWindow):
    def __init__(self):
        super().__init__()
    
        self.setFixedSize(618, 500)
        self.show_best_times = True
        
        self.difficulty_dict = {"Easy": 0.5, "Medium": 0.6, "Hard": 0.7, "Expert": 0.8}
        
        button_posX = 109
        button_posY = 150
        
        self.easy_button = QPushButton("Easy", self)
        self.easy_button.setGeometry(button_posX, button_posY, 200, 40)
        self.easy_button.clicked.connect(self.easyDifficulty)
        
        self.medium_button = QPushButton("Medium", self)
        self.medium_button.setGeometry(button_posX, button_posY+55, 200, 40)
        self.medium_button.clicked.connect(self.mediumDifficulty)
        
        self.hard_button = QPushButton("Hard", self)
        self.hard_button.setGeometry(button_posX, button_posY+110, 200, 40)
        self.hard_button.clicked.connect(self.hardDifficulty)
        
        self.expert_button = QPushButton("Expert", self)
        self.expert_button.setGeometry(button_posX, button_posY+165, 200, 40)
        self.expert_button.clicked.connect(self.expertDifficulty)
        
        self.locked_box = QFrame(self)
        self.locked_box.setFrameShape(QFrame.Shape.Box)
        self.locked_box.setGeometry(button_posX + 225, button_posY, 100, 205)
        self.locked_box.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
        
        self.locked_text = QLabel("Sign in to access this feature", self)
        self.locked_text.setWordWrap(True)
        self.locked_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.locked_text.setGeometry(button_posX+225, button_posY+75, 100, 50)

        
        if self.show_best_times:
            self.easy_best_time = QLabel("00:00", self)
            self.easy_best_time.move(button_posX+250, button_posY+5)
            self.easy_best_time.setFont(QFont("Arial", 20))
            
            self.medium_best_time = QLabel("00:00", self)
            self.medium_best_time.move(button_posX+250, button_posY+60)
            self.medium_best_time.setFont(QFont("Arial", 20))
            
            self.hard_best_time = QLabel("00:00", self)
            self.hard_best_time.move(button_posX+250, button_posY+115)
            self.hard_best_time.setFont(QFont("Arial", 20))
            
            self.expert_best_time = QLabel("00:00", self)
            self.expert_best_time .move(button_posX+250, button_posY+170)
            self.expert_best_time.setFont(QFont("Arial", 20))
            
            self.locked_box.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
            self.locked_text.hide()
            
            
        
    def update(self):
        pass
        
    def easyDifficulty(self):
        print(f"Difficulty Easy chosen with a value of {self.difficulty_dict['Easy']}")
    
    def mediumDifficulty(self):
        print(f"Difficulty Medium chosen with a value of {self.difficulty_dict['Medium']}")
    
    def hardDifficulty(self):
        print(f"Difficulty Hard chosen with a value of {self.difficulty_dict['Hard']}")
    
    def expertDifficulty(self):
        print(f"Difficulty Expert chosen with a value of {self.difficulty_dict['Expert']}")
        
        
if __name__ == '__main__':
    
    # app = menu.QApplication(sys.argv)
    # main_menu = menu.SelectionMenu()
    # main_menu.show()
    
    app = QApplication(sys.argv)
    
    
    window = DifficultySelection()
    window.show()
    
    sys.exit(app.exec())
