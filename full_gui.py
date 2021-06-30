# Samuel Neus
# Combines the calculator_gui with the usercalculator functions for a complete calculator

# Libraries
from tkinter.constants import X
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

userLayout = [  [gui.Text(size=(None, 1), key='uOut1')],
            [gui.Text(size=(None, 1), key='uOut2')],
            [gui.Input(key='uname', do_not_clear=False)],
            [gui.Button('Enter'), gui.Button('Menu')],
            [gui.Multiline(size=(None, 24), key='ustats', disabled=True, background_color='Light Slate Gray', text_color='White', reroute_stdout=True, auto_refresh=True, autoscroll=True)]]

gameLayout = [  [gui.Text(size=(None, 1), key='gOut1')],
            [gui.Text(size=(None, 1), key='gOut2')],
            [gui.Input(key='gname', do_not_clear=False)],
            [gui.Button('Enter'), gui.Button('Menu')],
            [gui.Multiline(size=(None, 24), key='gstats', disabled=True, background_color='Light Slate Gray', text_color='White')]]

# Sets the layout
layout = [[gui.Column(menuLayout, key='MenuL'), gui.Column(gameLayout, visible=False, key='GameL'), gui.Column(userLayout, visible=False, key='UserL')]]

# Create the Window
window = gui.Window("Completionist Calculator", layout, finalize=True)

# Loop Variables
state = 'Menu'
hltbID = None
userID = None
skipInput = False
menuCategories = ['Menu', 'Menu1', 'Game', 'User']

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
        # Converting button input to actual layout
        if event == 'Menu1':
            event = 'Menu'

        # Basic visual change
        window[f'{state}L'].update(visible=False)
        state = event
        window[f'{state}L'].update(visible=True)

        # Resetting complex menus
        if state == 'Game':
            hltbID = None

            window['gOut1'].update("Welcome to the Completionist Calculator!")
            window['gOut2'].update("Please write the name of the game to check:")
            window['gstats'].update("")
        elif state == 'User':
            user = None

            window['uOut1'].update("Welcome to the Completionist Calculator!")
            window['uOut2'].update("Please write the name of a public Steam profile to check:")
            window['ustats'].update("")
        continue

    # Game state options
    if state == 'Game':
        # Finding game
        if event == 'Enter' and values['gname'] != "" and not hltbID:
            # Game finding
            window['gOut2'].update("Loading...")
            window.finalize()
            game = values['gname']
            hltbInfo = hltbscraper.findHLTBAppID(game)

            # Game not found
            if not hltbInfo:
                window['gOut1'].update(f"The title \'{game}\' could not be found on How Long To Beat")
                window['gOut2'].update("Please provide the game's title again:\n")
                continue

            # Game found
            else:
                window['gOut1'].update(f"The title found was \'{hltbInfo[0]}\'")
                window['gOut2'].update("If this is correct, press Enter. Otherwise please provide the game's title again.")
                
                # Confirmation event
                event, values = window.read()

                # Game confirmation
                if event == 'Enter' and values['gname'] == "":
                    # Display loading
                    window['gOut2'].update("Loading...")
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
            display = calculator.tableMaker(lengthDict, percentList, True)
            display = "".join([display, calculator.descriptionMaker(lengthDict, percentList, True)])
            window['gOut1'].update(f"Game: \'{hltbInfo[0]}\'")
            window['gOut2'].update("Please write the name of the game to check:")
            window['gstats'].update(display)

            # Resetting
            hltbID = None
            event, values = window.read()

            window['gOut1'].update("Welcome to the Completionist Calculator!")
            window['gstats'].update("")
            skipInput = True

    # User state options
    elif state == 'User':
        # Finding a user
        if event == 'Enter0' and values['uname'] != "" and not user:
            # User finding
            window['uOut2'].update("Loading...")
            window.finalize()
            user = values['uname']
            userGames = userscraper.findGames(user)

            # User not found, or user's profile is private
            if not userGames:
                window['uOut1'].update(f"No data was found for \'{user}\'.")
                window['uOut2'].update("Please be sure that their profile is public and resubmit their name:\n")
                user = None
                continue

            # User found
            else:
                window['uOut1'].update(f"User \'{user}\' was found")
                window['uOut2'].update("If this is correct, press Enter. Otherwise please provide the username again.")
                
                # Confirmation event
                event, values = window.read()

                # User confirmation
                if event == 'Enter0' and values['uname'] == "":
                    # Display loading
                    window['uOut1'].update("Loading...")
                    window['uOut2'].update("This may take a while depending on the user's game library")
                    window.finalize()

                skipInput = True
                continue

        # Displaying user data
        elif event == 'Enter0' and user:
            # Tag finding and display
            userTags = usercalculator.getTagList(userGames)
            window['ustats'].update("")

            usercalculator.displayTagList(userTags)
            window['uOut1'].update(f"User: \'{user}\'")
            window['uOut2'].update("Please write the name of a public Steam profile to check:")

            # Resetting
            user = None
            event, values = window.read()

            window['uOut1'].update("Welcome to the Completionist Calculator!")
            window['ustats'].update("")
            skipInput = True
