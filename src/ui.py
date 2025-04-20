from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout
import sys
import os



TITLE = "RotMG Music Selector"
dir = "ref/"
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(TITLE)

        layout = QVBoxLayout()
        for ref_file in os.listdir(dir):
            button = QPushButton(ref_file)
            layout.addWidget(button)
        
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        
app = QApplication(sys.argv)

window = MainWindow()
window.show()




app.exec()


