# Samuel Neus
# Main Function

# Libraries
import hltbscraper
import steamscraper
import calculator

# Functions

# Given a game's app id, will find and return a dictionary of different average completion lengths
def main():
    hltbID = None
    print("Please provide the name of a game:")
    game = input()
    while not hltbID:
        # ID finding
        hltbInfo = hltbscraper.findHLTBAppID(game)
        steamID = steamscraper.findSteamAppID(game)

        if not hltbID:
            print(f"The title \'{game}\' could not be found on How Long To Beat")
            print("Please provide the game's title again\n")
            game = input()
        else:
            print(f"The title found was {hltbInfo[0]}")
            print("If this is correct, press Enter. Otherwise please provide the game's title again.")
            game = input()
            if game != "":
                hltbID = None
            else:
                hltbID = hltbInfo[1]

        

    # Data finding
    lengthDict = hltbscraper.findLength(hltbID)
    percentList = steamscraper.findPercents(steamID)

    # Results
    calculator.tableMaker(lengthDict, percentList)
    calculator.descriptionMaker(lengthDict, percentList)

# Main Execution
if __name__ == '__main__':
    main()
