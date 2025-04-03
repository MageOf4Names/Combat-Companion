"""
Author: Brandon Dennis
Version: 1.0.0
Last updated: 
PyInstaller Command: python -m PyInstaller 'DataHandler.spec'
"""

import sys

from CoreClasses import *
from GUIElements import *

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()