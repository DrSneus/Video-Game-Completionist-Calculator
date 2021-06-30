# Samuel Neus
# Combines the calculator_gui with the usercalculator functions for a complete calculator

# Libraries
import calculator
import hltbscraper
import steamscraper
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
            [gui.Multiline(size=(None, 24), key='ustats', disabled=True, background_color='Light Slate Gray', text_color='White')]]

gameLayout = [  [gui.Text(size=(None, 1), key='gOut1')],
            [gui.Text(size=(None, 1), key='gOut2')],
            [gui.Input(key='gamename', do_not_clear=False)],
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
        continue

    # Game state options
    if state == 'Game':
        # Finding game
        if event == 'Enter' and values['gamename'] != "" and not hltbID:
            # Game finding
            window['gOut2'].update("Loading...")
            window.finalize()
            game = values['gamename']
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
                if event == 'Enter' and values['gamename'] == "":
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
            window['gstats'].update(display)
            window['gOut2'].update("Please write the name of the game to check:")

            # Resetting
            hltbID = None
            event, values = window.read()

            window['gOut1'].update("Welcome to the Completionist Calculator!")
            window['gstats'].update("")
            skipInput = True