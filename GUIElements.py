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

from GUIHelperClasses import *
from HelperFunctions import *

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
                self.interact = monsterInteract(Interactions.ADD, source=self)
            case "playerView":
                self.interact = playerInteract(Interactions.ADD, source=self)
            case "partyView":
                self.interact = partyInteract(Interactions.ADD, source=self)
            case "speciesView":
                self.interact = speciesInteract(Interactions.ADD, source=self)
            case "classView":
                self.interact = classInteract(Interactions.ADD, source=self)
            case "monsterTypeView":
                self.interact = monsterTypeInteract(Interactions.ADD, source=self)
            case "conditionView":
                self.interact = conditionInteract(Interactions.ADD, source=self)
            case _:
                self.interact = dbInteract(Interactions.ADD, source=self)
        self.interact.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.hide()
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
            if w.__class__.__name__ == 'miniView':
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
            classStr = ""
            for k, v in p["class"].items():
                classStr += f"{k} {v},"
            pclass = QLabel(classStr[0: -1])
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
        self.layout = QGridLayout()
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
        self.head = QGridLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText(f"{subject} Name")
        self.head.addWidget(self.name, 0, 0, 2, 1)
        self.layout.addLayout(self.head, 0, 0)

        # Central area for child classes to redefine
        self.mid = QVBoxLayout()
        self.layout.addLayout(self.mid, 1, 0)

        self.foot = QGridLayout()
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
        self.foot.addWidget(self.confirm, 0, 0)
        self.foot.addWidget(cancel, 0, 1)
        if type == Interactions.EDIT:
            self.name.setText(target["name"])
            self.delete = QPushButton("Delete")
            self.delete.clicked.connect(lambda: self.deleteAction(subject, self.target))
            self.foot.addWidget(self.delete, 1, 1)
        self.layout.addLayout(self.foot, 2, 0)

        background.setLayout(self.layout)
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
        self.setParent(None)
        cleanWidget(self)
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
        self.resize(1400, 1100)
        self.saves = [0 for i in range(6)]

        # Add hp, ac, alignment, and initiative to the head layout
        self.maxHP = QPushButton("Enter HP")
        self.maxHP.clicked.connect(self.hitpointPopup)
        self.ac = QSpinBox(value=10)
        self.align = QComboBox()
        self.align.addItems(alignments)
        self.init = QSpinBox(value=0)
        self.head.addWidget(QLabel("Max HP"), 0, 2)
        self.head.addWidget(self.maxHP, 0, 3)
        self.head.addWidget(QLabel("Armor Class"), 0, 4)
        self.head.addWidget(self.ac, 0, 5)
        self.head.addWidget(QLabel("Alignment"), 1, 2)
        self.head.addWidget(self.align, 1, 3)
        self.head.addWidget(QLabel("Initiative"), 1, 4)
        self.head.addWidget(self.init, 1, 5)

        # Define and fill the layout with creature type, size, cr, and xp
        self.typeLayout = QHBoxLayout()
        self.monType = QComboBox()\
        # Pull data from reference tables to fill out monster types
        for t in types.all():
            self.monType.addItem(t["name"])
        self.monSize = QComboBox()
        # Pull data from reference tables to fill out monster sizes
        for s in sizes.all():
            self.monSize.addItem(s["size"])
        self.cr = QDoubleSpinBox(decimals=2, singleStep=0.25)
        self.xp = QSpinBox(value=0)
        self.typeLayout.addWidget(QLabel("Monster Type: "))
        self.typeLayout.addWidget(self.monType)
        self.typeLayout.addWidget(QLabel("Size: "))
        self.typeLayout.addWidget(self.monSize)
        self.typeLayout.addWidget(QLabel("CR: "))
        self.typeLayout.addWidget(self.cr)
        self.typeLayout.addWidget(QLabel("XP Value: "))
        self.typeLayout.addWidget(self.xp)
        # Add the layout to the main mid layout
        self.mid.addLayout(self.typeLayout)

        # Define and fill the layout with stats and saving throw proficiencies
        self.statLayout = QGridLayout()
        self.statInputs = []
        count = 0
        for stat in statDict.keys():
            self.statLayout.addWidget(QLabel(stat + ": "), 0, 2 * count)
            self.statInputs.append(QSpinBox(value=10))
            self.statLayout.addWidget(self.statInputs[count], 0, 2 * count + 1)
            count += 1
        # Create a button group with all stats for saving throws
        savesGroup = QButtonGroup(self)
        savesGroup.setExclusive(False)
        savesGroup.buttonToggled.connect(self.onToggle)
        count = 0
        for s in statDict.keys():
            checkBox = QCheckBox(s + " Save")
            self.statLayout.addWidget(checkBox, 1, 2 * count, 2, 1)
            savesGroup.addButton(checkBox, statDict[s])
            count += 1
        # Add the layout to the main mid layout
        self.mid.addLayout(self.statLayout)

        # Define and fill the layout containing skills and legendary checks
        self.skillLayout = QGridLayout()
        # Create a dropdown box for every skill and add it to the layout
        count = 0
        self.skillInputs = []
        for sk in skills.all():
            self.skillInputs.append(QComboBox())
            self.skillInputs[count].addItems(profDict.keys())
            self.skillLayout.addWidget(QLabel(sk["skill"]), count, 0)
            self.skillLayout.addWidget(self.skillInputs[count], count, 1)
            count += 1
        # Create and add entries for legendary tags and legendary resistances
        self.legend = QRadioButton("Legendary")
        self.legend_res = QSpinBox()
        self.skillLayout.addWidget(self.legend, count, 0, 1, 2)
        self.skillLayout.addWidget(QLabel("Legendary Resistances: "), count + 1, 0)
        self.skillLayout.addWidget(self.legend_res, count + 1, 1)

        # Define and fill the layout containing resistances and actions
        self.actionLayout = QVBoxLayout()

        self.actionLayout.addWidget(QLabel("Monster Actions"))
        # Define a list to track all actions
        self.actionList = [actionView()]
        # Create a backdrop for the scrollable area
        self.actionBackdrop = QVBoxLayout()
        if type != Interactions.EDIT:
            self.actionList.append(actionView())
            self.actionBackdrop.addWidget(self.actionList[0])
        self.actionEffectArea = Color("#F1E9D2")
        self.actionEffectArea.setLayout(self.actionBackdrop)
        # Define the scrollable area for monster actions
        self.actionArea = QScrollArea()
        self.actionArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.actionArea.setWidgetResizable(True)
        self.actionArea.setWidget(self.actionEffectArea)
        self.actionLayout.addWidget(self.actionArea)
        # Make a button to add additional elements
        addAction = QPushButton("Add Action")
        addAction.clicked.connect(lambda: self.addElement(ActionType.ACTION))
        self.actionLayout.addWidget(addAction)

        self.actionLayout.addWidget(QLabel("Special Traits"))
        # Define a list to track all special traits
        self.traitList = []
        # Create a backdrop for the scrollable area
        self.traitBackdrop = QVBoxLayout()
        self.traitEffectArea = Color("#F1E9D2")
        self.traitEffectArea.setLayout(self.traitBackdrop)
        # Define the scrollable area for monster actions
        self.traitArea = QScrollArea()
        self.traitArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.traitArea.setWidgetResizable(True)
        self.traitArea.setWidget(self.traitEffectArea)
        self.actionLayout.addWidget(self.traitArea)
        # Make a button to add additional elements
        addTrait = QPushButton("Add Trait")
        addTrait.clicked.connect(lambda: self.addElement(ActionType.TRAIT))
        self.actionLayout.addWidget(addTrait)

        self.actionLayout.addWidget(QLabel("Legendary Actions"))
        # Define a list to track all legendary actions
        self.lActionList = []
        # Create a backdrop for the scrollable area
        self.legendBackdrop = QVBoxLayout()
        self.legendEffectArea = Color("#F1E9D2")
        self.legendEffectArea.setLayout(self.legendBackdrop)
        # Define the scrollable area for monster actions
        self.legActionArea = QScrollArea()
        self.legActionArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.legActionArea.setWidgetResizable(True)
        self.legActionArea.setWidget(self.legendEffectArea)
        self.actionLayout.addWidget(self.legActionArea)
        # Make a button to add additional elements
        addLegAction = QPushButton("Add Legendary Action")
        addLegAction.clicked.connect(lambda: self.addElement(ActionType.LEG_ACTION))
        self.actionLayout.addWidget(addLegAction)

        self.actionLayout.addWidget(QLabel("Lair Actions"))
        # Define a list to track all lair actions
        self.lairActions = []
        # Create a backdrop for the scrollable area
        self.lairBackdrop = QVBoxLayout()
        self.lairEffectArea = Color("#F1E9D2")
        self.lairEffectArea.setLayout(self.lairBackdrop)
        # Define the scrollable area for monster actions
        self.lairActionArea = QScrollArea()
        self.lairActionArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.lairActionArea.setWidgetResizable(True)
        self.lairActionArea.setWidget(self.lairEffectArea)
        self.actionLayout.addWidget(self.lairActionArea)
        # Make a button to add additional elements
        addLairAction = QPushButton("Add Lair Action")
        addLairAction.clicked.connect(lambda: self.addElement(ActionType.LAIR_ACTION))
        self.actionLayout.addWidget(addLairAction)

        # Create an area for notes
        self.notes = QTextEdit()
        self.notes.setMaximumHeight(40)
        self.actionLayout.addWidget(QLabel("Additional Notes:"))
        self.actionLayout.addWidget(self.notes)

        # Define and fill the layout containing speeds and sesnses
        self.speedLayout = QGridLayout()

        self.speedLayout.addWidget(QLabel("Movement Speeds"), 0, 0, 1, 2)
        countSp = 0
        self.speedInputs = []
        for sp in movements:
            self.speedInputs.append(QSpinBox(value=30 if countSp == 0 else 0))
            self.speedLayout.addWidget(QLabel(sp), countSp + 1, 0)
            self.speedLayout.addWidget(self.speedInputs[countSp], countSp + 1, 1)
            countSp += 1

        self.speedLayout.addWidget(QLabel("Senses"), countSp + 2, 0, 1, 2)
        countSe = 0
        self.senseInputs = []
        for se in senses.all():
            self.senseInputs.append(QSpinBox())
            self.speedLayout.addWidget(QLabel(se["sense"]), countSe + countSp + 3, 0)
            self.speedLayout.addWidget(self.senseInputs[countSe], countSe + countSp + 3, 1)
            countSe += 1

        self.speedLayout.addWidget(QLabel("Weaknesses/Resistances"), countSp + countSe + 3, 0, 1, 2)
        countDa = 0
        self.damageInputs = []
        for dmg in damageType:
            self.damageInputs.append(QComboBox())
            self.damageInputs[countDa].addItems(damageDict.keys())
            self.speedLayout.addWidget(QLabel(dmg), countSp + countSe + countDa + 4, 0)
            self.speedLayout.addWidget(self.damageInputs[countDa], countSp + countSe + countDa + 4, 1)
            countDa += 1

        # Create a shell for the body elements like skills and actions to exist in
        self.bodyLayout = QGridLayout()
        # Add the skill, action, and speed layouts and give them each space
        self.bodyLayout.addLayout(self.skillLayout, 0, 0, -1, 2)
        self.bodyLayout.addLayout(self.actionLayout, 0, 3, -1, 4)
        self.bodyLayout.addLayout(self.speedLayout, 0, 7, -1, 2)
        # Add body layout to the form
        self.mid.addLayout(self.bodyLayout)

        # Add previously saved data if this is an edit
        if type == Interactions.EDIT:
            # Handle all numerical or text values
            self.cr.setValue(target["cr"])
            self.xp.setValue(target["xp"])
            self.maxHP.setText(target["hp"])
            self.ac.setValue(target["ac"])
            self.init.setValue(target["initiative"])
            self.notes.setPlainText(target["notes"])
            # Handle legendary markers
            if target["legendary"]:
                self.legend.setChecked(True)
                self.legend_res.setValue(target["legendary_resistances"])
            # Prefill dropdown menus that aren't in groups
            self.monSize.setCurrentIndex(target["size"] - 1)
            self.monType.setCurrentIndex(target["type"] - 1)
            self.align.setCurrentText(target["alignment"])
            # Prefill stat list and saves
            for st in range(6):
                self.statInputs[st].setValue(target["ability_scores"][st])
                if target["saves"][st] == 1:
                    savesGroup.button(st).setChecked(True)
                    self.saves[st] = 1
            # Prefill all other grouped categories
            # Speeds
            for i in range(len(target["speed"])):
                self.speedInputs[i].setValue(target["speed"][i])
            # Senses
            for i in range(len(target["senses"])):
                self.senseInputs[i].setValue(target["senses"][i])
            # Skills
            for i in range(len(target["skills"])):
                profInv = {val: key for key, val in profDict.items()}
                self.skillInputs[i].setCurrentText(profInv[target["skills"][i]])
            # Damage Types
            for i in range(len(target["damage_types"])):
                damageInv = {val: key for key, val in damageDict.items()}
                self.damageInputs[i].setCurrentText(damageInv[target["damage_types"][i]])
            # Preload actions and traits
            # Actions
            for name, data in target["actions"].items():
                self.addElement(ActionType.ACTION, name, data)
            # Traits
            for name, data in target["special_traits"].items():
                self.addElement(ActionType.TRAIT, name, data)
            # Legendary Actions
            for name, data in target["legendary_actions"].items():
                self.addElement(ActionType.LEG_ACTION, name, data)
            # Lair Actions
            for name, data in target["lair_actions"].items():
                self.addElement(ActionType.LAIR_ACTION, name, data)

    def onToggle(self, button, checked):
        # Add to the saves list if checked, remove if unchecked.
        if checked:
            self.saves[statDict[button.text()[0: -5]]] = 1
        else:
            self.saves[statDict[button.text()[0: -5]]] = 0

    def addElement(self, type, name=None, data=None):
        match type:
            case ActionType.ACTION:
                element = actionView(name=name, preload=data)
                self.actionList.append(element)
                self.actionBackdrop.addWidget(element)
            case ActionType.TRAIT:
                element = traitView(name=name, data=data)
                self.traitList.append(element)
                self.traitBackdrop.addWidget(element)
            case ActionType.LEG_ACTION:
                element = traitView(name=name, data=data)
                self.lActionList.append(element)
                self.legendBackdrop.addWidget(element)
            case ActionType.LAIR_ACTION:
                element = traitView(name=name, data=data)
                self.lairActions.append(element)
                self.lairBackdrop.addWidget(element)

    def hitpointPopup(self):
        hitpointDialog(self).exec()

    def confirmAction(self):
        speeds = [0 for i in range(5)]
        stats = [0 for i in range(6)]
        skills = [0 for i in range(18)]
        weakness = [0 for i in range(13)]
        senses = [0 for i in range(4)]
        action = {}
        traits = {}
        legend_action = {}
        lair_action = {}

        # Condense all stat spinboxes down into a single array.
        for i in range(len(self.statInputs)):
            stats[i] = self.statInputs[i].value()
        # Condense all skill inputs into a single array.
        for i in range(len(self.skillInputs)):
            skills[i] = profDict[self.skillInputs[i].currentText()]
        # Condense all damage type inputs into a single array.
        for i in range(len(self.damageInputs)):
            weakness[i] = damageDict[self.damageInputs[i].currentText()]
        # Condense all speed spinboxes down into a single array.
        for i in range(len(self.speedInputs)):
            speeds[i] = self.speedInputs[i].value()
        # Condense all sense spinboxes down into a single array.
        for i in range(len(self.senseInputs)):
            senses[i] = self.senseInputs[i].value()

        # Get the data from all actions listed and add it to the actions dictionary
        for act in self.actionList:
            name, data = act.toDict()
            if name != "":
                action[name] = data

        # Get the data from all special traits listed and add it to the actions dictionary
        for tr in self.traitList:
            name, data = tr.toDict()
            if name != "":
                traits[name] = data

        # Get the data from all legendary actions listed and add it to the actions dictionary
        for legend in self.lActionList:
            name, data = legend.toDict()
            if name != "":
                legend_action[name] = data

        # Get the data from all lair actions listed and add it to the actions dictionary
        for lair in self.lairActions:
            name, data = lair.toDict()
            if name != "":
                lair_action[name] = data

        match self.type:
            case Interactions.ADD:
                monsters.insert(
                    {
                        "name": self.name.text(),
                        "cr": self.cr.value(),
                        "xp": self.xp.value(),
                        "hp": self.maxHP.text(),
                        "ac": self.ac.value(),
                        "size": self.monSize.currentIndex() + 1,
                        "alignment": self.align.currentText(),
                        "initiative": self.init.value(),
                        "type": self.monType.currentIndex() + 1,
                        "speed": speeds,
                        "ability_scores": stats,
                        "saves": self.saves,
                        "skills": skills,
                        "senses": senses,
                        "damage_types": weakness,
                        "actions": action,
                        "special_traits": traits,
                        "legendary": True if self.legend.isChecked() else False,
                        "legendary_actions": legend_action,
                        "legendary_resistances": self.legend_res.value(),
                        "lair_actions": lair_action,
                        "notes": self.notes.toPlainText(),
                    }
                )
            case Interactions.EDIT:
                monsters.upsert(
                    Document(
                        {
                            "name": self.name.text(),
                            "cr": self.cr.value(),
                            "xp": self.xp.value(),
                            "hp": self.maxHP.text(),
                            "ac": self.ac.value(),
                            "size": self.monSize.currentIndex() + 1,
                            "alignment": self.align.currentText(),
                            "initiative": self.init.value(),
                            "type": self.monType.currentIndex() + 1,
                            "speed": speeds,
                            "ability_scores": stats,
                            "saves": self.saves,
                            "skills": skills,
                            "senses": senses,
                            "damage_types": weakness,
                            "actions": action,
                            "special_traits": traits,
                            "legendary": True if self.legend.isChecked() else False,
                            "legendary_actions": legend_action,
                            "legendary_resistances": self.legend_res.value(),
                            "lair_actions": lair_action,
                            "notes": self.notes.toPlainText(),
                        },
                        doc_id=self.target.doc_id,
                    )
                )
        self.source.populate()
        self.source.show()
        self.destruct()


