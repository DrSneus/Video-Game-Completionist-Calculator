# Samuel Neus
# Functions used for web scraping How Long to Beat.com

import requests
import re
import os

# Functions

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
                    data[category]["Time"] = y.group(1) + ".5"
                else:
                    data[category]["Time"] = y.group(1)

                data[category]["Format"] = y.group(3) # Hours or Minutes
            category = None # Resets category

    # Determines whether the end result is valid
    if len(data) == 0:
        print("This title does not exist.")
        return None

    return data

# Main Execution
if __name__ == '__main__':
    findLength(21248)
