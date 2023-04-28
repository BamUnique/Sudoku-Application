import sys
from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QGroupBox, QStackedWidget, QLabel
from PyQt6.QtCore import Qt, QCoreApplication, QRect
from PyQt6.QtGui import QFont



class SettingsScreen(QMainWindow):
    
    def __init__(self, currentWindow, pages_dict):
        super().__init__()
        self.setWindowTitle("Settings Screen")
        self.setGeometry(0, 0, 618, 500)
        