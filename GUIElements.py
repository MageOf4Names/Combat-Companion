"""
File: GUIElements.py
Brief: Contains all custom widgets and menus for the Combat Companion app
Description: Outlines all the non-basic classes and visual elements for the application.
    This includes submenus, editing logic, database views, as well as helper classes and
    widgets to improve the look and feel of the app.
Author: Brandon Dennis
Version: 0.0.0
Last updated: 4/11/2025
TODO:
"""

from HelperFunctions import *
from PySide6.QtCore import QSize, Qt
from PySide6 import QtWidgets
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
    QScrollArea,
    QSpinBox,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QWidget
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


"""
dbView: Parent class for all of the database views. Sets a header, scrollable area for content,
    and a button menu for adding new entries and returning to the main menu.
Constructor builds the basic layout including setting background and creating scrollable area
Includes shells for methods like populating the scrollable area, adding, and editing data.
"""
class dbView(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set default size, layout, and background image for the menu
        self.resize(800, 450)
        layout = QVBoxLayout()
        background = QLabel()
        background.setPixmap(QPixmap("images/background_medium.png"))
        background.setScaledContents(True)

        # Defines the label indicating what database the user is in
        self.label = QLabel('Another Menu')
        self.label.setFont(headerFont)
        # Add to the main layout
        layout.addWidget(self.label)

        # Create the layout for the area and populate it with the appropriate data
        self.data = QVBoxLayout()
        self.populate()
        self.dbArea = Color("#F1E9D2")
        self.dbArea.setLayout(self.data)
        # Define the scrollable area in the center of the menu. This will contain all the current data
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.dbArea)
        # Add to the main layout
        layout.addWidget(self.scroll)

        # Creates the buttons for returning to the main menu and adding a new entry to the database
        self.addButton = QPushButton()
        self.addButton.clicked.connect(self.addNew)
        returnButton = QPushButton('Return')
        returnButton.clicked.connect(self.hide)
        # Puts the buttons in a menu to add to the bottom of the menu
        buttonMenu = QHBoxLayout()
        buttonMenu.addWidget(self.addButton)
        buttonMenu.addWidget(returnButton)
        # Add to the main layout
        layout.addLayout(buttonMenu)

        background.setLayout(layout)
        self.setCentralWidget(background)

    def addNew(self):
        print('Add')

    def edit(self, target):
        print('Edit')

    def populate(self):
        for i in range(25):
            dbEntry = QLabel(f"Tex Label {i}")
            self.data.addWidget(dbEntry)


"""
monsterView: View of the current monsters database
Constructor sets the window label and text labels.
Overrides all the shell methods set up in the superclass.
"""
class monsterView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Monster Database')
        self.label.setText('Monsters')
        self.addButton.setText('Add a new Monstser')

    def populate(self):
        # Go through all monsters in the database and generate a miniView widget
        for m in monsters.all():
            # Create a list of HBoxLayouts to send to the miniView constructor
            rows = [QHBoxLayout() for i in range(3)]
            # Pull information from database and assign them to widgets
            name = QPushButton(m['name'])
            name.clicked.connect(lambda: self.edit(m))
            cr = QLabel('Challenge Rating: ' + str(m['cr']))
            size = QLabel(sizes.get(doc_id=m["size"])["size"])
            maxHP = QLabel('Max HP: ' + readHP(m['hp']))
            type = QLabel(types.get(doc_id=m["type"])["type"])
            ac = QLabel('AC: ' + str(m['ac']))
            # Add widgets to the appropriate layouts
            rows[0].addWidget(name)
            rows[0].addWidget(cr)
            rows[1].addWidget(size)
            rows[1].addWidget(maxHP)
            rows[2].addWidget(type)
            rows[2].addWidget(ac)
            # Generate miniView and add to the scrollable area in dbView
            monster = miniView(m.doc_id, rows)
            self.data.addWidget(monster)

    def edit(self, target):
        super().edit(target)

    def addNew(self):
        super().addNew()


"""
playerView: View of the current player character database
Constructor sets the window label and text labels.
Overrides all the shell methods set up in the superclass.
"""
class playerView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Player Character Database')
        self.label.setText('Player Characters')
        self.addButton.setText('Add a new Player Character')

    def populate(self):
        # Go through all player characters in the database and generate a miniView widget
        for p in players.all():
            # Create a list of HBoxLayouts to send to the miniView constructor
            rows = [QHBoxLayout() for i in range(3)]
            # Pull information from database and assign them to widgets
            name = QPushButton(p["name"])
            name.clicked.connect(lambda: self.edit(p))
            level = QLabel("Level: " + str(p["level"]))
            spec = QLabel(species.get(doc_id=p["species"])["name"])
            maxHP = QLabel("Max HP: " + str(p["hp"]))
            pclass = QLabel(classes.get(doc_id=int([*p["class"]][0]))["name"])
            ac = QLabel("AC: " + str(p["ac"]))
            # Add widgets to the appropriate layouts
            rows[0].addWidget(name)
            rows[0].addWidget(level)
            rows[1].addWidget(spec)
            rows[1].addWidget(maxHP)
            rows[2].addWidget(pclass)
            rows[2].addWidget(ac)
            # Generate miniView and add to the scrollable area in dbView
            player = miniView(p.doc_id, rows)
            self.data.addWidget(player)

    def edit(self, target):
        super().edit(target)

    def addNew(self):
        super().addNew()


