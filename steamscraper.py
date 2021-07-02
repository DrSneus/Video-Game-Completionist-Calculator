# Samuel Neus
# Functions used for web scraping the Steam store

import requests
import re
import difflib

# Functions
def findSteamAppID(game):
    # Gets a web response from the Steam store page
    gameSearch = game.replace(" ", "+")
    response = requests.get(f"https://store.steampowered.com/search/?term={gameSearch}")

    # Searches for app ids
    gameList = {}
    for lines in response.text.split('\n'):
        x = re.search("<a href=\"https://store.steampowered.com/app/(.*)/(.*)/.*\"", lines)
        if x: # Creates a dictionary of games and their steam ids
            gameList[x.group(2)] = x.group(1)

    # Finds the closest match to the user input
    closeMatch = difflib.get_close_matches(game, gameList, 1, .8)

    # If no match was found return None, else return the appID of the closest
    if len(closeMatch) != 0:
        appID = int(gameList[closeMatch[0]])
    else:
        appID = None

    return appID

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
        return None

    return data

# Given a Steam game's app id, will find and return its tags
def findTags(id):
    # Downloads text
    response = requests.get(f"https://store.steampowered.com/app/{id}").text.split('\n')

    data = {}
    for lines in response[1:]:
        # Searches for the tags of a product
        x = re.search('\[{\"tagid\"(.*)}\]', lines.lstrip())

        if x:
            for tags in x.group().split('},{'):
                # Gathers the game's tagid and name
                stats = re.search('\"tagid\":(\d*),\"name\":\"(.+?)\"', tags)
                data[stats.group(2)] = stats.group(1)
            break

    # Determines whether the end result is valid
    if len(data) == 0:
        return None

    return data

# Main Execution
if __name__ == '__main__':
    appID = findSteamAppID("Borderlands 2")

    if appID:
        data = findTags(appID)
        print(data)
    else:
        print("No ID found")
