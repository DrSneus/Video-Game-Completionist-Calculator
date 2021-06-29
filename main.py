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
    game = str(input("Please provide the name of a game: "))
    print()
    while not hltbID:
        # Game finding
        hltbInfo = hltbscraper.findHLTBAppID(game)

        print("\n")
        if not hltbInfo:
            print(f"The title \'{game}\' could not be found on How Long To Beat")
            print("Please provide the game's title again")
            game = input()
        else:
            print(f"The title found was \'{hltbInfo[0]}\'")
            game = str(input("If this is correct, press Enter. Otherwise please provide the game's title again: "))
            print()
            if game != "":
                hltbID = None
            else:
                # ID finding
                hltbID = hltbInfo[1]
                steamID = steamscraper.findSteamAppID(hltbInfo[0])

    # Data finding
    lengthDict = hltbscraper.findLength(hltbID)
    percentList = steamscraper.findPercents(steamID)

    # Results
    calculator.tableMaker(lengthDict, percentList)
    calculator.descriptionMaker(lengthDict, percentList)


# Main Execution
if __name__ == '__main__':
    main()
