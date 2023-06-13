from PyQt6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QGroupBox, QLineEdit, QLabel, QCheckBox
from PyQt6.QtCore import Qt, QTimer, QDateTime
import email_validator
import json
import menu
from databasemanager import DatabaseManager


class LoginScreen(QMainWindow):
    def __init__(self, currentPage, pages_dict):
        super().__init__()
        
        self.error_text = ""
        self.db = DatabaseManager()
        self.loaded_account = None
        
        self.pages_dict = pages_dict
        
        self.x_position = 120
        self.y_position = 160
        
        self.currentPage = currentPage
        
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.go_back)
        
        # Generates the stuff for email entering
        self.email_label = QLabel("Email:", self)
        self.email_label.move(self.x_position + 25, self.y_position)
        self.email_box = QLineEdit(self)
        self.email_box.setGeometry(self.x_position+65, self.y_position, 250, 30)
        self.email_box.setTextMargins(7, 0, 0, 0)

        # Generates the stuff for password entering
        self.password_label = QLabel("Password:", self)
        self.password_label.move(self.x_position, self.y_position+40)
        self.password_box = QLineEdit(self)
        self.password_box.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_box.setGeometry(self.x_position+65, self.y_position+40, 250, 30)
        self.password_box.setTextMargins(7, 0, 0, 0)
        
        # Allows the user to see the password that they have entered
        self.show_password_option = QCheckBox(self)
        self.show_password_option.move(self.x_position+65, self.y_position+70)
        self.show_password_option.clicked.connect(self.checkIfShowPassword)
        self.show_password_label = QLabel("Show password", self)
        self.show_password_label.move(self.x_position+90, self.y_position+70)
        
        self.login_button = QPushButton("Login", self)
        self.login_button.setGeometry(self.x_position+(214), self.y_position+70, 100, 30)
        self.login_button.clicked.connect(self.attemptLogin)
        
        self.create_account = QLabel("Create account", self)
        self.create_account.move(self.x_position+65, self.y_position+100)
        self.create_account.setStyleSheet("color: #4e85de;")
        self.create_account.mousePressEvent = self.createAccountClicked
        
        self.error_message = QLabel(self.error_text, self)
        self.error_message.move(self.x_position+65, self.y_position+150)
        self.error_message.setStyleSheet("color: #fa143e;")
        
        self.message_timer = QTimer(self)
        self.message_timer.setInterval(3500)
        self.message_timer.timeout.connect(self.hide_error_message)
        
    def hide_error_message(self):
        self.error_message.hide()
        self.message_timer.stop()
        
    def createAccountClicked(self, event):
        self.currentPage.setCurrentWidget(self.pages_dict["Create Account Menu"])
    
    def checkIfShowPassword(self):
        if self.show_password_option.isChecked():
            self.password_box.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_box.setEchoMode(QLineEdit.EchoMode.Password)
    
    def go_back(self):
        self.currentPage.setCurrentWidget(self.pages_dict["Main Menu"])
        
    def attemptLogin(self):
        throw_error = False
        
        email = self.email_box.text()
        password = self.password_box.text()
        invalid_email = self.db.validate_email(email)
        
        if invalid_email:
            throw_error = True
        else:
            exists = self.db.unique_account(email)
            if exists:
                account_information = self.db.validate_password(email, password)
                if account_information is not None: # Runs if the email entered is valid and login is successful.
                    self.reset()
                    self.loaded_account = account_information
                    self.loaded_account.append(self.db.return_best_times(self.loaded_account[0]))
                    self.currentPage.setCurrentWidget(self.pages_dict["Main Menu"])
                else:
                    throw_error = True
            else:
                throw_error = True
                
        if throw_error:
            self.error_message.setText("Incorrect email or password")
            self.error_message.adjustSize()
            self.message_timer.start()
            
    def reset(self):
        self.email_box.clear()
        self.password_box.clear()

