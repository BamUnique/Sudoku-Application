import sys
from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QGroupBox, QStackedWidget, QLabel, QFrame
from PyQt6.QtCore import Qt, QCoreApplication, QRect
from PyQt6.QtGui import QFont

import sudokuboard
import loginfeature
import difficulty_selection
import settings
import account


class SelectionMenu(QMainWindow):
    
    pages_dict = {
        "Main Menu": None,
        "Settings Menu": None,
        "Account Menu": None,
        "Account Window": None,
        "Create Account Menu": None,
        "Difficulty Menu": None,
        "Game Menu": None
    }
    
    def __init__(self, currentWindow):
        super().__init__()
        
        self.loggedIn = False
        self.account_information = None
        
        self.currentWindow = currentWindow

        self.setWindowTitle('Sudoku Application')
        self.setGeometry(0, 0, 618, 500)
        self.setFixedSize(618, 500)
        
        self.central_layout = QGroupBox(self)
        self.setCentralWidget(self.central_layout)
        
        # self.setStyleSheet("background-color: white;")
        
        button_width = 200
        button_height = 40
        button_spot = -10
        
        self.username = "Guest"
        
        self.font = QFont()
        self.font.setFamily("Arial")
        self.font.setPixelSize(30)
        
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
        
        self.username_text = QLabel("", self)
        self.username_text.adjustSize()
        self.username_text.move((618-self.username_text.width())-10, 10)
        
        self.username_box = QFrame(self)
        self.username_box.setFrameShape(QFrame.Shape.Box)
        self.username_box.setGeometry(578, 10, 30, 30)
        
        self.settings_button = QPushButton('⚙', self)
        self.settings_button.setFont(QFont('Arial', 35))
        self.settings_button.clicked.connect(self.settingsButton)
        self.settings_button.setGeometry(10, 5, 35, 42)
        
        self.currentWindow.currentChanged.connect(self.updateStuff)
        
        self.central_layout.setLayout(self.button_grid)
        
        self.init_pages()
        
    
    def init_pages(self):
        
        self.pages_dict["Main Menu"] = self
        self.pages_dict["Settings Menu"] = settings.SettingsScreen(self.currentWindow, self.pages_dict)
        self.lf = loginfeature.LoginScreen(self.currentWindow, self.pages_dict)
        self.pages_dict["Account Menu"] = self.lf
        self.acc = account.AccountWindow(self.currentWindow, self.account_information, self.pages_dict)
        self.pages_dict["Account Window"] = self.acc
        self.game = sudokuboard.Window(0, None, self.currentWindow, self.pages_dict)
        self.pages_dict["Game Menu"] = self.game
        self.pages_dict["Create Account Menu"] = loginfeature.CreateNewAccount(self.currentWindow, self.pages_dict)
        self.diff = difficulty_selection.DifficultySelection(self.currentWindow, self.pages_dict, self.account_information, self.game)
        self.pages_dict["Difficulty Menu"] = self.diff
            
        for key in self.pages_dict:
            if self.pages_dict[key] != None:
                self.currentWindow.addWidget(self.pages_dict[key])
                
        self.currentWindow.setCurrentWidget(self.pages_dict["Main Menu"])
        self.currentWindow.setFixedSize(618, 500)
        self.currentWindow.show()
        
    def playButton(self):
        self.changePage("Difficulty Menu")
        
    def accountButton(self):
        if self.loggedIn:
            self.changePage("Account Window")
        else:   
            self.changePage("Account Menu")
        
    def settingsButton(self):
        self.changePage("Settings Menu")
        
    def updateStuff(self):
        """_summary_
        
        Updates everything that needs to be changes regularily and needs to be checked.\n
        This function is run whenever the window changes.
        """
        # print("Updating Information")
        self.account_information = self.lf.loaded_account

        # Updates everything that needs to be updated when the user is logged in. Refreshes whenever the user changes a screen
        if self.account_information is not None:
            self.loggedIn = True
            self.username = self.account_information[1]
            self.id = self.account_information[0]
            
            self.acc.account_information = self.account_information
            self.acc.logged_in()
        
            self.update_username_box(self.username)
            
            self.diff.show_best_times = True
            self.diff.account_information = self.account_information
            self.diff.update()
            
            self.game.account_data = self.account_information
            self.game.logged_in = True      
            
            # Runs if the user clicks on the logout button in account.py
            if self.acc.logout is True:
                self.acc.logout = False
                self.loggedIn = False
                self.account_information = None
                self.username = None
                self.id = None
                
                self.diff.locked_box.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
                self.diff.locked_text.show()
                self.diff.login = False
                self.diff.show_best_times = False
                self.diff.account_information = None
                self.diff.hide_best_times()
                
                self.lf.loaded_account = None
                
                self.game.account_data = None
                self.game.logged_in = False  
                
                self.update_username_box("")
                
                
    def changePage(self, pageToChangeTo):
        """_summary_
        
        Changes the page to whatever the given page is.
        
        Args:
            pageToChangeTo (_type_): str variable e.g. "Main Menu" is a key in the self.pages_dict
        """
        self.currentWindow.setCurrentWidget(self.pages_dict[pageToChangeTo])
      
    def update_username_box(self, username):
        """_summary_
        
        Adjusts the sizes of the username, and userame boxe found at the top right of the main menu screen. 
        """
        self.username_text.setText(username)
        self.username_text.adjustSize()
        self.username_text.move((618-self.username_text.width())-20, 16)
        if username == "":
            self.username_box.setGeometry(578, 10, 30, 30)
        else:
            self.username_box.setGeometry((588-self.username_text.width()), 10, (20 + self.username_text.width()), 30)
        
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
        self.changePage(None)    
        
    def across_button(self):
        self.changePage(None)
    
    def changePage(self, pageToChangeTo):
        currentWindow.setCurrentWidget(pageToChangeTo)
          
        
if __name__ == '__main__':
    
    
    app = QApplication(sys.argv)
    currentWindow = QStackedWidget()
    
    menu = SelectionMenu(currentWindow)
    
    menu.show()
    
    sys.exit(app.exec())