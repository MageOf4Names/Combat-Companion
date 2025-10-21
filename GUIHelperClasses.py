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

from HelperFunctions import *
from PySide6.QtCore import QSize, Qt, QTimer
from PySide6 import QtWidgets
from PySide6.QtGui import QAction, QColor, QFont, QIcon, QKeySequence, QPalette, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLayout,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QStackedLayout,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSpinBox,
    QStatusBar,
    QTabWidget,
    QTextEdit,
    QToolBar,
    QWidget
)

openFont = QFont()
openFont.setPointSize(50)

headerFont = QFont()
headerFont.setPointSize(20)


# Method for clearing up spare widgets from memory
def cleanWidget(widget):
    for child in widget.children():
        if issubclass(child.__class__, QLayout):
            cleanWidget(child)
        else:
            child.deleteLater()
    widget.deleteLater()


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


"""
actionView
Creates a container for the user to enter data for an action. This includes the action's
    name, hit bonus, range, targets, damage, type, and additional notes.
"""
class actionView(QWidget):
    def __init__(self, name=None, preload=None):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        self.name = QLineEdit()
        self.bonus = QSpinBox()
        self.range = QSpinBox()
        self.targets = QComboBox()
        self.targets.addItems(["Single Target", "Area of Effect"])
        self.damageList = []
        self.damage = QPushButton()
        damageLabel = QLabel("N/A")
        self.damage.clicked.connect(lambda: self.damagePopup(damageLabel))
        self.info = QTextEdit()
        self.info.setMaximumHeight(50)

        # Preload data if this is editing existing data
        if preload != None and name != None:
            self.name.setText(name)
            self.range.setValue(preload["range"])
            self.bonus.setValue(preload["hit_bonus"])
            self.targets.setCurrentText(preload["targets"])
            dmgText = ""
            for dmg in preload["damage"]:
                self.damageList.append(dmg)
                dmgText += dmg + " + "
            damageLabel.setText(dmgText[0: -3])
            self.info.setText(preload["extra"])

        layout.addWidget(QLabel("Name: "), 0, 0)
        layout.addWidget(self.name, 0, 1)
        layout.addWidget(QLabel("Hit Bonus:"), 0, 2)
        layout.addWidget(self.bonus, 0, 3)
        layout.addWidget(QLabel("Range: "), 1, 0)
        layout.addWidget(self.range, 1, 1)
        layout.addWidget(QLabel("Targets: "), 1, 2)
        layout.addWidget(self.targets, 1, 3)
        layout.addWidget(QLabel("Damage: "), 2, 0)
        layout.addWidget(damageLabel, 2, 1, 1, 2)
        layout.addWidget(self.damage, 2, 3)
        layout.addWidget(QLabel("Additional Info:"), 3, 0, 1, 2)
        layout.addWidget(self.info, 4, 0, 1, -1)

    def damagePopup(self, label):
        success = damageDialog(self).exec()
        if success:
            labelText = ""
            for i in self.damageList:
                labelText += i + ", "
            label.setText(labelText[0: -2])

    def toDict(self):
        name = self.name.text()
        dictify = {}
        dictify["range"] = self.range.value()
        dictify["hit_bonus"] = self.bonus.value()
        dictify["targets"] = self.targets.currentText()
        dictify["damage"] = self.damageList
        dictify["extra"] = self.info.toPlainText()
        return name, dictify

    def destruct(self):
        cleanWidget(self)


"""
traitView
Creates a container for a special feature (lair action, special trait, legendary action, etc.)
    and contains inputs for a name and a description box.
"""
class traitView(QWidget):
    def __init__(self, name=None, data=None):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        self.name = QLineEdit()
        self.desc = QTextEdit()
        self.desc.setMaximumHeight(50)

        # Preload data if this is an edit of existing data
        if name != None and data != None:
            self.name.setText(name)
            self.desc.setText(data)

        layout.addWidget(QLabel("Name: "), 0, 0)
        layout.addWidget(self.name, 0, 1)
        layout.addWidget(QLabel("Description:"), 1, 0)
        layout.addWidget(self.desc, 2, 0, 1, -1)

    def toDict(self):
        return self.name.text(), self.desc.toPlainText()

    def destruct(self):
        cleanWidget(self)


