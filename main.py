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
    game = "Game Name"

    # Data finding
    percentList = steamscraper.findPercents(567640)
    lengthDict = hltbscraper.findLength(44389)

    # Results
    print(f"{game}")
    calculator.tableMaker(lengthDict, percentList)

# Main Execution
if __name__ == '__main__':
    main()
