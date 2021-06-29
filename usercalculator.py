# Samuel Neus
# Functions used for calculating a user's statistics

# Functions
import steamscraper
import userscraper

# Requires the list of games from findGames()
# Outputs a description of the user's favorite game tags
def userTagList(gamesDict):
    # Checks if there is a valid dictionary
    if gamesDict == None:
        return None

    # Finds the tags for each game
    tagList = {}
    print("This user likes games with the following tags:\n")
    for appid in gamesDict:
        print(f"Searching tags for {gamesDict[appid]}")
        newTags = steamscraper.findTags(appid)
        if newTags:
            for tag in newTags:
                if tag in tagList: # If the tag is in the list, increment
                    tagList[tag] += 1
                else:
                    tagList[tag] = 1 # Otherwise, add the tag to the list
        
    tagList = dict(sorted(tagList.items(), key=lambda tag: tag[1]))
    for i in range(0, 10):
        print(f"{tagList.popitem()[0]}")

if __name__ == '__main__':
    data = userscraper.findGames('doctorsneus')
    userTagList(data)
