from PyQt6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QGroupBox, QLineEdit, QLabel, QCheckBox, QApplication, QLineEdit
from PyQt6.QtCore import QPoint, QRect
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
        
        self.logout_button = QPushButton("Logout", self)
        self.logout_button.move(10, 450)
        self.logout_button.clicked.connect(self.logout_function)
        

        
    def logged_in(self):
        
        if self.account_information is not None:
            self.pos_x = 100
            self.pos_y = 107
            
            self.username_label = QLabel("Username:", self)
            self.username_label.move(self.pos_x, self.pos_y)
            self.username_label.adjustSize()
            print(self.username_label.size())
            
            self.username_box = QLineEdit(self)
            self.username_box.setMaxLength(30)
            self.username_box.setText(self.account_information[1])
            self.username_box.setTextMargins(7, 0, 0, 0)
            self.username_box.setReadOnly(True)
            self.username_box.setGeometry(self.pos_x+75, self.pos_y-7, 250, 30)
            
            self.change_username = QPushButton("Edit", self)
            self.change_username.clicked.connect(self.change_username_function)
            
            self.best_times = self.account_information[2]
            
    def logout_function(self):
        self.logout = True
        self.currentWindow.setCurrentWidget(self.pages_dict["Main Menu"])
        
    def change_username_function(self):
        if self.change_username.text() == "Confirm":
            self.change_username.setText("Edit")
            self.username_box.setReadOnly(True)
        else:
            self.change_username.setText("Confirm")
            self.username_box.clear()
            self.username_box.setReadOnly(False)
            
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    aw = AccountWindow(None, [1, "testUsername", ["00:00", "00:00", "00:00", "00:00"]], None)
    aw.logged_in()
    
    aw.show()
    sys.exit(app.exec())
    