"""
partyView: View of the current party database
Constructor sets the window label and text labels.
Overrides all the shell methods set up in the superclass.
"""
class partyView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PC Party Database')
        self.label.setText('Parties')
        self.addButton.setText('Add a new Party')

    def populate(self):
        super().populate()

    def edit(self, target):
        super().edit(target)

    def addNew(self):
        super().addNew()


"""
speciesView: View of the current species database
Constructor sets the window label and text labels.
Overrides all the shell methods set up in the superclass.
"""
class speciesView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Species Database')
        self.label.setText('Species')
        self.addButton.setText('Add a new Species')

    def populate(self):
        # Go through all species in the database and generate a miniView widget
        for s in species.all():
            # Create a list of HBoxLayouts to send to the miniView constructor
            rows = [QHBoxLayout() for i in range(2)]
            # Pull information from database and assign them to widgets
            name = QPushButton(s["name"])
            name.clicked.connect(lambda: self.edit(s))
            speed = QLabel("Speed: " + s["speed"] + " feet")
            # Multiple sizes are possible, so concatenate all potential options
            sizes = ''
            for i in s['size']:
                sizes += i + '/'
            size = QLabel(sizes[:-1])
            # Add widgets to the appropriate layouts
            rows[0].addWidget(name)
            rows[0].addWidget(speed)
            rows[1].addWidget(size)
            # Generate miniView and add to the scrollable area in dbView
            species_entry = miniView(s.doc_id, rows, 30)
            self.data.addWidget(species_entry)

    def edit(self, target):
        super().edit(target)

    def addNew(self):
        super().addNew()


"""
classView: View of the current player class database
Constructor sets the window label and text labels.
Overrides all the shell methods set up in the superclass.
"""
class classView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Player Class Database')
        self.label.setText('Player Classes')
        self.addButton.setText('Add a new Class')

    def populate(self):
        # Go through all player classes in the database and generate a miniView widget
        for c in classes.all():
            # Create a list of HBoxLayouts to send to the miniView constructor
            rows = [QHBoxLayout() for i in range(2)]
            # Pull information from database and assign them to widgets
            name = QPushButton(c["name"])
            name.clicked.connect(lambda: self.edit(c))
            hit = QLabel('Hit Die: ' + c['hit-die'])
            saves = QLabel(c['saving-throws'][0] + ', ' + c['saving-throws'][1])
            # Add widgets to the appropriate layouts
            rows[0].addWidget(name)
            rows[0].addWidget(hit)
            rows[1].addWidget(saves)
            # Generate miniView and add to the scrollable area in dbView
            pclass = miniView(c.doc_id, rows, 30)
            self.data.addWidget(pclass)

    def edit(self, target):
        super().edit(target)

    def addNew(self):
        super().addNew()


"""
monsterTypeView: View of the current monster types database
Constructor sets the window label and text labels.
Overrides all the shell methods set up in the superclass.
"""
class monsterTypeView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Monster Type Database')
        self.label.setText('Database')
        self.addButton.setText('Add a new Monster Type')

    def populate(self):
        charLimit = 100
        # Go through all monster types in the database and generate a miniView widget
        for t in types.all():
            # Create a list of HBoxLayouts to send to the miniView constructor
            rows = [QHBoxLayout() for i in range(2)]
            # Pull information from database and assign them to widgets
            name = QPushButton(t["type"])
            name.clicked.connect(lambda: self.edit(t))
            # If the description of an entry is too long, shorten it and add indicator
            if len(t['description']) > charLimit:
                desc = QLabel(t['description'][0: charLimit - 3] + "...")
            else:
                desc = QLabel(t['description'])
            # Add widgets to the appropriate layouts
            rows[0].addWidget(name)
            rows[1].addWidget(desc)
            # Generate miniView and add to the scrollable area in dbView
            pclass = miniView(t.doc_id, rows, 30)
            self.data.addWidget(pclass)

    def edit(self, target):
        super().edit(target)

    def addNew(self):
        super().addNew()


"""
conditionView: View of the current conditions database
Constructor sets the window label and text labels.
Overrides all the shell methods set up in the superclass.
"""
class conditionView(dbView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Condition Database')
        self.label.setText('Conditions')
        self.addButton.setText('Add a new Condition')

    def populate(self):
        charLimit = 100
        # Go through all conditions in the database and generate a miniView for each
        for c in conditions.all():
            # Create a list of HBoxLayouts for name and each sub-effect of the condition
            rows = [QHBoxLayout() for i in range(len(c['effects']) + 1)]
            # Tracks current row for effects
            row = 1
            # Create name button and assign to edit method for that entry
            name = QPushButton(c["name"])
            name.clicked.connect(lambda: self.edit(c))
            # Go down the list of effects and add the text to the appropriate layout
            for e in c['effects']:
                # If an effect description is too long, shorten it and add indicator
                if len(e) >  charLimit:
                    desc = e[0: charLimit - 3] + "..."
                else:
                    desc = e
                effect = QLabel(desc)
                rows[row].addWidget(effect)
                row += 1
            # Add the name tag to the top row
            rows[0].addWidget(name)
            # Generate miniView and add to the scrollable area in dbView
            species_entry = miniView(c.doc_id, rows, 30)
            self.data.addWidget(species_entry)

    def edit(self, target):
        super().edit(target)

    def addNew(self):
        super().addNew()