"""
damageDialog
Defines a popup dialog for defining the damage of an attack
"""
class damageDialog(QDialog):
    def __init__(self, src):
        super().__init__()

        self.setWindowTitle("Assign Damage")

        # Create the button box enumeration from pre-determined options
        btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        # Initialize the button box and set events
        self.buttonBox = QDialogButtonBox(btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Set an attribute to point to the source of the dialog
        self.source = src

        # If there is already data in the damage list, parse it so it can be
        # preloaded into the form fields
        prefillFlag = False
        prefillList = []
        if len(self.source.damageList) > 0:
            prefillFlag = True
            for dmg in self.source.damageList:
                prefillList.append(
                    re.findall(r"[0-9]+d[0-9]{1,2}| [+-] |[0-9]+|[a-zA-Z]{3,20}", dmg)
                )

        # Arrange and set the layout
        layout = QGridLayout()
        self.diceNum = []
        self.diceType = []
        self.operation = []
        self.additional = []
        for count in range(len(damageType)):
            # Initialize all of the input areas for each damage type
            self.diceNum.append(QSpinBox())
            self.diceType.append(QComboBox())
            self.diceType[count].addItems(["d4", "d6", "d8", "d10", "d12"])
            self.operation.append(QComboBox())
            self.operation[count].addItems([" + ", " - "])
            self.additional.append(QSpinBox())
            # If there is existing data and there are elements still unfilled
            # Preload the form fields now
            if prefillFlag and len(prefillList) > 0:
                # Match the prefill type with current type
                if prefillList[0][-1] == damageType[count]:
                    # Determine the type of input
                    # (Dice only, dice and static damage, or just static)
                    if len(prefillList[0]) == 4:
                        # Splid dice values into quantity and type
                        diceSplit = re.split(r'd', prefillList[0][0])
                        self.diceNum[count].setValue(int(diceSplit[0]))
                        self.diceType[count].setCurrentText("d" + diceSplit[1])
                        self.operation[count].setCurrentText(prefillList[0][1])
                        self.additional[count].setValue(int(prefillList[0][2]))
                    # Case with only dice damage
                    elif "d" in prefillList[0][0]:
                        diceSplit = re.split(r"d", prefillList[0][0])
                        self.diceNum[count].setValue(int(diceSplit[0]))
                        self.diceType[count].setCurrentText("d" + diceSplit[1])
                    # Case with just static damage
                    else:
                        self.additional[count].setValue(int(prefillList[0][0]))
                    # remove this item from the list
                    prefillList.pop(0)
            layout.addWidget(self.diceNum[count], count, 0)
            layout.addWidget(self.diceType[count], count, 1)
            layout.addWidget(self.operation[count], count, 2)
            layout.addWidget(self.additional[count], count, 3)
            layout.addWidget(QLabel(damageType[count]), count, 4)
        layout.addWidget(self.buttonBox, count + 1, 0, 1, -1)
        self.setLayout(layout)

    def accept(self):
        super().accept()
        self.source.damageList = []
        # Add all relevant damage sources to an array to return
        for i in range(len(self.diceNum)):
            # If damage type has both dice to roll and additional damage modifier
            if self.diceNum[i].value() != 0 and self.additional[i].value() != 0:
                self.source.damageList.append(
                    f"({self.diceNum[i].value()}{self.diceType[i].currentText()}{self.operation[i].currentText()}{self.additional[i].value()}){damageType[i]}")
            # Damage source only has dice to determine damage
            elif self.diceNum[i].value() != 0 and self.additional[i].value() == 0:
                self.source.damageList.append(f"({self.diceNum[i].value()}{self.diceType[i].currentText()}){damageType[i]}")
            # Damage source only has static damage
            elif self.diceNum[i].value() == 0 and self.additional[i].value() != 0:
                self.source.damageList.append(f"({self.additional[i].value()}){damageType[i]}")


"""
hitpointDialog
Defines a popup dialog for defining the hitpoints of a monster
"""
class hitpointDialog(QDialog):
    def __init__(self, src):
        super().__init__()

        self.setWindowTitle("Define Hitpoits")

        # Create the button box enumeration from pre-determined options
        btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        # Initialize the button box and set events
        self.buttonBox = QDialogButtonBox(btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Set an attribute to point to the source of the dialog
        self.source = src

        # If there is already data in the damage list, parse it so it can be
        # preloaded into the form fields
        prefillFlag = False
        if self.source.maxHP.text() != "Enter HP":
            prefillFlag = True

        # Arrange and set the layout
        layout = QGridLayout()

        # Define form elements
        self.diceNum = QSpinBox()
        self.diceType = QComboBox()
        self.diceType.addItems(["d4", "d6", "d8", "d10", "d12", "d20"])
        self.additional = QSpinBox()
        # If there is existing data and there are elements still unfilled
        # Preload the form fields now
        if prefillFlag:
            data = re.split(r"[:d+]", self.source.maxHP.text())
            # Toss the old average (recalculate at accept) and prefill form fields
            self.diceNum.setValue(data[1])
            self.diceType.setCurrentText(f"d{data[2]}")
            self.additional.setValue(data[3])
        # Arrange the layout with form elements
        layout.addWidget(self.diceNum, 0, 0)
        layout.addWidget(self.diceType, 0, 1)
        layout.addWidget(self.additional, 0, 2)
        layout.addWidget(self.buttonBox, 1, 0, 1, -1)
        self.setLayout(layout)

    def accept(self):
        super().accept()
        avg = int(self.diceNum.value() * (float(self.diceType.currentText()[1:]) / 2 + 0.5) + self.additional.value())
        self.source.maxHP.setText(
                f"{avg}:{self.diceNum.value()}{self.diceType.currentText()}+{self.additional.value()}"
            )


"""
hitpointDialog
Defines a popup dialog for defining the hitpoints of a monster
"""
class classDialog(QDialog):
    def __init__(self, src):
        super().__init__()

        self.setWindowTitle("Enter Class Information")

        # Create the button box enumeration from pre-determined options
        btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        # Initialize the button box and set events
        self.buttonBox = QDialogButtonBox(btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Set an attribute to point to the source of the dialog
        self.source = src

        # If there is already data in the damage list, parse it so it can be
        # preloaded into the form fields
        prefillFlag = False
        prefillList = {}
        if len(self.source.classDict.items()) > 0:
            prefillFlag = True
            for cl, lvl in self.source.classDict.items():
                prefillList[cl] = lvl

        # Arrange and set the layout
        layout = QGridLayout()
        self.classInputs = []
        count = 0
        for cls in classes.all():
            # Initialize all of the input areas for each class
            self.classInputs.append(QSpinBox())
            # If there is existing data and there are elements still unfilled
            # Preload the form fields now
            if prefillFlag and len(prefillList.items()) > 0:
                # Match the prefill type with current type
                if cls["name"] in prefillList.keys():
                    # Case with just static damage
                    self.classInputs[count].setValue(prefillList[cls["name"]])
                    # remove this item from the list
                    prefillList.pop(cls["name"])
            layout.addWidget(QLabel(cls["name"] + ": "), count, 0)
            layout.addWidget(self.classInputs[count], count, 1)
            count += 1
        layout.addWidget(self.buttonBox, count + 1, 0, 1, -1)
        self.setLayout(layout)

    def accept(self):
        super().accept()
        count = 0
        level = 0
        classStr = ""
        for cls in self.classInputs:
            if cls.value() > 0:
                name = classes.all()[count]["name"]
                self.source.classDict[name] = cls.value()
                classStr += f"{name} {cls.value()}, "
                level += cls.value()
            count += 1
        self.source.level.setValue(level)
        self.source.charClass.setText(classStr[0: -2])
