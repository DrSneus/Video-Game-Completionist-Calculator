# Samuel Neus
# Main function adapted to a GUI

# Libraries
import calculator
import hltbscraper
import steamscraper
import PySimpleGUI as gui

# The GUI Template
gui.theme('Dark Blue 3')

layout = [  [gui.Text(size=(None, 1), key='textOut1')],
            [gui.Text(size=(None, 1), key='textOut2')],
            [gui.Input(key='gamename', do_not_clear=False)],
            [gui.Button('Enter'), gui.Button('Quit')],
            [gui.Multiline(size=(None, 24), key='stats', disabled=True, background_color='Light Slate Gray', text_color='White')]]

# Create the Window
window = gui.Window("Completionist Calculator", layout, finalize=True)
window['textOut1'].update("Welcome to the Completionist Calculator!")
window['textOut2'].update("Please write the name of the game to check:")

# Main Loop
hltbID = None
skipInput = False
while True:
    # Some results require inputs later, so it needs to be possible to skip the initial prompt
    if not skipInput:
        # Events
        event, values = window.read()

        # Quit
        if event == gui.WIN_CLOSED or event == 'Quit':
            break
    else:
        skipInput = False

    # Finding game
    if event == 'Enter' and values['gamename'] != "" and not hltbID:
        # Game finding
        game = values['gamename']
        hltbInfo = hltbscraper.findHLTBAppID(game)

        # Game not found
        if not hltbInfo:
            window['textOut1'].update(f"The title \'{game}\' could not be found on How Long To Beat")
            window['textOut2'].update("Please provide the game's title again:\n")
            continue

        # Game found
        else:
            window['textOut1'].update(f"The title found was \'{hltbInfo[0]}\'")
            window['textOut2'].update("If this is correct, press Enter. Otherwise please provide the game's title again.")
            
            event, values = window.read()
            # Quit
            if event == gui.WIN_CLOSED or event == 'Quit':
                break

            # Confirm title
            elif event == 'Enter' and values['gamename'] == "":
                # ID finding
                hltbID = hltbInfo[1]
                steamID = steamscraper.findSteamAppID(hltbInfo[0])
                skipInput = True
                continue

            # Change in title
            else:
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
        window['stats'].update(display)
        window['textOut2'].update("Please write the name of the game to check:")

        # Resetting
        hltbID = None
        event, values = window.read()

        # Quit
        if event == gui.WIN_CLOSED or event == 'Quit':
            break

        # Reset
        else:
            window['textOut1'].update("Welcome to the Completionist Calculator!")
            window['stats'].update("")
            skipInput = True