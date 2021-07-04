# Samuel Neus
# Functions used for web scraping a user's Steam profile

import requests
import re

# Functions
# Finds a user's list of played titles given their Steam ID
# Alternatively, can find a user's list of unplayed untitles
def findGames(id, altMode=False):
    # Downloads text
    response = requests.get(f"https://steamcommunity.com/id/{id}/games/?tab=all&sort=playtime").text.split('\n')

    data = {}
    for lines in response[1:]:
        # Searches for the list of games in a user's account
        x = re.search('var rgGames = (.*)', lines.lstrip())

        if x:
            for games in x.group().split('},{'):
                # Find games that have logged hours
                hours = re.search('\"hours_forever\":\"(.*)\"', games)

                # Default, finds games with logged hours
                if not altMode:
                    if hours:
                        # Gathers the game's steamid and name
                        stats = re.search('\"appid\":(\d*),\"name\":\"(.+?)\"', games)
                        data[stats.group(1)] = re.sub(r'\\u(.){4}', '', stats.group(2)) # Removes Unicodes
                    else:
                        break

                # Finds games without logged hours
                else:
                    if not hours:
                        # Gathers the game's steamid and name
                        stats = re.search('\"appid\":(\d*),\"name\":\"(.+?)\"', games)
                        data[stats.group(1)] = re.sub(r'\\u(.){4}', '', stats.group(2)) # Removes Unicodes
             

            break # Data already found, no need to keep searching

    # Determines whether the end result is valid
    if len(data) == 0:
        return None

    return data

# Main Execution
if __name__ == '__main__':
    data = findGames('doctorsneus')
    print(data)
