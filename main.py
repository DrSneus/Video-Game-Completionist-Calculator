# Samuel Neus
# Main Function

# Libraries
import hltbscraper
import steamscraper
import calculator

# Functions

# Given a game's app id, will find and return a dictionary of different average completion lengths
def main():
    # Defining variables
    print("Please provide the name of a game:")
    game = input()

    # ID finding
    steamID = steamscraper.findSteamAppID(game)
    hltbID = hltbscraper.findHLTBAppID(game)

    # Data finding
    percentList = steamscraper.findPercents(steamID)

    if hltbID:
        lengthDict = hltbscraper.findLength(hltbID)
    else:
        print(f"The title \'{game}\' could not be found on How Long To Beat")
        return None

    # Results
    calculator.tableMaker(lengthDict, percentList)

# Main Execution
if __name__ == '__main__':
    main()