"""
playerInteract: Interact with player characters in the database by either adding new
    entries or manipulating existing ones.
Constructor sets additional fields for data entry/deletion
Defines data entry, edit, and deletion methods.
"""
class playerInteract(dbInteract):
    def __init__(self, type, target=None, source=None):
        super().__init__(type, target, source)
        self.resize(1400, 1100)
        self.saves = [0 for i in range(6)]

        # Add hp, ac, alignment, and initiative to the head layout
        self.maxHP = QSpinBox()
        self.ac = QSpinBox(value=10)
        self.align = QComboBox()
        self.align.addItems(alignments)
        self.init = QSpinBox(value=0)
        self.head.addWidget(QLabel("Max HP"), 0, 2)
        self.head.addWidget(self.maxHP, 0, 3)
        self.head.addWidget(QLabel("Armor Class"), 0, 4)
        self.head.addWidget(self.ac, 0, 5)
        self.head.addWidget(QLabel("Alignment"), 1, 2)
        self.head.addWidget(self.align, 1, 3)
        self.head.addWidget(QLabel("Initiative"), 1, 4)
        self.head.addWidget(self.init, 1, 5)

        # Define and fill the layout with creature type, sepcies, size, and level
        self.typeLayout = QHBoxLayout()
        self.charClass = QPushButton("Enter Class")
        self.charClass.clicked.connect(self.classPopup)
        self.charSize = QComboBox()
        self.charSpec = QComboBox()
        self.classDict = {}
        # Pull data from reference tables to fill out pc sizes
        for s in sizes.all():
            self.charSize.addItem(s["size"])
        # Pull data from reference tables to fill out pc species
        for s in species.all():
            self.charSpec.addItem(s["name"])
        self.level = QSpinBox(value=0)
        self.typeLayout.addWidget(QLabel("Class(es): "))
        self.typeLayout.addWidget(self.charClass)
        self.typeLayout.addWidget(QLabel("Species: "))
        self.typeLayout.addWidget(self.charSpec)
        self.typeLayout.addWidget(QLabel("Size: "))
        self.typeLayout.addWidget(self.charSize)
        self.typeLayout.addWidget(QLabel("Total Level: "))
        self.typeLayout.addWidget(self.level)
        # Add the layout to the main mid layout
        self.mid.addLayout(self.typeLayout)

        # Define and fill the layout with stats and saving throw proficiencies
        self.statLayout = QGridLayout()
        self.inPary = []
        self.statInputs = []
        count = 0
        for stat in statDict.keys():
            self.statLayout.addWidget(QLabel(stat + ": "), 0, 2 * count)
            self.statInputs.append(QSpinBox(value=10))
            self.statLayout.addWidget(self.statInputs[count], 0, 2 * count + 1)
            count += 1
        # Create a button group with all stats for saving throws
        savesGroup = QButtonGroup(self)
        savesGroup.setExclusive(False)
        savesGroup.buttonToggled.connect(self.onToggle)
        count = 0
        for s in statDict.keys():
            checkBox = QCheckBox(s + " Save")
            self.statLayout.addWidget(checkBox, 1, 2 * count, 2, 1)
            savesGroup.addButton(checkBox, statDict[s])
            count += 1
        # Add the layout to the main mid layout
        self.mid.addLayout(self.statLayout)

        # Define and fill the layout containing skills and legendary checks
        self.skillLayout = QGridLayout()
        # Create a dropdown box for every skill and add it to the layout
        count = 0
        self.skillInputs = []
        for sk in skills.all():
            self.skillInputs.append(QComboBox())
            self.skillInputs[count].addItems(profDict.keys())
            self.skillLayout.addWidget(QLabel(sk["skill"]), count, 0)
            self.skillLayout.addWidget(self.skillInputs[count], count, 1)
            count += 1
        # Create and add entries for legendary tags and legendary resistances
        self.jackOfTrades = QRadioButton("Jack of all trades")
        self.skillLayout.addWidget(self.jackOfTrades, count, 0, 1, 2)

        # Define and fill the layout containing resistances and actions
        self.infoLayout = QGridLayout()

        self.infoLayout.addWidget(QLabel("Weaknesses/Resistances"), 0, 0, 1, -1)
        countDa = 0
        self.damageInputs = []
        for dmg in damageType:
            self.damageInputs.append(QComboBox())
            self.damageInputs[countDa].addItems(damageDict.keys())
            self.infoLayout.addWidget(QLabel(dmg), countDa + 1, 0)
            self.infoLayout.addWidget(self.damageInputs[countDa], countDa + 1, 1)
            countDa += 1

        # Create an area for notes
        self.notes = QTextEdit()
        self.notes.setMaximumHeight(40)
        self.infoLayout.addWidget(QLabel("Additional Notes:"), countDa + 2, 0)
        self.infoLayout.addWidget(self.notes, countDa + 3, 0, 1, -1)

        # Define and fill the layout containing speeds and sesnses
        self.speedLayout = QGridLayout()

        self.speedLayout.addWidget(QLabel("Movement Speeds"), 0, 0, 1, 2)
        countSp = 0
        self.speedInputs = []
        for sp in movements:
            self.speedInputs.append(QSpinBox(value=30 if countSp == 0 else 0))
            self.speedLayout.addWidget(QLabel(sp), countSp + 1, 0)
            self.speedLayout.addWidget(self.speedInputs[countSp], countSp + 1, 1)
            countSp += 1

        self.speedLayout.addWidget(QLabel("Senses"), countSp + 2, 0, 1, 2)
        countSe = 0
        self.senseInputs = []
        for se in senses.all():
            self.senseInputs.append(QSpinBox())
            self.speedLayout.addWidget(QLabel(se["sense"]), countSe + countSp + 3, 0)
            self.speedLayout.addWidget(self.senseInputs[countSe], countSe + countSp + 3, 1)
            countSe += 1

        # Create a shell for the body elements like skills and actions to exist in
        self.bodyLayout = QGridLayout()
        # Add the skill, action, and speed layouts and give them each space
        self.bodyLayout.addLayout(self.skillLayout, 0, 0, -1, 2)
        self.bodyLayout.addLayout(self.infoLayout, 0, 3, -1, 4)
        self.bodyLayout.addLayout(self.speedLayout, 0, 7, -1, 2)
        # Add body layout to the form
        self.mid.addLayout(self.bodyLayout)

        # Add previously saved data if this is an edit
        if type == Interactions.EDIT:
            self.inPary = target["inparty"]
            # Handle all numerical or text values
            self.level.setValue(target["level"])
            self.maxHP.setValue(target["hp"])
            self.ac.setValue(target["ac"])
            self.init.setValue(target["initiative"])
            self.notes.setPlainText(target["notes"])
            # Handle true/false markers
            if target["jack_of_trades"]:
                self.jackOfTrades.setChecked(True)
            # Prefill dropdown menus that aren't in groups
            self.charSize.setCurrentIndex(target["size"] - 1)
            self.charSpec.setCurrentIndex(target["species"] - 1)
            self.align.setCurrentText(target["alignment"])
            # Prefill stat list and saves
            for st in range(6):
                self.statInputs[st].setValue(target["ability_scores"][st])
                if target["saves"][st] == 1:
                    savesGroup.button(st).setChecked(True)
                    self.saves[st] = 1
            # Prefill Character Classes
            classStr = ""
            for k, v in target["class"].items():
                self.classDict[k] = v
                classStr += f"{k} {v}, "
            self.charClass.setText(classStr[0: -2])
            # Prefill all other grouped categories
            # Speeds
            for i in range(len(target["speed"])):
                self.speedInputs[i].setValue(target["speed"][i])
            # Senses
            for i in range(len(target["senses"])):
                self.senseInputs[i].setValue(target["senses"][i])
            # Skills
            for i in range(len(target["skills"])):
                profInv = {val: key for key, val in profDict.items()}
                self.skillInputs[i].setCurrentText(profInv[target["skills"][i]])
            # Damage Types
            for i in range(len(target["damage_types"])):
                damageInv = {val: key for key, val in damageDict.items()}
                self.damageInputs[i].setCurrentText(damageInv[target["damage_types"][i]])

    def onToggle(self, button, checked):
        # Add to the saves list if checked, remove if unchecked.
        if checked:
            self.saves[statDict[button.text()[0: -5]]] = 1
        else:
            self.saves[statDict[button.text()[0: -5]]] = 0

    def classPopup(self):
        classDialog(self).exec()

    def confirmAction(self):
        speeds = [0 for i in range(5)]
        stats = [0 for i in range(6)]
        skills = [0 for i in range(18)]
        weakness = [0 for i in range(13)]
        senses = [0 for i in range(4)]

        # Condense all stat spinboxes down into a single array.
        for i in range(len(self.statInputs)):
            stats[i] = self.statInputs[i].value()
        # Condense all skill inputs into a single array.
        for i in range(len(self.skillInputs)):
            skills[i] = profDict[self.skillInputs[i].currentText()]
        # Condense all damage type inputs into a single array.
        for i in range(len(self.damageInputs)):
            weakness[i] = damageDict[self.damageInputs[i].currentText()]
        # Condense all speed spinboxes down into a single array.
        for i in range(len(self.speedInputs)):
            speeds[i] = self.speedInputs[i].value()
        # Condense all sense spinboxes down into a single array.
        for i in range(len(self.senseInputs)):
            senses[i] = self.senseInputs[i].value()

        match self.type:
            case Interactions.ADD:
                players.insert(
                    {
                        "name": self.name.text(),
                        "level": self.level.value(),
                        "class": self.classDict,
                        "hp": self.maxHP.value(),
                        "ac": self.ac.value(),
                        "size": self.charSize.currentIndex() + 1,
                        "alignment": self.align.currentText(),
                        "initiative": self.init.value(),
                        "species": self.charSpec.currentIndex() + 1,
                        "speed": speeds,
                        "ability_scores": stats,
                        "saves": self.saves,
                        "skills": skills,
                        "jack_of_trades": (
                            True if self.jackOfTrades.isChecked() else False
                        ),
                        "senses": senses,
                        "damage_types": weakness,
                        "notes": self.notes.toPlainText(),
                        "inparty": self.inPary,
                    }
                )
            case Interactions.EDIT:
                players.upsert(Document(
                    {
                        "name": self.name.text(),
                        "level": self.level.value(),
                        "class": self.classDict,
                        "hp": self.maxHP.value(),
                        "ac": self.ac.value(),
                        "size": self.charSize.currentIndex() + 1,
                        "alignment": self.align.currentText(),
                        "initiative": self.init.value(),
                        "species": self.charSpec.currentIndex() + 1,
                        "speed": speeds,
                        "ability_scores": stats,
                        "saves": self.saves,
                        "skills": skills,
                        "jack_of_trades": True if self.jackOfTrades.isChecked() else False,
                        "senses": senses,
                        "damage_types": weakness,
                        "notes": self.notes.toPlainText(),
                        "inparty": self.inPary
                    }, doc_id=self.target.doc_id))
        self.source.populate()
        self.source.show()
        self.destruct()


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
        self.sizes = []

        # Create a label for the size field and add it to body
        sizeLabel = QLabel("Creature size:")
        self.mid.addWidget(sizeLabel)

        # Create a button group with all known creature sizes
        sizesGroup = QButtonGroup(self)
        sizesGroup.setExclusive(False)
        sizesGroup.buttonToggled.connect(self.onToggle)
        # Populate the group with data from the sizes table
        for s in sizes.all():
            checkBox = QCheckBox(s["size"])
            self.mid.addWidget(checkBox)
            sizesGroup.addButton(checkBox, id=s.doc_id)

        # Create a field and label for the default walking speed
        speedLabel = QLabel("Walking speed:")
        self.mid.addWidget(speedLabel)
        self.speed = QSpinBox()
        self.mid.addWidget(self.speed)

        # Add previously saved data to the form if this is an edit
        if type == Interactions.EDIT:
            Size = Query()
            for s in target["size"]:
                s_id = sizes.search(Size.size == s)[0].doc_id
                if sizesGroup.button(s_id):
                    sizesGroup.button(s_id).setChecked(True)
            self.speed.setValue(int(target["speed"]))

    def onToggle(self, button, checked):
        if checked:
            self.sizes.append(button.text())
        else:
            self.sizes.remove(button.text())

    def confirmAction(self):
        match self.type:
            case Interactions.ADD:
                species.insert({"name": self.name.text(), "size": self.sizes, "speed": self.speed.text()})
            case Interactions.EDIT:
                species.upsert(Document({"name": self.name.text(), "size": self.sizes, "speed": self.speed.text()},
                              doc_id=self.target.doc_id))
        self.source.populate()
        self.source.show()
        self.destruct()


