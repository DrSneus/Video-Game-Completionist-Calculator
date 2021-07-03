# Samuel Neus
# Main Program

# Libraries
import usercalculator
import calculator
import hltbscraper
import steamscraper
import userscraper
import PySimpleGUI as gui

# The GUI Templates
gui.theme('Dark Blue 3')

# Each layout is set to a different, toggleable column
menuLayout = [  [gui.Text("Welcome to the Completionist Calculator")],
            [gui.Text("Click \'Game\' to find information about a game and click \'User\' to find information about a particular user")],
            [gui.Button('Game'), gui.Button('User')] ]

interactLayout = [  [gui.Text(size=(None, 1), key='Out1')],
            [gui.Text(size=(None, 1), key='Out2')],
            [gui.Input(key='input', do_not_clear=False)],
            [gui.Button('Enter'), gui.Button('Menu')],
            [gui.Multiline(size=(None, 24), key='stats', disabled=True, background_color='Light Slate Gray', text_color='White', reroute_stdout=True, auto_refresh=True, autoscroll=True)]]

# Sets the layout
layout = [[gui.Column(menuLayout, key='MenuL'), gui.Column(interactLayout, visible=False, key='InterL')]]

# Create the Window
window = gui.Window("Completionist Calculator", layout, finalize=True)

# Loop Variables
state = 'Menu'
hltbID = None
userID = None
skipInput = False
menuCategories = ['Menu', 'Game', 'User']

# Main Loop
while True:
    # Deals with any initial inputs
    if not skipInput:
        # Events
        event, values = window.read()    
    
    # No additional inputs gathered
    else:
        skipInput = False

    # Deals with initial event consequences
    # Quit
    if event == gui.WIN_CLOSED:
        break
    
    # Changing the Menu state
    elif event in menuCategories:
        # Basic visual change
        if event == 'Menu':
            window[f'InterL'].update(visible=False)
            window[f'MenuL'].update(visible=True)
        elif event == 'User' or event == 'Game':
            window[f'MenuL'].update(visible=False)
            window[f'InterL'].update(visible=True)

        # Resetting complex menus
        state = event
        if state == 'Game':
            hltbID = None
            window['Out1'].update("Welcome to the Completionist Calculator!")
            window['Out2'].update("Please write the name of the game to check:")
            window['stats'].update("")
        elif state == 'User':
            user = None
            window['Out1'].update("Welcome to the Completionist Calculator!")
            window['Out2'].update("Please write the name of a public Steam profile to check:")
            window['stats'].update("")
        continue

    # Game state options
    if state == 'Game':
        # Finding game
        if event == 'Enter' and values['input'] != "" and not hltbID:
            # Game finding
            window['Out2'].update("Loading...")
            window.finalize()
            game = values['input']
            hltbInfo = hltbscraper.findHLTBAppID(game)

            # Game not found
            if not hltbInfo:
                window['Out1'].update(f"The title \'{game}\' could not be found on How Long To Beat")
                window['Out2'].update("Please provide the game's title again:\n")
                continue

            # Game found
            else:
                window['Out1'].update(f"The title found was \'{hltbInfo[0]}\'")
                window['Out2'].update("If this is correct, press Enter. Otherwise please provide the game's title again.")
                
                # Confirmation event
                event, values = window.read()

                # Game confirmation
                if event == 'Enter' and values['input'] == "":
                    # Display loading
                    window['Out2'].update("Loading...")
                    window.finalize()

                    # ID finding                
                    hltbID = hltbInfo[1]
                    steamID = steamscraper.findSteamAppID(hltbInfo[0])

                skipInput = True
                continue

        # Getting game data
        elif event == 'Enter' and hltbID:
            # Data finding
            lengthDict = hltbscraper.findLength(hltbID)
            percentList = steamscraper.findPercents(steamID)

            # Results
            calculator.tableMaker(lengthDict, percentList)
            calculator.descriptionMaker(lengthDict, percentList)
            window['Out1'].update(f"Game: \'{hltbInfo[0]}\'")
            window['Out2'].update("Please write the name of the game to check:")

            # Resetting
            hltbID = None
            event, values = window.read()

            window['Out1'].update("Welcome to the Completionist Calculator!")
            window['stats'].update("")
            skipInput = True

    # User state options
    elif state == 'User':
        # Finding a user
        if event == 'Enter' and values['input'] != "" and not user:
            # User finding
            window['Out2'].update("Loading...")
            window.finalize()
            user = values['input']
            userGames = userscraper.findGames(user)

            # User not found, or user's profile is private
            if not userGames:
                window['Out1'].update(f"No data was found for \'{user}\'.")
                window['Out2'].update("Please be sure that their profile is public and resubmit their name:\n")
                user = None
                continue

            # User found
            else:
                window['Out1'].update(f"User \'{user}\' was found")
                window['Out2'].update("If this is correct, press Enter. Otherwise please provide the username again.")
                
                # Confirmation event
                event, values = window.read()

                # User confirmation
                if event == 'Enter' and values['input'] == "":
                    # Display loading
                    window['Out1'].update("Loading...")
                    window['Out2'].update("This may take a while depending on the user's game library")
                    window.finalize()

                skipInput = True
                continue

        # Displaying user data
        elif event == 'Enter' and user:
            # Tag finding and display
            userTags = usercalculator.getTagList(userGames)
            userPopTags = {k: userTags[k] for k in list(userTags)[-10:]}
            window['stats'].update("")

            usercalculator.displayTagList(userPopTags)
            window['Out1'].update(f"User: \'{user}\'")
            window['Out2'].update("Please write the name of a public Steam profile to check:")

            # Resetting
            user = None
            event, values = window.read()

            window['Out1'].update("Welcome to the Completionist Calculator!")
            window['stats'].update("")
            skipInput = True
