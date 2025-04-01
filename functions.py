import re
import random as rd

# Takes in a player level or creature CR and outputs the corresponding proviciency modifier.
def profByLevel(level):
    return 2 + int((level - 1) / 4)



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
