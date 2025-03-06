# Takes in a player level or creature CR and outputs the corresponding proviciency modifier.
def profByLevel(level):
    return 2 + int((level - 1) / 4)
