from PyQt6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QGroupBox, QLineEdit, QLabel, QCheckBox, QApplication, QLineEdit
from PyQt6.QtCore import QPoint, QRect, QTimer
from PyQt6.QtGui import QFont
import email_validator
import json
import sys
import databasemanager



class AccountWindow(QMainWindow):
    def __init__(self, currentWindow, account_information, pages_dict):
        super().__init__()
        
        self.setFixedSize(618, 500)
        
        self.db = databasemanager.DatabaseManager()
        
        self.currentWindow = currentWindow
        self.logout = False
        self.pages_dict = pages_dict
        self.account_information = account_information
        self.best_times = None
        
        self.back_button = QPushButton('⬅', self)
        self.back_button.setFont(QFont('Arial', 20))
        self.back_button.setGeometry(10, 5, 35, 42)
        self.back_button.clicked.connect(lambda: self.currentWindow.setCurrentWidget(self.pages_dict["Main Menu"]))
        
        self.logout_button = QPushButton("Logout", self)
        self.logout_button.move(10, 450)
        self.logout_button.clicked.connect(self.logout_function)
        
        self.logged_in_bool = False
        

        
    def logged_in(self):
        
        if self.account_information is not None and self.logged_in_bool is False:
            self.logged_in_bool = True
            self.pos_x = 100
            self.pos_y = 107
            
            self.username_label = QLabel("Username:", self)
            self.username_label.move(self.pos_x, self.pos_y)
            self.username_label.adjustSize()
            
            self.timer = QTimer()
            self.timer.setInterval(1000)
            self.timer.timeout.connect(self.check_if_matching)
            
            self.error_text = QLabel("Passwords do not match", self)
            self.error_text.setStyleSheet("color: red;")
            self.error_text.adjustSize()
            self.error_text.move(self.pos_x+75, self.pos_y + 130)
            self.error_text.hide()
            
            self.username_box = QLineEdit(self)
            self.username_box.setMaxLength(30)
            self.username_box.setText(self.account_information[1])
            self.username_box.setTextMargins(7, 0, 0, 0)
            self.username_box.setReadOnly(True)
            self.username_box.setGeometry(self.pos_x+75, self.pos_y-7, 250, 30)
            
            self.password_label = QLabel("Password:", self)
            self.password_label.move(self.pos_x+3, self.pos_y+33)
            self.password_label.adjustSize()
            
            self.password_box = QLineEdit(self)
            self.password_box.setText("placeholderpassword")
            self.password_box.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_box.setGeometry(self.pos_x+75, self.pos_y+26, 250, 30)
            self.password_box.setReadOnly(True)
            
            self.new_password_label = QLabel("New Password:", self)
            self.new_password_label.move(self.pos_x-27, self.pos_y+66)
            self.new_password_label.adjustSize()
            self.new_password_label.hide()
            
            self.new_password_box = QLineEdit(self)
            self.new_password_box.hide()
            self.new_password_box.setEchoMode(QLineEdit.EchoMode.Password)
            self.new_password_box.setGeometry(self.pos_x+75, self.pos_y+59, 250, 30)
            
            self.password_box.textEdited.connect(lambda: print(self.password_box.text()))
            
            self.confirm_password_label = QLabel("Confirm Password:", self)
            self.confirm_password_label.move(self.pos_x-48, self.pos_y+99)
            self.confirm_password_label.adjustSize()
            self.confirm_password_label.hide()
            
            self.confirm_new_password_box = QLineEdit(self)
            self.confirm_new_password_box.hide()
            self.confirm_new_password_box.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_new_password_box.setGeometry(self.pos_x+75, self.pos_y+92, 250, 30)
            
            self.confirm_new_password_box.textEdited.connect(lambda: self.timer.start())
            
            self.change_password = QPushButton("Edit", self)
            self.change_password.clicked.connect(self.change_password_function)
            self.change_password.move(self.pos_x+330, self.pos_y+26)
            
            
            self.change_username = QPushButton("Edit", self)
            self.change_username.clicked.connect(self.change_username_function)
            self.change_username.move(self.pos_x+330, self.pos_y-7)
            
            self.best_times = self.account_information[2]
            
    def logout_function(self):
        self.logout = True
        self.currentWindow.setCurrentWidget(self.pages_dict["Main Menu"])
        
    def change_username_function(self):
        """_summary_
        
        Allows the user to edit their username.
        """
        if self.change_username.text() == "Confirm":
            self.change_username.setText("Edit")
            self.username_box.setReadOnly(True)
            if self.username_box.text().isspace() or len(self.username_box.text()) == 0:
                self.username_box.setText(self.account_information[1])
            else:
                self.username_box.setText(self.username_box.text().strip())
                
            if self.username_box.text().strip() != self.account_information[1]:
                self.account_information[1] = self.username_box.text().strip()
                self.db.update_username(self.account_information[0], self.account_information[1])
            
        else:
            self.change_username.setText("Confirm")
            self.username_box.clear()
            self.username_box.setReadOnly(False)
            
            
    def change_password_function(self):
        if self.change_password.text() == "Confirm":
            response = self.db.check_password(self.account_information[0], self.password_box.text())
            if response:
                self.db.update_password(self.account_information[0], self.new_password_box.text())
                self.change_password.setText("Edit")
                self.password_box.setText("placeholderpassword")
                self.password_box.setReadOnly(True)
                
                self.new_password_box.hide()
                self.confirm_new_password_box.hide()
                self.new_password_label.hide()
                self.confirm_password_label.hide()
            else:
                self.error_text.show()
                self.error_text.setText("Incorrect Password")
                
        else:
            self.change_password.setText("Confirm")
            self.password_box.clear()
            self.new_password_box.clear()
            self.confirm_new_password_box.clear()
            
            self.password_box.setReadOnly(False)
            
            self.new_password_box.show()
            self.confirm_new_password_box.show()
            self.new_password_label.show()
            self.confirm_password_label.show()
            

            
    def check_if_matching(self):
        if self.new_password_box.text() != self.confirm_new_password_box.text():
            self.error_text.setText("Password is not matching")
            self.error_text.show()
        else:
            self.error_text.hide()
        
        
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    aw = AccountWindow(None, [1, "testUsername", ["00:00", "00:00", "00:00", "00:00"]], None)
    aw.logged_in()
    
    aw.show()
    sys.exit(app.exec())
    