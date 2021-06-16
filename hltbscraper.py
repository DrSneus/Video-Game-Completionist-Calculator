# Samuel Neus
# Functions used for web scraping How Long to Beat.com

import requests
import re
import os
import difflib
from googlesearch import search

# Functions
def findHLTBAppID(game):
    # Parameters for searches
    headers = {'user-agent': 'hltb-{}'.format(os.environ.get('USER', 'user'))}
    query = "HowLongToBeat" + game
    
    # Google search
    gameList = {}
    for searches in search(query, tld="com", num=10, stop=10, pause=2):
        # Find the search results with a HLTB url
        hltbURL = re.search("https://howlongtobeat.com/.*id=(\d*)", searches)

        if hltbURL:
            response = requests.get(hltbURL.string, headers=headers)

            # Searches for app ids on the site
            for lines in response.text.split('\n'):
                x = re.search("\'gameName\': \'(.*)\',\s*\'pageType\'", lines)
                if x: # Creates a dictionary of games and their HLTB ids
                    gameList[x.group(1)] = hltbURL.group(1)

    # Finds the closest match to the user input
    closeMatch = difflib.get_close_matches(game, gameList, 1)

    # If no match was found return None, else return the appID of the closest
    if len(closeMatch) != 0:
        appID = int(gameList[closeMatch[0]])
    else:
        appID = None
    return appID


# Given a game's app id, will find and return a dictionary of different average completion lengths
def findLength(id):
    # Downloads text
    headers = {'user-agent': 'hltb-{}'.format(os.environ.get('USER', 'user'))}
    response = requests.get(f"https://howlongtobeat.com/game?id={id}", headers=headers).text.split('\n')

    data = {}
    category = None

    for lines in response[1:]:
        # Searches for the categories of completion, and respective times
        x = re.search('<h5>(.*)</h5>', lines)
        y = re.search('<div>(\d*)(&#189;)? (\w*)\s*</div>', lines)

        if x: # Finds a category of playstyle: "Main Story", "Completionist", etc
            category = x.group(1).strip()
            data[category] = {"Time": None, "Format": None}
            continue

        if category:
            if y: # If there is data for this category
                if y.group(2): # The ASCII for a 0.5 value
                    data[category]["Time"] = float(y.group(1) + ".5")
                else:
                    data[category]["Time"] = float(y.group(1))

                data[category]["Format"] = y.group(3) # Hours or Minutes
            category = None # Resets category

    return data

# Main Execution
if __name__ == '__main__':
    appID = findHLTBAppID("Borderlands 2")
    if appID:
        findLength(appID)
    else:
        print("No ID found")