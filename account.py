from PyQt6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QGroupBox, QLineEdit, QLabel, QCheckBox
import email_validator
import json



class AccountWindow(QMainWindow):
    def __init__(self, currentWindow, account_information, pages_dict):
        super().__init__()
        
        self.currentWindow = currentWindow
        self.pages_dict = pages_dict
        self.account_information = account_information
        
        print(self.account_information)
        
    def logged_in(self):
        
        if self.account_information is not None:
            self.username_text = QLabel(self.account_information[1], self)