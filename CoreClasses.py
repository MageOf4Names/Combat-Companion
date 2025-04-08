"""
File:
Brief:
Description :
Author: Brandon Dennis
Version: 0.0.0
Last updated: 4/3/2025
TODO:
"""

from HelperFunctions import *
from ErrorClasses import *

class Encounter:
    # Expected format for a combatant entry:
    # [Monster_Flag, combatant data, initiative score, current_hp, max_hp]
    def __init__(self, entries):
        # Build objects for each combatant in the encounter
        combatants = []
        for c in entries:
            if c[0]: combatants.append(Monster(c[1]. c[2], c[3], c[4]))
            else: combatants.append(Player(c[1], c[2], c[3]))
        # Sort by initiative value (highest value first)
        self.combatants = sorted(combatants, key=lambda combatant: combatant.init, reverse=True)
        # Assign highest initiative to the current focus and 
        self.currentIndex = 0
        self.current = self.combatants[0]

"""
Combatant class is a general template for all monsters and players in combat
Contains shared attributes like Armor Class, Maximum HP, and Notes
Methods serve to manipulate data that is not permanently saved in the database
"""
class Combatant:
    def __init__(self, source, init, currentHP):
        # Permanent values assigned from the database entry
        self.index = source.doc_id
        self.name = source["name"]
        self.ac = source['ac']
        self.size = source['size']
        self.alignment = source['alignment']
        self.languages = source['languages']
        self.speed = source['speed']
        self.stats = source['ability_scores']
        self.saves = source['saves']
        self.skillProf = source['skills']
        self.senses = source['senses']
        self.damages = source['damage_types']
        self.notes = source['notes']
        # Temporary values assigned during combat
        self.init = init + source['ability_scores'][1] / 100 # Add dex score at the end to help sort ties.
        self.tempHP = 0
        self.conditions = []
        self.concentration = False
        self.conscious = True
        # Set HP stats to zero as a baseline (overridden later)
        self.maxHP = 0
        self.currentHP = currentHP
        self.proficiency = 1

    """
    setCurrentHP takes in an expression and adjusts a combatant's currentHP attribute to match
    val: String representing the expression
    """
    def setCurrentHP(self, val):
        # Trim all unexpected characters from the string
        val = re.sub(r"[^0-9+-]", '', val)
        # Check if user wants to add to the current hp (and ensures hp isn't over max)
        if val[0] == '+' and '+' not in val[1:]:
            self.currentHP += int(val[1:])
            if self.currentHP > self.maxHP: self.currentHP = self.maxHP
        # Check if user wants to subtract from current hp (and checks for unconsciousness)
        elif val[0] == '-' and '-' not in val[1:]:
            self.currentHP -= int(val[1:])
            if self.currentHP <= 0:
                self.currentHP = 0
                self.conscious = False
        # Check to see if the expression only contains digits
        elif '+' not in val and '-' not in val:
            self.currentHP = int(val)
        # Raises an exception if the expression contains extra characters
        else:
            raise UnexpectedSyntax
 
    """
    updateTempHP takes in an expression and adjusts a combatant's tempHP attribute to match
    val: String representing the expression
    """
    def updateTempHP(self, val):
        # Trim all unexpected characters from the string
        val = re.sub(r"[^0-9+-]", '', val)
        # Check if user wants to add to the current hp (and ensures hp isn't over max)
        if val[0] == '+' and '+' not in val[1:]:
            self.tempHP += int(val[1:])
        # Check if user wants to subtract from current hp (and checks for unconsciousness)
        elif val[0] == '-' and '-' not in val[1:]:
            self.tempHP -= int(val[1:])
            if self.tempHP <= 0:
                self.tempHP = 0
        # Check to see if the expression only contains digits
        elif '+' not in val and '-' not in val:
            self.tempHP = int(val)
        # Raises an exception if the expression contains extra characters
        else:
            raise UnexpectedSyntax

    # Sets maximum HP to a set value temporarily (Doesn't save to database)
    def setMaxHP(self, newMax):
        self.maxHP = newMax

    # Rolls a saving throw for the given stat.
    def rollSave(self, stat):
        # Builds a statement for rolling a d20 + ability modifier
        stmt = "d20+" + str(getBonus(self.stats[statDict[stat]]))
        if self.saves[statDict[stat]] == 1:
            stmt += str(self.proficiency)
        return rollDice(stmt)

    # Rolls a skill check using the name of the skill.
    def rollSkill(self, skillName):
        # Looks for the requested skill in reference database
        lookup = Query()
        skill = skills.search(lookup.skill == skillName)[0]
        # Finds the proper list in the ability array
        stat = statDict[skill['stat']]
        # Builds the rolling statement for d20 + ability modifier
        stmt = "d20+" + str(getBonus(self.stats[stat]))
        match self.skillProf[skill.doc_id]:
            case 1:
                stmt += "+" + str(self.proficiency)
            case 2:
                stmt += "+" + str(self.proficiency * 2)
        return rollDice(stmt)

    # Updates the notes field for the given combatant.
    def updateNotes(self, txt):
        self.notes = txt
    
    # Updates the initiative attribute.
    def updateInit(self, newInit):
        self.init = newInit + self.stats[1] / 100 # Add dex score at the end to help sort ties.

    # Updates the concentration field to represent if the combatant is concentration or not
    def updateConcentrate(self, con):
        self.concentration = con

    # Adds a condition to the combatant's list
    def addCondition(self, cond):
        self.conditions.append(cond)

    # Removes a condition from the combatant's list
    def removeCondition(self, cond):
        self.conditions.remove(cond)

"""
Player class is used for player characters in initiative order
Contains player-specific stats like species, class, and death saves
"""
class Player(Combatant):
    def __init__(self, pc, init, currentHP):
        # Set all shared values through the super method
        super().__init__(pc, init, currentHP)
        # Set values unique to a player character
        self.level = pc['level']
        self.playerClass = pc['class']
        self.species = pc['species']
        self.currentHP = self.maxHP
        self.deathSaves = [0, 0]
        # Override default values
        self.maxHP = pc['hp']
        self.proficiency = profByLevel(self.level)

    # Handles death saves either by inserted value or by rolling dice
    def deathSave(self, val, roll=True):
        if roll:
            val = rollDice("d20")
        if val >= 10:
            self.deathSave[1] += 1
        else:
            self.deathSave[0] += 1


"""
Monster class is used for monster combatants in initiative
Contains monster-specific stats like their Challenge Rating, XP gained, and legendary status
"""
class Monster(Combatant):
    def __init__(self, monst, init, currentHP, maxHP):
        # Set all shared values through the super method
        super().__init__(monst, init, currentHP)
        # Set values unique to a monster
        self.cr = monst["cr"]
        self.xp = monst["xp"]
        self.type = monst["type"]
        self.actions = monst["actions"]
        self.traits = monst["special_traits"]
        self.legend = monst["legendary"]
        self.lAct = monst["legendary_actions"]
        self.lRes = monst["legendary_resistances"]
        self.lair = monst["lair_actions"]
        # Override default values
        self.maxHP = maxHP
        self.proficiency = profByLevel(self.cr)

    # Overrides default method to add xp to encounter when monster is defeated.
    def setCurrentHP(self, val):
        super().setCurrentHP(val)
        if self.conscious == False:
            encounterXP += self.xp
