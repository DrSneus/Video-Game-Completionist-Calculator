# Samuel Neus
# Functions used for calculating a game's statistics

# Functions

# Requires the dictionary from findLength() and the list from findPercentages()
# Outputs a further description of the results gathered
# Helpful for a more advanced understanding
import restart


def descriptionMaker(lengthDict, percentList, isGUI=False):
    # Checks if there is a valid time
    if lengthDict is None:
        return None

    display = ""
    # Calculating and printing length-statistics
    if "Completionists" in lengthDict:
        time = (lengthDict["Completionists"] - lengthDict["Main Story"])

        # Time formatting
        if time < 60:
            time_format = "minutes"
        elif time == 60:
            time /= 60
            time_format = "hour"
        else:
            time /= 60
            time_format = "hours"
        display = '\n'.join([display,
                             f"The time difference between an normal playthrough and a completionist one is "
                             f"{int(time)} {time_format}"])

    # Calculating and printing difficulty-statistics
    if percentList is None:
        display = '\n'.join([display, "There are no achievements for this title on Steam!\n"])
        restart.restart()

        if not isGUI:
            print(display)
            return None
        else:
            return display

    hard_Achievements = [percents for percents in percentList if percents < 3]
    impossible_Achievements = [percents for percents in percentList if percents < 1]

    # Finds the challenging achievements
    if len(hard_Achievements) == 0:
        display = '\n'.join([display, "There are no achievements considered challenging for this title"])
    elif len(hard_Achievements) <= 5:
        display = '\n'.join([display, "There are few achievements considered challenging for this title"])
    else:
        display = '\n'.join([display, f"There are at least {len(hard_Achievements)} achievements that are considered "
                                      f"challenging"])

    # Finds the really challenging achievements
    if len(impossible_Achievements) == 1:
        display = '\n'.join([display, "Of those, there is 1 achievement considered extremely difficult"])
    elif len(impossible_Achievements) > 1:
        display = '\n'.join([display, f"Of those, there are {len(impossible_Achievements)} achievements considered "
                                      f"extremely difficult"])

    restart.restart()

    if not isGUI:
        print(display)
    else:
        return display


# Requires the dictionary from findLength() and the list from findPercentages()
# Outputs a rating for the lengths and overall difficulty
def tableMaker(lengthDict, percentList, isGUI=False):
    # Checks if there is a valid time
    if lengthDict is None:
        return None

    display = ""

    # Time scores
    completionistLengthScore = None
    display = '\n'.join([display, "Game Length"])
    display = '\n'.join([display, "-----------"])
    for category in lengthDict:
        # Adjusts the time value
        time = lengthDict[category] / 60

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
            if category == "Completionists":
                completionistLengthScore = lengthScore

            # Prints results
            display = '\n'.join([display, f"{category} Length Score = {lengthScore}"])
    display = '\n'.join([display, "\n"])

    # Checks if there are valid achievements
    if percentList is None:
        if not isGUI:
            print(display)
            return None
        else:
            return display

    # Determines a difficulty score
    difficultyScore = 0
    display = '\n'.join([display, "Game Difficulty"])
    display = '\n'.join([display, "---------------"])
    for achievement in percentList:
        if achievement > 60:
            difficultyScore += 1
        elif achievement > 30:
            difficultyScore += 2
        elif achievement > 10:
            difficultyScore += 3
        elif achievement > 3:
            difficultyScore += 4
        else:
            difficultyScore += 5

    difficultyScore = int(difficultyScore / len(percentList))
    display = '\n'.join([display, f"Achievement Difficulty = {difficultyScore}"])

    if completionistLengthScore:
        completionistScore = (difficultyScore + (1.5 * completionistLengthScore)) / 2

        if completionistScore > 5:
            completionistScore = 5

        display = '\n'.join([display, f"Completionist Difficulty = {completionistScore}"])
    display = '\n'.join([display, "\n"])

    # Printing
    if not isGUI:
        print(display)
    else:
        return display
