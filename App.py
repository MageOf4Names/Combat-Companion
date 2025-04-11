"""
File: App.py
Brief: Main executable file for the Combat Companion app.
Description: 
Author: Brandon Dennis
Version: 0.0.0
Last updated: 4/10/2025
TODO: 
"""

from CoreClasses import *
from GUIElements import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Sets default window name and size
        self.setWindowTitle("Combat Companion")
        self.resize(QSize(1600, 900))
        # Creates and assigns pages for each database view
        self.monsterDB = monsterView()
        self.playerDB = playerView()
        self.partyDB = partyView()
        self.speciesDB = speciesView()
        self.classDB = classView()
        self.typeDB = monsterTypeView()
        self.conditionDB = conditionView()

        layout = QVBoxLayout()

        # Creates an action for the monsters database to be added to the menu
        monsterAction = QAction("Monsters", self)
        monsterAction.setStatusTip("View the monsters database")
        monsterAction.triggered.connect(lambda: self.routeDatabase(self.monsterDB))
        monsterAction.setShortcut(QKeySequence("Ctrl+Shift+m"))

        # Creates an action for the player character database to be added to the menu
        playerAction = QAction("Players", self)
        playerAction.setStatusTip("View the players database")
        playerAction.triggered.connect(lambda: self.routeDatabase(self.playerDB))
        playerAction.setShortcut(QKeySequence("Ctrl+Shift+c"))

        # Creates an action for the parties database to be added to the menu
        partyAction = QAction("Parties", self)
        partyAction.setStatusTip("View the parties database")
        partyAction.triggered.connect(lambda: self.routeDatabase(self.partyDB))
        partyAction.setShortcut(QKeySequence("Ctrl+Shift+p"))

        # Creates an action for the species database to be added to the menu
        speciesAction = QAction("Species", self)
        speciesAction.setStatusTip("View the species database")
        speciesAction.triggered.connect(lambda: self.routeDatabase(self.speciesDB))

        # Creates an action for the player classes database to be added to the menu
        classAction = QAction("Classes", self)
        classAction.setStatusTip("View the classes database")
        classAction.triggered.connect(lambda: self.routeDatabase(self.classDB))

        # Creates an action for the monster types database to be added to the menu
        typeAction = QAction("Monster Types", self)
        typeAction.setStatusTip("View the monster types database")
        typeAction.triggered.connect(lambda: self.routeDatabase(self.typeDB))

        # Creates an action for the conditions database to be added to the menu
        condAction = QAction("Conditions", self)
        condAction.setStatusTip("View the conditions database")
        condAction.triggered.connect(lambda: self.routeDatabase(self.conditionDB))

        menu = self.menuBar()
        # Creates the portion of the menu for monsters
        monsterMenu = menu.addMenu("&Monsters")
        monsterMenu.addAction(monsterAction)

        # Creates the portion of the menu having to do with PCs
        playerMenu = menu.addMenu("&Player Characters")
        playerMenu.addAction(playerAction)
        playerMenu.addSeparator()
        playerMenu.addAction(partyAction)

        # Creates the portion of the menu for various lookup databases
        lookupMenu = menu.addMenu("&Other Databases")
        lookupMenu.addAction(speciesAction)
        lookupMenu.addSeparator()
        lookupMenu.addAction(classAction)
        lookupMenu.addSeparator()
        lookupMenu.addAction(typeAction)
        lookupMenu.addSeparator()
        lookupMenu.addAction(condAction)

        name = QLabel()
        name.setText("Welcome to the Combat Companion!")
        name.setAlignment(Qt.AlignCenter)
        name.setFont(openFont)

        start = QPushButton()
        start.setText("Build an encounter")

        layout.addWidget(name)
        layout.addWidget(start)

        background = QLabel()
        background.setPixmap(QPixmap("images/background.png"))
        background.setScaledContents(True)
        background.setLayout(layout)

        self.setCentralWidget(background)

    def routeDatabase(self, dest):
        if dest.isVisible():
            dest.hide()
        else:
            dest.show()
    
    def closeEvent(self, action):
        self.monsterDB.close()
        self.playerDB.close()
        self.partyDB.close()
        self.speciesDB.close()
        self.classDB.close()
        self.typeDB.close()
        self.conditionDB.close()
        super().closeEvent(action)

app = QApplication()
app.setStyle("windowsvista")

window = MainWindow()
window.show()

# Start the app on the main screen
app.exec()
