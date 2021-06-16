# Samuel Neus
# Functions used for calculating a game's statistics

# Functions

# Requires the dictionary from findLength() and the list from findPercentages()
# Outputs a rating for the lengths and overall difficulty
def tableMaker(lengthDict, percentList):
    # Checks if there is a valid time
    if lengthDict == None:
        return None

    completionistLengthScore = None
    for category in lengthDict:
        # Adjusts the time value
        if lengthDict[category]["Format"] == "Minutes":
            time = lengthDict[category]["Time"] / 60
        else:
            time = lengthDict[category]["Time"]

        # Determines a length score
        if time:
            if time <= 4:
                lengthScore = 1
            elif time <= 15:
                lengthScore = 2
            elif time <= 45:
                lengthScore = 3
            elif time <= 100:
                lengthScore = 4
            else:
                lengthScore = 5

            # Saves the Completionist category data
            if category == "Completionist":
                completionistLengthScore = lengthScore

            # Prints results
            print(f"{category} Length Score = {lengthScore}")

    # Checks if there are valid achievements
    if percentList == None:
        return None

    # Determines a difficulty score
    difficultyScore = 0
    for achiev in percentList:
        if achiev > 60:
            difficultyScore += 1
        elif achiev > 30:
            difficultyScore += 2
        elif achiev > 10:
            difficultyScore += 3
        elif achiev > 3:
            difficultyScore += 4
        else:
            difficultyScore += 5

    difficultyScore = int(difficultyScore / len(percentList))
    print(f"\nAchievement Difficulty = {difficultyScore}")

    if completionistLengthScore:
        completionistScore = (difficultyScore + (1.5*completionistLengthScore))/2

        if completionistScore > 5:
            completionistScore = 5

        print(f"\nCompletionist Difficulty = {completionistScore}")
    
    