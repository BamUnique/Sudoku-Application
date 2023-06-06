from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QGroupBox, QStackedWidget, QComboBox, QFrame, QLabel
from PyQt6.QtGui import QFont, QTextFormat
from PyQt6.QtCore import Qt
import sys
from databasemanager import DatabaseManager

class DifficultySelection(QMainWindow):
    def __init__(self, currentWindow, pages_dict, account_information, game):
        super().__init__()
        
        self.show_best_times = False
        self.game = game
        self.login = False
        
        self.currentWindow = currentWindow
        self.pages_dict = pages_dict
        self.account_information = account_information
        if account_information is not None:
            self.load_times = self.account_information[3]
            self.show_best_times = True
            self.easy = self.load_times[0]
            self.medium = self.load_times[1]
            self.hard = self.load_times[2]
            self.expert = self.load_times[3]
            
    
        self.setFixedSize(618, 500)
        
        self.difficulty_dict = {"Easy": 0.5, "Medium": 0.6, "Hard": 0.7, "Expert": 0.8}
        self.difficulty_num = {"Easy": 0, "Medium": 1, "Hard": 2, "Expert": 3}
        
        self.button_posX = 109
        self.button_posY = 150 
        
        self.back_button = QPushButton('⬅', self)
        self.back_button.setFont(QFont('Arial', 20))
        self.back_button.setGeometry(10, 5, 35, 42)
        self.back_button.clicked.connect(self.back)
        
        
        self.easy_button = QPushButton("Easy", self)
        self.easy_button.setGeometry(self.button_posX, self.button_posY, 200, 40)
        self.easy_button.clicked.connect(lambda: self.choose_difficulty('Easy'))
        
        self.medium_button = QPushButton("Medium", self)
        self.medium_button.setGeometry(self.button_posX, self.button_posY+55, 200, 40)
        self.medium_button.clicked.connect(lambda: self.choose_difficulty('Medium'))
        
        self.hard_button = QPushButton("Hard", self)
        self.hard_button.setGeometry(self.button_posX, self.button_posY+110, 200, 40)
        self.hard_button.clicked.connect(lambda: self.choose_difficulty('Hard'))
        
        self.expert_button = QPushButton("Expert", self)
        self.expert_button.setGeometry(self.button_posX, self.button_posY+165, 200, 40)
        self.expert_button.clicked.connect(lambda: self.choose_difficulty('Expert'))
        
        self.choose_difficulty_label = QLabel("         Difficulty         ", self) # 9 Spaces on each side to center the text and add an underline effect.
        font = QFont()
        font.setPointSize(25)
        font.setUnderline(True)
        self.choose_difficulty_label.setFont(font)
        self.choose_difficulty_label.adjustSize()
        self.choose_difficulty_label.move(self.button_posX, self.button_posY-40)
        
        self.locked_box = QFrame(self)
        self.locked_box.setFrameShape(QFrame.Shape.Box)
        self.locked_box.setGeometry(self.button_posX + 225, self.button_posY, 100, 205)
        self.locked_box.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
        
        self.locked_text = QLabel("Sign in to access this feature", self)
        self.locked_text.setWordWrap(True)
        self.locked_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.locked_text.setGeometry(self.button_posX+225, self.button_posY+75, 100, 50)
        
        self.easy_best_time = QLabel("00:00", self)
        self.easy_best_time.move(self.button_posX+250, self.button_posY+5)
        self.easy_best_time.setFont(QFont("Arial", 20))
        
        self.medium_best_time = QLabel("00:00", self)
        self.medium_best_time.move(self.button_posX+250, self.button_posY+60)
        self.medium_best_time.setFont(QFont("Arial", 20))
        
        self.hard_best_time = QLabel("00:00", self)
        self.hard_best_time.move(self.button_posX+250, self.button_posY+115)
        self.hard_best_time.setFont(QFont("Arial", 20))
        
        self.expert_best_time = QLabel("00:00", self)
        self.expert_best_time .move(self.button_posX+250, self.button_posY+170)
        self.expert_best_time.setFont(QFont("Arial", 20))
        
        self.hide_best_times()

        
        
            
    def back(self):
        self.currentWindow.setCurrentWidget(self.pages_dict["Main Menu"])
        
    def update(self):
        if self.show_best_times:
            self.login = True
            self.load_times = self.account_information[2]
            self.easy = self.load_times[0]
            self.medium = self.load_times[1]
            self.hard = self.load_times[2]
            self.expert = self.load_times[3]
            
            self.show_best_times_function()
            
            self.easy_best_time.setText(self.easy)
            self.medium_best_time.setText(self.medium)
            self.hard_best_time.setText(self.hard)
            self.expert_best_time.setText(self.expert)
            
            self.locked_box.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
            self.locked_text.hide()
            
            
            
    def hide_best_times(self):
        self.easy_best_time.hide()
        self.medium_best_time.hide()
        self.hard_best_time.hide()
        self.expert_best_time.hide()
        
    def show_best_times_function(self):
        self.easy_best_time.show()
        self.medium_best_time.show()
        self.hard_best_time.show()
        self.expert_best_time.show()
            
    def choose_difficulty(self, difficulty):
        self.game.setup_board([self.difficulty_dict[difficulty], difficulty, self.difficulty_num[difficulty]])
        if self.login:
            self.game.personal_best_time.show()
            self.game.best_time_label.show()
            self.game.personal_best_time.setText(self.load_times[self.difficulty_num[difficulty]])
        else:
            self.game.personal_best_time.hide()
            self.game.best_time_label.hide()
        self.currentWindow.setCurrentWidget(self.pages_dict['Game Menu'])
        
if __name__ == '__main__':
    
    # app = menu.QApplication(sys.argv)
    # main_menu = menu.SelectionMenu()
    # main_menu.show()
    
    app = QApplication(sys.argv)
    
    
    window = DifficultySelection(None, None, None)
    window.show()
    
    sys.exit(app.exec())
