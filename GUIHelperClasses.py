"""
File: GUIHelperClasses.py
Brief: Contains helper classes to build larger widgets
Description: Contains definitions for all submenu items like dialogs and backgrounds
    that are used to suport larger menus. 
Author: Brandon Dennis
Version: 0.0.0
Last updated: 8/6/2025
TODO:
"""

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6 import QtWidgets
from PySide6.QtGui import QAction, QColor, QFont, QIcon, QKeySequence, QPalette, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QStackedLayout,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QWidget,
)

openFont = QFont()
openFont.setPointSize(50)

headerFont = QFont()
headerFont.setPointSize(20)


# Basic flat color widget for backgrounds.
class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

# Dialog box making sure the user wants to delete selected data.
class deleteDialog(QDialog):
    def __init__(self, type, name, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Confirm delete")

        # Create the button box enumeration from pre-determined options
        btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        # Initialize the button box and set events
        self.buttonBox = QDialogButtonBox(btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Arrange and set the layout
        layout = QVBoxLayout()
        message = QLabel(f"Would you like to delete {type}: {name}?")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


"""
miniView: Creates a widget that can be used for scrollable areas
Constructor takes in an index for later reference, a spacing value for text,
    and a list of HBoxLayouts for content to be added to the widget.
"""
class miniView(QWidget):
    def __init__(self, index=0, info=None, spacing=27):
        super().__init__()
        self.id = index

        # Add all content in the form of horizontal layouts
        layout = QVBoxLayout()
        if info is not None:
            for row in info:
                if row is None:
                    continue
                layout.addLayout(row)
        # If no layouts were found, add an empty label
        else:
            empty = QLabel("Empty")
            layout.addWidget(empty)
        # Set height according to spacing parameter and number of rows
        self.setFixedHeight(len(info) * spacing)
        self.setLayout(layout)

    def cleanup(self):
        # Go down each row and remove widgets.
        while self.layout().itemAt(0) != None:
            row = self.layout().itemAt(0)
            # Clear all of the data in each row
            while row.layout().itemAt(0) != None:
                w = row.layout().itemAt(0).wid
                w.setParent(None)
                row.removeWidget(w)
                w.deleteLater()
            row.setParent(None)
            self.layout().removeItem(row)
            row.deleteLater()
