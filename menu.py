import sys
from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QGroupBox, QStackedWidget
from PyQt6.QtCore import Qt, QCoreApplication, QRect
from PyQt6.QtGui import QFont

import newgui
import loginfeature
import difficulty_selection


class SelectionMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Sudoku Application')
        self.setGeometry(0, 0, 450, 450)
        
        self.central_layout = QGroupBox(self)
        self.setCentralWidget(self.central_layout)
        
        button_width = 200
        button_height = 40
        button_spot = -10
        
        self.x_pos = int((618 - button_width) / 2)
        self.y_pos = int((self.frameGeometry().height() - button_height) / 2)
        
        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.playButton)
        self.play_button.setGeometry(QRect(self.x_pos, self.y_pos-(button_spot), button_width, button_height))
        
        self.account_button = QPushButton('Account', self)
        self.account_button.clicked.connect(self.accountButton)
        self.account_button.setGeometry(QRect(self.x_pos, self.y_pos-(button_spot-35), button_width, button_height))
        
        self.quit_button = QPushButton('Quit', self)
        self.quit_button.clicked.connect(QCoreApplication.instance().quit)
        self.quit_button.setGeometry(QRect(self.x_pos, self.y_pos-(button_spot-70), button_width, button_height))
        
        self.button_grid = QGridLayout()
        # self.button_grid.addWidget(self.play_button, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        # self.button_grid.addWidget(self.account_button, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        # self.button_grid.addWidget(self.quit_button, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.central_layout.setLayout(self.button_grid)
        
    def playButton(self):
        print("Play")
        self.changePage(game_page)
        # self.changePage(difficulty_page)
        
    def accountButton(self):
        print("Account")
        print("Switching Page")
        self.changePage(account_page)   
      
      
    def changePage(self, pageToChangeTo):
        currentPage.setCurrentWidget(pageToChangeTo)
      
class TestPage(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.buttonGrid = QGridLayout()
        
        self.backButton = QPushButton("Back", self)
        self.backButton.clicked.connect(self.back_button)
        self.buttonGrid.addWidget(self.backButton, 0, 0)
        
        self.new_button = QPushButton("Across", self)
        self.new_button.clicked.connect(self.across_button)
        self.buttonGrid.addWidget(self.new_button, 0, 1)
        self.buttonGrid.setSpacing(10)
        
    def back_button(self):
        self.changePage(main_menu)    
        
    def across_button(self):
        self.changePage(account_page)
    
    def changePage(self, pageToChangeTo):
        currentPage.setCurrentWidget(pageToChangeTo)
          
        
if __name__ == '__main__':
    
    
    app = QApplication(sys.argv)
    currentPage = QStackedWidget()
    
    difficulty_page = difficulty_selection.DifficultySelection()
    currentPage.addWidget(difficulty_page)
    
    game_page = newgui.Window(0.6)
    currentPage.addWidget(game_page)
    
    main_menu = SelectionMenu()
    currentPage.addWidget(main_menu)
    
    test_page = TestPage()
    currentPage.addWidget(test_page)
    
    new_account_page = loginfeature.CreateNewAccount(currentPage, main_menu)
    currentPage.addWidget(new_account_page)
    
    account_page = loginfeature.LoginScreen(currentPage, main_menu, new_account_page)
    currentPage.addWidget(account_page)
    
    currentPage.setCurrentWidget(main_menu)
    currentPage.show()
    
    
    sys.exit(app.exec())