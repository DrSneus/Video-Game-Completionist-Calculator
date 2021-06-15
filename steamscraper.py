# Samuel Neus
# Functions used for web scraping the Steam store

import requests
import re

# Functions

# Given a Steam game's app id, will find and return a list of achievement percentages
def findPercents(id):
    # Downloads text
    response = requests.get(f"https://steamcommunity.com/stats/{id}/achievements").text.split('\n')

    data = []
    for lines in response[1:]:
        # Searches for the percentage of players who've completed certain achievements
        x = re.search('achievePercent">([0-9]+\.[0-9])', lines.lstrip())
        if x:
            data.append(float(x.group(1))) # Appends the percentage of players to the list

    # Determines whether the end result is valid
    if len(data) == 0:
        print("This title does not have any Steam achievements.")
        return None

    return data

# Main Execution
if __name__ == '__main__':
    findPercents(250900)
