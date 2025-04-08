"""
File:
Brief:
Description :
Author: Brandon Dennis
Version: 0.0.0
Last updated: 4/3/2025
TODO:
"""

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import (
    QAction,
    QColor,
    QFont,
    QIcon,
    QKeySequence,
    QPalette,
    QPixmap
)
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QStackedLayout,
    QCheckBox,
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QWidget
)


class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class dbView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


class monsterView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Monster Database')
        self.resize(300, 300)


class playerView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Player Character Database')
        self.resize(300, 300)


class partyView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PC Party Database')
        self.resize(300, 300)


class classView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Player Class Database')
        self.resize(300, 300)


class speciesView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Species Database')
        self.resize(300, 300)


class monsterTypeView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Monster Type Database')
        self.resize(300, 300)


class conditionView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Condition Database')
        self.resize(300, 300)
