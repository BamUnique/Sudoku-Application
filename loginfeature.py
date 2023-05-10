from PyQt6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QGroupBox, QLineEdit, QLabel, QCheckBox
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
        self.login_button.clicked.connect(self.attemptLogin)
        
        self.create_account = QLabel("Create account", self)
        self.create_account.move(self.x_position+65, self.y_position+100)
        self.create_account.setStyleSheet("color: #4e85de;")
        self.create_account.mousePressEvent = self.createAccountClicked
        
        self.error_message = QLabel(self.error_text, self)
        self.error_message.move(self.x_position+65, self.y_position+150)
        self.error_message.setStyleSheet("color: #fa143e;")
        
    def createAccountClicked(self, event):
        self.currentPage.setCurrentWidget(self.newAccountPage)
    
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
                if account_information is not None:
                    self.loaded_account = account_information
                    print(self.loaded_account)
                    self.loaded_account.append(self.db.return_best_times(self.loaded_account[0]))
                    self.currentPage.setCurrentWidget(self.pages_dict["Main Menu"])
                else:
                    throw_error = True
            else:
                throw_error = True
                
        if throw_error:
            self.error_message.setText("Incorrect email or password")
            self.error_message.adjustSize()
            
            
            
                
    
    def matchPassword(self):
        self.return_error = False
        
        f = open('test_account.json')
        data = json.load(f)
        
        email = self.email_box.text()
        
        emails = [account['email'] for account in data['accounts']]
        try:
            index = emails.index(email)
            if self.password_box.text() != data['accounts'][index]['password']:
                self.return_error = True
                self.error_text = "Incorrect email or password"
        except ValueError:
            self.return_error = True
            self.error_text = "Incorrect email or password"
            
        if not self.return_error:
            self.loaded_account = (data['accounts'][index])
            # print(self.loaded_account)
            self.currentPage.setCurrentWidget(self.menu)

        else:
            self.error_message.setText(self.error_text)
            self.error_message.adjustSize()
            
    def getAccountInformation(self):
        pass
            

class CreateNewAccount(QMainWindow):
    def __init__(self, currentPage):
        super().__init__()
        
        self.x_position = 120
        self.y_position = 160
        
        self.currentPage = currentPage
        self.menu = menu
        
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.go_back)
        
        # Generates the stuff for username entering
        self.username_label = QLabel("Username", self)
        self.username_label.move(self.x_position, self.y_position-40)
        self.username_box = QLineEdit(self)
        self.username_box.setGeometry(self.x_position+65, self.y_position-40, 250, 30)
        
        
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
        
        self.create_account_button = QPushButton("Create Account", self)
        self.create_account_button.setGeometry(self.x_position+(204), self.y_position+70, 110, 30)
        self.create_account_button.clicked.connect(self.checkIfExisting)
        
        
    def go_back(self):
        self.currentPage.setCurrentWidget(self.menu)
    
    def checkIfShowPassword(self):
        if self.show_password_option.isChecked():
            self.password_box.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_box.setEchoMode(QLineEdit.EchoMode.Password)
    
    def checkIfExisting(self):
        self.return_error = False
        if not self.return_error:
            self.password_box.setReadOnly(True)
            self.username_box.setReadOnly(True)
            self.email_box.setReadOnly(True)
        
        f = open('test_account.json')
        data = json.load(f)
        
        email = self.email_box.text()
        
        emails = [account['email'] for account in data['accounts']]
        try:
            index = emails.index(email)
            self.return_error = True
            # Return error as email is already in use
        except ValueError:
            self.return_error = False
            
        if not self.return_error:
            username = self.username_box.text()
            usernames = [account['username'] for account in data['accounts']]
            try:
                index = usernames.index(username)
                self.return_error = True
                # Return Error as username is already taken
            except ValueError:
                self.return_error = False
                
        if not self.return_error:
            
            new_account_data = {
                "email": self.email_box.text(),
                "username": self.username_box.text(),
                "password": self.password_box.text(),
                "scores": {
                        "easy"  : "none",
                        "medium": "none",
                        "hard"  : "none",
                        "expert": "none"
                    }
            }
            
            with open('test_account.json', 'r') as f:
                data = json.load(f)
                
            data['accounts'].append(new_account_data)

            with open('test_account.json', 'w') as f:
                json.dump(data, f, indent=4)
                
            print("Here")
            self.loadAccountData()
    
        if self.return_error:
            self.password_box.setReadOnly(False)
            self.username_box.setReadOnly(False)
            self.email_box.setReadOnly(False)
            
    def loadAccountData(self):
        f = open('test_account.json')
        data = json.load(f)
        
        username = self.username_box.text()
        
        usernames = [account['username'] for account in data['accounts']]
        
        try:
            index = usernames.index(username)
            print(data['accounts'][index])
            self.account_information = data['accounts'][index]
        except ValueError:
            pass
            