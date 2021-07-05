# Samuel Neus
# Functions used for calculating a user's statistics

# Functions
import steamscraper
import userscraper

# Requires the list of games from findGames()
# Breaks down a list of games into a list of most popular tags
def getTagList(gamesDict):
    # Checks if there is a valid dictionary
    if gamesDict == None:
        return None

    # Finds the tags for each game
    tagList = {}
    for appid in gamesDict:
        print(f"Searching {gamesDict[appid]}")
        newTags = steamscraper.findTags(appid)
        if newTags:
            for tag in newTags:
                if tag in tagList: # If the tag is in the list, increment
                    tagList[tag] += 1
                else:
                    tagList[tag] = 1 # Otherwise, add the tag to the list
    return dict(sorted(tagList.items(), key=lambda tag: tag[1]))

# Requires the list of tags from getTagList(), and the list of unplayed games from findGames()
# Suggests an unplayed game from a user's list that best fits the user's preferred tags
def suggestGame(popTagList, unplayedList):
    # Checks if there is a valid dictionary
    if popTagList == None or unplayedList == None:
        return None

    # Goes through each unplayed game, and sorts by amount of overlapping tags
    unplayedSuggestions = {}
    for appid in unplayedList:
        print(f"Searching tags for {unplayedList[appid]}")
        unplayedTags = steamscraper.findTags(appid)
        if unplayedTags:
            unplayedSuggestions[unplayedList[appid]] = 0 # Initializing game in list

            for tag in unplayedTags:
                if tag in popTagList: # If the tag is in the list of preferred tags, improve the game's rating
                    unplayedSuggestions[unplayedList[appid]] += 1

            # Removes items that aren't suggested
            if unplayedSuggestions[unplayedList[appid]] == 0:
                unplayedSuggestions.pop([unplayedSuggestions[appid]])

    return dict(sorted(unplayedSuggestions.items(), key=lambda rank: rank[1]))

# Requires the list of tags from getTagList()
# Prints results
def displayTagList(tagList):
    if tagList:
        print("This user likes games with the following tags:\n")
        while tagList:
            print(f"{tagList.popitem()[0]}")

if __name__ == '__main__':
    data = userscraper.findGames('doctorsneus')
    tagList = getTagList(data)
    #unplayedList = userscraper.findGames('doctorsneus',True)
    
    popTagList = {k: tagList[k] for k in list(tagList)[-10:]}
    #suggestions = suggestGame(popTagList, unplayedList)

    displayTagList(popTagList)

