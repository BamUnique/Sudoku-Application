from PyQt6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QGroupBox, QLineEdit, QLabel, QCheckBox
import email_validator
import json


class LoginScreen(QMainWindow):
    def __init__(self, currentPage, menu):
        super().__init__()
        
        self.x_position = 120
        self.y_position = 160
        
        self.central_layout = QGroupBox()
        
        self.currentPage = currentPage
        self.menu = menu
        
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.go_back)
        
        # Generates the stuff for email entering
        self.email_label = QLabel("Email:", self)
        self.email_label.move(self.x_position + 25, self.y_position)
        self.email_box = QLineEdit(self)
        self.email_box.setGeometry(self.x_position+65, self.y_position, 250, 30)

        # Generates the stuff for password entering
        self.password_label = QLabel("Password:", self)
        self.password_label.move(self.x_position, self.y_position+40)
        self.password_box = QLineEdit(self)
        self.password_box.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_box.setGeometry(self.x_position+65, self.y_position+40, 250, 30)
        
        # Allows the user to see the password that they have entered
        self.show_password_option = QCheckBox(self)
        self.show_password_option.move(self.x_position+65, self.y_position+70)
        self.show_password_option.clicked.connect(self.checkIfShowPassword)
        self.show_password_label = QLabel("Show password", self)
        self.show_password_label.move(self.x_position+90, self.y_position+70)
        
        self.login_button = QPushButton("Login", self)
        self.login_button.setGeometry(self.x_position+(214), self.y_position+70, 100, 30)
        self.login_button.clicked.connect(self.matchPassword)
        
    def checkIfShowPassword(self):
        if self.show_password_option.isChecked():
            self.password_box.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_box.setEchoMode(QLineEdit.EchoMode.Password)
    
    def go_back(self):
        self.currentPage.setCurrentWidget(self.menu)
        

    def matchPassword(self):
        self.return_error = False
        
        f = open('test_account.json')
        data = json.load(f)
        
        email = self.email_box.text()
        
        emails = [account['email'] for account in data['accounts']]
        try:
            index = emails.index(email)
            print(index)
            if self.password_box.text() == data['accounts'][index]['password']:
                print("True")
            else: 
                self.return_error = True
        except ValueError:
            self.return_error = True
            
        if not self.return_error:
            self.loaded_account = (data['accounts'][index])
            print(self.loaded_account)
        
        
class CreateNewAccount(QMainWindow):
    def __init__(self, currentPage):
        super().__init__()
        
        
        self.email_label = QLabel("Email:", self)
        self.email_label.move(50, 70)
        self.email_box = QLineEdit(self)
        
        