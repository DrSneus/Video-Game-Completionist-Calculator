# Samuel Neus
# Functions used for calculating a game's "difficulty" for completion

# Functions

# Requires the dictionary from findLength() and the list from findPercentages()
# Outputs a score out of 100
def calculator(lengthDict, percentList):
    score = 0
    
    # Checks if there is a valid time
    if lengthDict == None:
        return None
    elif lengthDict["Completionist"]["Time"] == None:
        return None

    # Adjusts the time value
    if lengthDict["Completionist"]["Format"] == "Hours":
        score = lengthDict["Completionist"]["Time"] * 60
    else:
        score = lengthDict["Completionist"]["Time"]

    # Adds in the score for achievements
    if percentList != None:
        multiplier = 100 / (sum(percentList) / len(percentList))

        # 30000 was chosen after testing to match up with desired scores for certain games
        score = int((100 * score * multiplier) / 30000)
    else:
        # 7500 was chosen to account for the difference in games without achievements
        score = int((100 * score) / 7500)

     
    

    # Some games can go way over 100, but the calculator gets more difficult to use at higher levels
    if score > 100: 
        return 101
    else:
        return int(score)
