from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QLineEdit
from PySide6.QtCore import QTimer

import sys
import os

import globals as globals

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(globals.TITLE)

        self.layout = QVBoxLayout()
        self.line_edit = QLineEdit()

        self.display()
        
        self.loading()

    
    def loading(self):
        self.layout.addWidget(self.line_edit)
        for i in range(1,101):
            self.line_edit.setText(f"{i}")   


        

    def display(self):

        for ref_file in os.listdir(globals.REF_DIR):
            if os.path.isdir(os.path.join(globals.REF_DIR, ref_file)):
                button = QPushButton(ref_file)
                self.layout.addWidget(button)
        


        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


