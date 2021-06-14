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
    game = "Borderlands the Pre-Sequel"

    # Data finding
    percentList = steamscraper.findPercents(250900)
    lengthDict = hltbscraper.findLength(21248)

    # Calculating
    score = calculator.calculator(lengthDict, percentList)

    # Results
    print(f"The game \"{game}\" has a difficulty rating of {score}")

# Main Execution
if __name__ == '__main__':
    main()
