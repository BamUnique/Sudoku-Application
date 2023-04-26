import sys
from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QGroupBox, QStackedWidget, QLabel
from PyQt6.QtCore import Qt, QCoreApplication, QRect
from PyQt6.QtGui import QFont

import newgui
import loginfeature
import difficulty_selection
import menu

app = QApplication(sys.argv)

currentPage = QStackedWidget()

WINDOWS = {"Main Menu": menu.SelectionMenu(currentPage),
            "Difficulty Window": difficulty_selection.DifficultySelection(currentPage),
            "Game Window": newgui.Window(0.6, currentPage),
            "Test Window": menu.TestPage(currentPage),
            "Login Window": loginfeature.LoginScreen(currentPage),
            "Account Creation": loginfeature.CreateNewAccount(currentPage)}



def init_pages():
    for key in WINDOWS:
        print(key, WINDOWS[key])
        currentPage.addWidget(WINDOWS[key])

        

        
def change_window(window_index):
    currentPage.setCurrentWidget(WINDOWS[window_index])


if __name__ == '__main__':
    
    
    app = QApplication(sys.argv)
    init_pages()

    
    
    change_window("Main Menu")
    currentPage.show()

    
    
    sys.exit(app.exec())