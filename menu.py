from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QGroupBox, QStackedWidget
from PyQt6.QtCore import Qt, QCoreApplication
from PyQt6.QtGui import QFont
import newgui
import test_file
import sys


class SelectionMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Sudoku Application')
        self.setGeometry(100, 100, 450, 450)
        
        self.central_layout = QGroupBox(self)
        self.setCentralWidget(self.central_layout)
        
        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.playButton)
        
        self.account_button = QPushButton('Account', self)
        self.account_button.clicked.connect(self.accountButton)
        
        self.quit_button = QPushButton('Quit', self)
        self.quit_button.clicked.connect(QCoreApplication.instance().quit)
        
        self.button_grid = QGridLayout()
        self.button_grid.addWidget(self.play_button, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.button_grid.addWidget(self.account_button, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.button_grid.addWidget(self.quit_button, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.central_layout.setLayout(self.button_grid)
        
    def playButton(self):
        print("Play")
        self.changePage(game_page)
        
    def accountButton(self):
        print("Account")
        print("Switching Page")
        self.changePage(test_page)   
      
      
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
        self.changePage(testing_page)
    
    def changePage(self, pageToChangeTo):
        currentPage.setCurrentWidget(pageToChangeTo)
          
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    currentPage = QStackedWidget()
    
    game_page = newgui.Window(0.6)
    currentPage.addWidget(game_page)
    
    main_menu = SelectionMenu()
    currentPage.addWidget(main_menu)
    
    test_page = TestPage()
    currentPage.addWidget(test_page)
    
    testing_page = test_file.AccountLogin(currentPage, main_menu)
    currentPage.addWidget(testing_page)
    
    currentPage.setCurrentWidget(main_menu)
    currentPage.show()
    
    
    sys.exit(app.exec())