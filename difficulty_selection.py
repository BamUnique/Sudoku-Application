from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout, QGroupBox, QStackedWidget, QComboBox
import sys

class DifficultySelection(QMainWindow):
    def __init__(self, currentPage):
        super().__init__()
        
        self.currentPage = currentPage
        self.setFixedSize(618, 500)
        
        self.difficulty_dict = {"Easy": 0.5, "Medium": 0.6, "Hard": 0.7, "Expert": 0.8}
        self.choose_difficulty_selection = QComboBox(self)
        self.choose_difficulty_selection.addItems(["Easy", "Medium", "Hard", "Expert"])
        # self.choose_difficulty_selection.move()
        
        
if __name__ == '__main__':
    
    # app = menu.QApplication(sys.argv)
    # main_menu = menu.SelectionMenu()
    # main_menu.show()
    
    app = QApplication(sys.argv)
    
    
    window = DifficultySelection()
    window.show()
    
    sys.exit(app.exec())