"""
classInteract: Interact with player classes in the database by either adding new
    entries or manipulating existing ones.
Constructor sets additional fields for data entry/deletion
Defines data entry, edit, and deletion methods.
"""
class classInteract(dbInteract):
    def __init__(self, type, target=None, source=None):
        super().__init__(type, target, source)
        self.saves = []

        # Create a field and label for the hit die
        hdLabel = QLabel("Hit die:")
        self.mid.addWidget(hdLabel)
        self.hd = QComboBox()
        self.hd.addItems(["d4", "d6", "d8", "d10", "d12"])
        self.mid.addWidget(self.hd)

        # Create a label for the saving throws
        savesLabel = QLabel("Saving throw proficiencies:")
        self.mid.addWidget(savesLabel)

        # Create a button group with all stats for saving throws
        savesGroup = QButtonGroup(self)
        savesGroup.setExclusive(False)
        savesGroup.buttonToggled.connect(self.onToggle)
        for s in statDict.keys():
            checkBox = QCheckBox(s)
            self.mid.addWidget(checkBox)
            savesGroup.addButton(checkBox, statDict[s])

        # Add previously saved data if this is an edit
        if type == Interactions.EDIT:
            for s in target["saving-throws"]:
                s_id = statDict[s]
                if savesGroup.button(s_id):
                    savesGroup.button(s_id).setChecked(True)
            self.hd.setCurrentText(target["hit-die"])

    def onToggle(self, button, checked):
        # Add to the saves list if checked, remove if unchecked.
        if checked:
            self.saves.append(button.text())
        else:
            self.saves.remove(button.text())

    def confirmAction(self):
        match self.type:
            case Interactions.ADD:
                classes.insert({"name": self.name.text(), "hit-die": self.hd.currentText(), "saving-throws": self.saves})
            case Interactions.EDIT:
                classes.upsert(Document({"name": self.name.text(), "hit-die": self.hd.currentText(), "saving-throws": self.saves},
                              doc_id=self.target.doc_id))
        self.source.populate()
        self.source.show()
        self.destruct()


