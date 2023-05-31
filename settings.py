import sys
from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QGroupBox, QStackedWidget, QLabel
from PyQt6.QtCore import Qt, QCoreApplication, QRect
from PyQt6.QtGui import QFont



class SettingsScreen(QMainWindow):
    
    def __init__(self, currentWindow, pages_dict):
        super().__init__()
        self.setWindowTitle("Settings Screen")
        self.setGeometry(0, 0, 618, 500)
        
        self.currentWindow = currentWindow
        self.pages_dict = pages_dict
        
        self.back_button = QPushButton('⬅', self)
        self.back_button.setFont(QFont('Arial', 20))
        self.back_button.setGeometry(10, 5, 35, 42)
        self.back_button.clicked.connect(lambda: self.currentWindow.setCurrentWidget(self.pages_dict["Main Menu"]))
        