class CreateNewAccount(QMainWindow):
    def __init__(self, currentWindow, pages_dict):
        super().__init__()
        
        self.db = DatabaseManager()
        
        self.x_position = 120
        self.y_position = 160
        
        self.error_text = ""
        
        self.currentWindow = currentWindow
        self.pages_dict = pages_dict
        
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.go_back)
        
        # Generates the stuff for username entering
        self.username_label = QLabel("Username", self)
        self.username_label.move(self.x_position, self.y_position-40)
        self.username_box = QLineEdit(self)
        self.username_box.setGeometry(self.x_position+65, self.y_position-40, 250, 30)
        self.username_box.setMaxLength(30)
        self.username_box.setTextMargins(7, 0, 0, 0)
        
        
        # Generates the stuff for email entering
        self.email_label = QLabel("Email:", self)
        self.email_label.move(self.x_position + 25, self.y_position)
        self.email_box = QLineEdit(self)
        self.email_box.setGeometry(self.x_position+65, self.y_position, 250, 30)
        self.email_box.setTextMargins(7, 0, 0, 0)

        # Generates the stuff for password entering
        self.password_label = QLabel("Password:", self)
        self.password_label.move(self.x_position, self.y_position+40)
        self.password_box = QLineEdit(self)
        self.password_box.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_box.setGeometry(self.x_position+65, self.y_position+40, 250, 30)
        self.password_box.setTextMargins(7, 0, 0, 0)
        
        # Allows the user to see the password that they have entered
        self.show_password_option = QCheckBox(self)
        self.show_password_option.move(self.x_position+65, self.y_position+70)
        self.show_password_option.clicked.connect(self.checkIfShowPassword)
        self.show_password_label = QLabel("Show password", self)
        self.show_password_label.move(self.x_position+90, self.y_position+70)
        
        self.create_account_button = QPushButton("Create Account", self)
        self.create_account_button.setGeometry(self.x_position+(204), self.y_position+70, 110, 30)
        self.create_account_button.clicked.connect(self.checkIfExisting)
        
        self.error_message = QLabel(self.error_text, self)
        self.error_message.move(self.x_position+65, self.y_position+150)
        self.error_message.setStyleSheet("color: #fa143e;")
        
        self.message_timer = QTimer(self)
        self.message_timer.setInterval(3500)
        self.message_timer.timeout.connect(self.hide_error_message)
        
    def hide_error_message(self):
        self.error_message.hide()
        self.message_timer.stop()
        
        
    def go_back(self):
        self.currentWindow.setCurrentWidget(self.pages_dict["Main Menu"])
    
    def checkIfShowPassword(self):
        if self.show_password_option.isChecked():
            self.password_box.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_box.setEchoMode(QLineEdit.EchoMode.Password)
    
    def checkIfExisting(self):
        """_summary_\n
        Runs if the user is creating a new account and have clicked the create account button.
        """
        self.return_error = False
        if not self.return_error:
            self.password_box.setReadOnly(True)
            self.username_box.setReadOnly(True)
            self.email_box.setReadOnly(True)
        
        existing = self.db.unique_account(self.email_box.text())
        
        if not existing:
            print("Inputting Credentials")
            inputted = self.db.input_credentials(self.username_box.text(), self.email_box.text(), self.password_box.text())
            if not inputted:
                self.error_message.setText("Invalid email address")
                self.error_message.adjustSize()
                self.return_error = True
        else:
            self.return_error = True
            self.error_message.setText("Email already in use")
            self.error_message.adjustSize()
    
        if self.return_error:
            self.password_box.setReadOnly(False)
            self.username_box.setReadOnly(False)
            self.email_box.setReadOnly(False)
            self.message_timer.start()
        else:
            self.currentWindow.setCurrentWidget(self.pages_dict["Main Menu"])
            
            
    def error_message_update(self, message):
        self.error_message.setText(message)
        self.error_message.adjustSize()
