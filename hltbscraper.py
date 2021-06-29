# Samuel Neus
# Functions used for web scraping How Long to Beat.com

import requests
import re
import os
import difflib
from googlesearch import search


# Functions
import restart


def findHLTBAppID(game):
    # Parameters for searches
    headers = {'user-agent': 'hltb-{}'.format(os.environ.get('USER', 'user'))}
    query = "HowLongToBeat" + game

    # Google search
    gameList = {}
    for searches in search(query, num=10, stop=10, pause=2):
        # Find the search results with a HLTB url
        hltbURL = re.search("https://howlongtobeat.com/.*id=(\d*)", searches)

        if hltbURL:

            response = requests.get(hltbURL.string, headers=headers)

            # Searches for app ids on the site
            for lines in response.text.split('\n'):
                x = re.search("\'gameName\': \'(.*)\',\s*\'pageType\'", lines)
                if x:  # Creates a dictionary of games and their HLTB ids
                    gameList[x.group(1)] = hltbURL.group(1)

    # Finds the closest match to the user input
    closeMatch = difflib.get_close_matches(game, gameList, 1)

    # If no match was found return None, else return the appID of the closest
    if len(closeMatch) != 0:
        data = [closeMatch[0], int(gameList[closeMatch[0]])]
        return data
    else:
        return None


# Given a game's app id, will find and return a dictionary of different average completion lengths
def findLength(id):
    categories = ["Main Story", "Main + Extras", "Completionists", "All PlayStyles", "Co-Op", "Competitive"]

    # Downloads text
    headers = {'user-agent': 'hltb-{}'.format(os.environ.get('USER', 'user'))}
    response = requests.get(f"https://howlongtobeat.com/game?id={id}", headers=headers).text.split('\n')

    data = {}
    category = None

    for lines in response[1:]:
        # Searches for the categories of completion, and respective times
        x = re.search('<td>(\w.*)</', lines.strip())

        # If one of the desired fields is found
        if x and x.group(1) in categories:
            category = x.group(1)
            data[category] = {"Time": None, "Format": None}  # Creates a dictionary entry
            continue
        elif category:  # The immediate entry after the category is its average time of completion
            # All formats are similar to the form: 50h 20m
            y = re.search("(\d*)(\w) (\d*)?", x.group(1))
            time = 0

            if y.group(2) == "h":  # If the first value is in hours
                time += int(y.group(1)) * 60
                if y.group(3):  # If there is a subscript of minutes
                    time += int(y.group(3))

            else:  # If the only value is in minutes
                time += int(y.group(1))

            data[category] = time  # Add to the dictionary

            category = None  # Resets category

    return data


# Main Execution
if __name__ == '__main__':
    appID = findHLTBAppID("Minecraft")
    if appID:
        findLength(appID)
    else:
        print("No ID found")
        restart.restart()
