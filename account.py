from PyQt6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QGroupBox, QLineEdit, QLabel, QCheckBox, QApplication
import email_validator
import json
import sys



class AccountWindow(QMainWindow):
    def __init__(self, currentWindow, account_information, pages_dict):
        super().__init__()
        
        self.setFixedSize(618, 500)
        
        self.currentWindow = currentWindow
        self.logout = False
        self.pages_dict = pages_dict
        self.account_information = account_information
        self.best_times = None
        
        print(self.account_information)
        
        self.logout_button = QPushButton("Logout", self)
        self.logout_button.move(10, 450)
        self.logout_button.clicked.connect(self.logout_function)
        
    def logged_in(self):
        
        if self.account_information is not None:
            self.username_text = QLabel(self.account_information[1], self)
            self.best_times = self.account_information[2]
            
    def logout_function(self):
        self.logout = True
        self.currentWindow.setCurrentWidget(self.pages_dict["Main Menu"])
            
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    aw = AccountWindow(None, None, None)
    
    aw.show()
    sys.exit(app.exec())
    