"""
monsterTypeInteract: Interact with monster types in the database by either adding new
    entries or manipulating existing ones.
Constructor sets additional fields for data entry/deletion
Defines data entry, edit, and deletion methods.
"""
class monsterTypeInteract(dbInteract):
    def __init__(self, type, target=None, source=None):
        super().__init__(type, target, source)

        descLabel = QLabel("Description:")
        self.mid.addWidget(descLabel)
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
        self.destruct()


"""
conditionsInteract: Interact with conditions in the database by either adding new
    entries or manipulating existing ones.
Constructor sets additional fields for data entry/deletion
Defines data entry, edit, and deletion methods.
"""
class conditionInteract(dbInteract):
    def __init__(self, type, target=None, source=None):
        super().__init__(type, target, source)

        self.mid.setParent(None)
        # Create a widget to house effects
        self.effectArea = Color("#F1E9D2")
        self.effectArea.setLayout(self.mid)
        # Define the scrollable area in the center of the menu for multiple effects.
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.effectArea)
        self.layout.addWidget(self.scroll, 1, 0)

        effectLabel = QLabel("Condition Effects:")
        self.mid.addWidget(effectLabel)

        if type == Interactions.EDIT:
            for e in target["effects"]:
                effect = QLineEdit(e)
                self.mid.addWidget(effect)
        else:
            self.mid.addWidget(QLineEdit())

        self.additionalEffect = QPushButton("Add New Effect")
        self.additionalEffect.clicked.connect(self.addEffect)
        self.foot.addWidget(self.additionalEffect, 1, 0)

    def addEffect(self):
        self.mid.addWidget(QLineEdit())

    def confirmAction(self):
        effects = []
        # Adds all non-blank effects to a list for inserting.
        while self.mid.itemAt(0) != None:
            w = self.mid.itemAt(0).wid
            # If this is one of the main tables, clear mini views.
            if w.__class__.__name__ == "QLineEdit" and w.text() != "":
                effects.append(w.text())
            # Clean up the attached widget
            w.setParent(None)
            self.mid.removeWidget(w)
            w.deleteLater()

        match self.type:
            case Interactions.ADD:
                conditions.insert({"name": self.name.text(), "effects": effects})
            case Interactions.EDIT:
                conditions.upsert(Document({"name": self.name.text(), "effects": effects},
                              doc_id=self.target.doc_id))
        self.source.populate()
        self.source.show()
        self.destruct()
