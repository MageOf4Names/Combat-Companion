import re
import math
import random as rd
from tinydb import TinyDB, Query

players = TinyDB("TestDatabases/players.json").table("player_characters")
monsters = TinyDB("TestDatabases/monsters.json").table("monsters")
types = TinyDB("TestDatabases/type.json").table("monster_types")
classes = TinyDB("TestDatabases/class.json").table("player_classes")
species = TinyDB("TestDatabases/species.json").table("species")
conditions = TinyDB("TestDatabases/condition.json").table("conditions")
parties = TinyDB("TestDatabases/party.json").table("parties")
refs = TinyDB("TestDatabases/reference.json")
senses = refs.table("senses")
sizes = refs.table("sizes")
skills = refs.table("skills")

encounterXP = 0

# List of all valid damage types in dnd 5e and 2024 edition
damageType = [
    "Piercing",
    "Bludgeoning",
    "Slashing",
    "Cold",
    "Fire",
    "Lightning",
    "Thunder",
    "Poison",
    "Acid",
    "Necrotic",
    "Radiant",
    "Force",
    "Psychic",
]

# List of all valid alignments in dnd 5e and 2024 edition
alignments = [
    "Unaligned",
    "Lawful Good",
    "Lawful Neutral",
    "Lawful Evil",
    "Neutral Good",
    "True Neutral",
    "Neutral Evil",
    "Chaotic Good",
    "Chaotic Neutral",
    "Chaotic Evil",
]

# Dictionary for translating stat names into list order
statDict = {
    "Strength": 0,
    "Dexterity": 1,
    "Constitution": 2,
    "Intelligence": 3,
    "Wisdom": 4,
    "Charisma": 5,
}

# Takes in a player level or creature CR and outputs the corresponding proviciency modifier.
def profByLevel(level):
    return 2 + int((level - 1) / 4)


# Takes in an ability score and returns the associated bonus score
def getBonus(score):
    return math.floor((score - 10) / 2)


"""
rollDice takes in a string expression representing a series of dice and randomizes a total in that range
stmt: A string representing the dice expression
hasAvg: Boolean value determining if an expression has a predetermined average value
rollAvg: Boolean value representing if the average value was requested or not
Returns: An integer representing the value of the expression
"""
def rollDice(stmt, hasAvg=True, rollAvg=False):
    # Cleans the statement of any unexpected characters
    stmt = re.sub(r"[^d0-9+:]", "", stmt.lower())
    total = 0  # Total number rolled

    # Special case for expressions that have an average value (Expressed before dice with a colon)
    if hasAvg:
        # Splits the average value (behind the colon) from the dice expression
        splitAvg = stmt.split(":")
        # Returns the average if requested
        if rollAvg:
            return int(splitAvg[0])
        # Otherwise, reassigns stmt to conform with the rest of the method
        stmt = splitAvg[1]

    # Splits the statement across additions of different dice values
    dice = stmt.split("+")
    for d in dice:
        # Checks for a dice value, if none, add the term directly
        if "d" in d:
            # Splits term into dice quantity and value
            die = d.split("d")
            # If no quantity of dice was given, assume 1
            if die[0] == "":
                die[0] = "1"
            for i in range(int(die[0])):
                total += rd.randint(1, int(die[1]))
        else:
            total += int(d)
    return total
