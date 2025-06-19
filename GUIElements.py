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
from PySide6.QtCore import QSize, Qt, QTimer
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


class deleteDialog(QDialog):
    def __init__(self, type, name, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Confirm delete")
        
        # Create the button box enumeration from pre-determined options
        btn = (
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

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
        while self.layout.data.itemAt(0) != None:
            row = self.data.itemAt(0).wid
            # Clear all of the data in each row
            while row.data.itemAt(0) != None:
                w = row.data.itemAt(0).wid
                w.setParent(None)
                row.removeWidget(w)
                w.deleteLater()
            row.setParent(None)
            self.layout.removeWidget(row)
            row.deleteLater()


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
        self.addButton.clicked.connect(self.add)
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

    def add(self):
        match self.__class__.__name__:
            case "monsterView":
                self.interact = monsterInteract(Interactions.ADD)
            case "playerViewView":
                self.interact = playerInteract(Interactions.ADD)
            case "partyView":
                self.interact = partyInteract(Interactions.ADD)
            case "speciesView":
                self.interact = speciesInteract(Interactions.ADD)
            case "classView":
                self.interact = classInteract(Interactions.ADD)
            case "monsterTypeView":
                self.interact = monsterTypeInteract(Interactions.ADD)
            case "conditionView":
                self.interact = conditionInteract(Interactions.ADD)
            case _:
                self.interact = dbInteract(Interactions.ADD)
        self.interact.show()

    def edit(self, target):
        print('Edit')

    def populate(self):
        for i in range(25):
            dbEntry = QLabel(f"Tex Label {i}")
            self.data.addWidget(dbEntry)

    def cleanData(self):
        while (self.data.itemAt(0) != None):
            w = self.data.itemAt(0).wid
            # If this is one of the main tables, clear mini views.
            if w.__class__.__name__ == miniView:
                w.cleanup()                        
            # Clean up the attached widget
            w.setParent(None)
            self.data.removeWidget(w)
            w.deleteLater()


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
        # Clear all previous data in the section
        self.cleanData()
        # Go through all monsters in the database and generate a miniView widget
        for m in monsters.all():
            # Create a list of HBoxLayouts to send to the miniView constructor
            rows = [QHBoxLayout() for i in range(3)]
            # Pull information from database and assign them to widgets
            name = QPushButton(m['name'])
            name.clicked.connect(lambda checked=True, m=m: self.edit(m))
            cr = QLabel('Challenge Rating: ' + str(m['cr']))
            size = QLabel(sizes.get(doc_id=m["size"])["size"])
            maxHP = QLabel('Max HP: ' + readHP(m['hp']))
            type = QLabel(types.get(doc_id=m["type"])["name"])
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
        self.interact = monsterInteract(Interactions.EDIT, target, self)
        self.interact.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.hide()
        self.interact.show()


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
        # Clear all previous data in the section
        self.cleanData()
        # Go through all player characters in the database and generate a miniView widget
        for p in players.all():
            # Create a list of HBoxLayouts to send to the miniView constructor
            rows = [QHBoxLayout() for i in range(3)]
            # Pull information from database and assign them to widgets
            name = QPushButton(p["name"])
            name.clicked.connect(lambda checked=True, p=p: self.edit(p))
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
        self.interact = playerInteract(Interactions.EDIT, target, self)
        self.interact.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.hide()
        self.interact.show()


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
        self.interact = partyInteract(Interactions.EDIT, target, self)
        self.interact.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.hide()
        self.interact.show()


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
        # Clear all previous data in the section
        self.cleanData()
        # Go through all species in the database and generate a miniView widget
        for s in species.all():
            # Create a list of HBoxLayouts to send to the miniView constructor
            rows = [QHBoxLayout() for i in range(2)]
            # Pull information from database and assign them to widgets
            name = QPushButton(s["name"])
            name.clicked.connect(lambda checked=True, s=s: self.edit(s))
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
        self.interact = speciesInteract(Interactions.EDIT, target, self)
        self.interact.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.hide()
        self.interact.show()


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
        # Clear all previous data in the section
        self.cleanData()
        # Go through all player classes in the database and generate a miniView widget
        for c in classes.all():
            # Create a list of HBoxLayouts to send to the miniView constructor
            rows = [QHBoxLayout() for i in range(2)]
            # Pull information from database and assign them to widgets
            name = QPushButton(c["name"])
            name.clicked.connect(lambda checked=True, c=c: self.edit(c))
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
        self.interact = classInteract(Interactions.EDIT, target, self)
        self.interact.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.hide()
        self.interact.show()


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
        # Clear all previous data in the section
        self.cleanData()
        # Go through all monster types in the database and generate a miniView widget
        for t in types.all():
            # Create a list of HBoxLayouts to send to the miniView constructor
            rows = [QHBoxLayout() for i in range(2)]
            # Pull information from database and assign them to widgets
            name = QPushButton(t["name"])
            name.clicked.connect(lambda checked=True, t=t: self.edit(t))
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
        self.interact = monsterTypeInteract(Interactions.EDIT, target, self)
        self.interact.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.hide()
        self.interact.show()


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
        # Clear all previous data in the section
        self.cleanData()
        # Go through all conditions in the database and generate a miniView for each
        for c in conditions.all():
            # Create a list of HBoxLayouts for name and each sub-effect of the condition
            rows = [QHBoxLayout() for i in range(len(c['effects']) + 1)]
            # Tracks current row for effects
            row = 1
            # Create name button and assign to edit method for that entry
            name = QPushButton(c["name"])
            name.clicked.connect(lambda checked=True, c=c: self.edit(c))
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
        self.interact = conditionInteract(Interactions.EDIT, target, self)
        self.interact.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.hide()
        self.interact.show()


"""
dbInteract: A base template for database interactions like adding, editing, and deleting
Defines general purpose functionalities like a name field and button interactions.
"""
class dbInteract(QMainWindow):
    def __init__(self, type, target=None, source=None):
        super().__init__()
        # Set default size, layout, and background image for the menu
        self.type = type
        self.resize(800, 450)
        layout = QVBoxLayout()
        background = QLabel()
        background.setPixmap(QPixmap("images/background_medium.png"))
        background.setScaledContents(True)

        # Set the target object of the interaction and the data source
        self.target = target
        self.source = source

        # Set window title based on object type
        subject = ""
        match self.__class__.__name__:
            case "monsterInteract":
                subject = "Monster"
            case "playerInteract":
                subject = "Player Character"
            case "partyInteract":
                subject = "Party"
            case "speciesInteract":
                subject = "Species"
            case "classInteract":
                subject = "Player Class"
            case "monsterTypeInteract":
                subject = "Monster Type"
            case "conditionInteract":
                subject = "Condition"
        match type:
            case Interactions.ADD:
                self.setWindowTitle(f"Add New {subject}")
            case Interactions.EDIT:
                self.setWindowTitle(f"Edit {subject}")

        # Create a section for the name to be entered
        self.head = QVBoxLayout()
        self.name = QLineEdit()
        self.head.addWidget(self.name)
        layout.addLayout(self.head)

        # Central area for child classes to redefine
        self.mid = QVBoxLayout()
        layout.addLayout(self.mid)

        self.foot = QHBoxLayout()
        # Properly label the confirmation button depending on the requested action.
        match type:
            case Interactions.ADD:
                cLabel = "Add Entry"
            case Interactions.EDIT:
                cLabel = "Save Changes"
            case _:
                # Set a default label for undefined types
                cLabel = "Undefined"
        self.confirm = QPushButton(cLabel)
        self.confirm.clicked.connect(self.confirmAction)
        # If the item is being edited, add a button for deleting the entry.
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.destruct)
        self.foot.addWidget(self.confirm)
        self.foot.addWidget(cancel)
        if type == Interactions.EDIT:
            self.name.setText(target["name"])
            self.delete = QPushButton("Delete")
            self.delete.clicked.connect(lambda: self.deleteAction(subject, self.target))
            self.foot.addWidget(self.delete)
        layout.addLayout(self.foot)

        background.setLayout(layout)
        self.setCentralWidget(background)

    def confirmAction(self):
        print(f"CONFIRM {self.type}")
        return

    def deleteAction(self, type, target):
        confirmation = deleteDialog(type, target["name"], self)
        if confirmation.exec():
            match self.__class__.__name__:
                case "monsterInteract":
                    monsters.remove(doc_ids=[self.target.doc_id])
                case "playerInteract":
                    players.remove(doc_ids=[self.target.doc_id])
                case "partyInteract":
                    parties.remove(doc_ids=[self.target.doc_id])
                case "speciesInteract":
                    species.remove(doc_ids=[self.target.doc_id])
                case "classInteract":
                    classes.remove(doc_ids=[self.target.doc_id])
                case "monsterTypeInteract":
                    types.remove(doc_ids=[self.target.doc_id])
                case "conditionInteract":
                    conditions.remove(doc_ids=[self.target.doc_id])
            self.destruct()
        

    def destruct(self):
        self.head.deleteLater()
        self.name.deleteLater()
        self.mid.deleteLater()
        self.confirm.deleteLater()
        self.foot.deleteLater()
        self.source.populate()
        self.source.show()
        self.close()


"""
monsterInteract: Interact with monsters in the database by either adding new
    entries or manipulating existing ones.
Constructor sets additional fields for data entry/deletion
Defines data entry, edit, and deletion methods.
"""
class monsterInteract(dbInteract):
    def __init__(self, type, target=None, source=None):
        super().__init__(type, target, source)

    def confirmAction(self):
        return super().confirmAction()


"""
playerInteract: Interact with player characters in the database by either adding new
    entries or manipulating existing ones.
Constructor sets additional fields for data entry/deletion
Defines data entry, edit, and deletion methods.
"""
class playerInteract(dbInteract):
    def __init__(self, type, target=None, source=None):
        super().__init__(type, target, source)

    def confirmAction(self):
        return super().confirmAction()


"""
partyInteract: Interact with parties in the database by either adding new
    entries or manipulating existing ones.
Constructor sets additional fields for data entry/deletion
Defines data entry, edit, and deletion methods.
"""
class partyInteract(dbInteract):
    def __init__(self, type, target=None, source=None):
        super().__init__(type, target, source)

    def confirmAction(self):
        return super().confirmAction()


"""
speciesInteract: Interact with species in the database by either adding new
    entries or manipulating existing ones.
Constructor sets additional fields for data entry/deletion
Defines data entry, edit, and deletion methods.
"""
class speciesInteract(dbInteract):
    def __init__(self, type, target=None, source=None):
        super().__init__(type, target, source)

    def confirmAction(self):
        return super().confirmAction()


"""
classInteract: Interact with player classes in the database by either adding new
    entries or manipulating existing ones.
Constructor sets additional fields for data entry/deletion
Defines data entry, edit, and deletion methods.
"""
class classInteract(dbInteract):
    def __init__(self, type, target=None, source=None):
        super().__init__(type, target, source)

    def confirmAction(self):
        return super().confirmAction()


"""
monsterTypeInteract: Interact with monster types in the database by either adding new
    entries or manipulating existing ones.
Constructor sets additional fields for data entry/deletion
Defines data entry, edit, and deletion methods.
"""
class monsterTypeInteract(dbInteract):
    def __init__(self, type, target=None, source=None):
        super().__init__(type, target, source)

        self.description = QLineEdit()
        self.mid.addWidget(self.description)

        if type == Interactions.EDIT:
            self.description.setText(target["description"])

    def confirmAction(self):
        match self.type:
            case Interactions.ADD:
                types.insert(
                    {"name": self.name.text(), "description": self.description.text()}
                )
            case Interactions.EDIT:
                types.upsert(Document({"name": self.name.text(), "description": self.description.text()},
                              doc_id=self.target.doc_id))
        self.source.populate()
        self.source.show()
        self.close()

"""
conditionsInteract: Interact with conditions in the database by either adding new
    entries or manipulating existing ones.
Constructor sets additional fields for data entry/deletion
Defines data entry, edit, and deletion methods.
"""
class conditionInteract(dbInteract):
    def __init__(self, type, target=None, source=None):
        super().__init__(type, target, source)

    def confirmAction(self):
        return super().confirmAction()
