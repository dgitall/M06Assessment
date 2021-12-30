import WOF_globals
import json

## Prepare the application and print a greeting
def ApplicationStartup():
    PuzzleDict = {}
    PlayerList = []
    GameSettings = {}
    # Greeting
    print(WOF_globals.StringRscs['StartBanner'])

    # Load the list of puzzles and clues
    with open('Data\phrases.json') as json_file:
        PuzzleDict = json.load(json_file)

    # Create and initialize the list of players
    PlayerList = [{'Name': None, 'Bio': None, 'GamesPlayed': 0, 'GamesWon': 0, 'TotalWinnings': 0},
                  {'Name': None, 'Bio': None, 'GamesPlayed': 0, 'GamesWon': 0, 'TotalWinnings': 0},
                  {'Name': None, 'Bio': None, 'GamesPlayed': 0, 'GamesWon': 0, 'TotalWinnings': 0}]

    # Create and Initialize the default game Settings
    GameSettings = {'MillionCard': False}

    return PuzzleDict, PlayerList, GameSettings

## Ask the three players to register
def ContestantSignin(PlayerList):
    result = WOF_globals.RSLT_NONE

    print(WOF_globals.StringRscs['ContestantSignupBanner'])
    for ContestantIndex in range(0,3):
        print(WOF_globals.fstr(WOF_globals.StringRscs['ContestantBanner'], locals()))
        name = str()
        while len(name) == 0:
            name = input(WOF_globals.StringRscs['ContestantName'])
        bio = input(WOF_globals.StringRscs['ContestantBio'])
        PlayerList[ContestantIndex]['Name'] = name
        if len(bio)==0:
            PlayerList[ContestantIndex]['Bio'] = None
        else:
            PlayerList[ContestantIndex]['Bio'] = bio

    return result  


def DisplayDirections():
    result = WOF_globals.RSLT_NONE

    print(WOF_globals.StringRscs['Directions'])
    input(WOF_globals.StringRscs['DirectionsPrompt'])
    return result   

## Show the current game statistics for each player. This is not round statistics but only
## stats for cumulative games completed during this session.
def ShowPlayerStats(PlayerList):
    result = WOF_globals.RSLT_NONE
    print(WOF_globals.StringRscs['ContestantStatsBanner'])
    for ContestantIndex in range(0,3):
        name = PlayerList[ContestantIndex]['Name']
        played = PlayerList[ContestantIndex]['GamesPlayed']
        won = PlayerList[ContestantIndex]['GamesWon']
        winnings = PlayerList[ContestantIndex]['TotalWinnings']
        print(WOF_globals.fstr(WOF_globals.StringRscs['ContestantStatsBanner2'], locals()))
        print(WOF_globals.fstr(WOF_globals.StringRscs['StatsName'], locals()))
        print(WOF_globals.fstr(WOF_globals.StringRscs['StatsGamesPlayed'], locals()))
        print(WOF_globals.fstr(WOF_globals.StringRscs['StatsGamesWon'], locals()))
        print(WOF_globals.fstr(WOF_globals.StringRscs['StatsWinnings'], locals()))


    input(WOF_globals.StringRscs['StatsPrompt'])

    return result   

## Allow the user to change the game settings
def ChangeSettings(GameSettings):
    result = WOF_globals.RSLT_NONE

    print(WOF_globals.StringRscs['SettingsBanner'])
    # Show the list of settings to change and the current value. Repeat until they enter '0' for none
    UserInput = -1
    while UserInput != '0':
        million = GameSettings['MillionCard']
        print(WOF_globals.fstr(WOF_globals.StringRscs['SettingsMenu1'],locals()))
        print(WOF_globals.StringRscs['SettingsMenu0'])
        UserInput = input(WOF_globals.StringRscs['SettingsPrompt'])
        if UserInput == '1':
            GameSettings['MillionCard'] = not GameSettings['MillionCard']


    return result

## Exit Game selected from the menu. Check that the player wants to exit. If so, print
# the contestant statistics and exit.
def ExitGame(PlayerList):
    result = WOF_globals.RSLT_NONE

    print('\n' + WOF_globals.StringRscs['ExitBanner'])
    # Confirm they want to quit
    UserInput = input(WOF_globals.StringRscs['ExitPrompt'])
    if UserInput == 'y':
        # If exiting, print out the player statistics and return code to exit the application
        result = WOF_globals.RSLT_STOP
        print(WOF_globals.StringRscs['ContestantStatsBanner'])
        for ContestantIndex in range(0, 3):
            name = PlayerList[ContestantIndex]['Name']
            played = PlayerList[ContestantIndex]['GamesPlayed']
            won = PlayerList[ContestantIndex]['GamesWon']
            winnings = PlayerList[ContestantIndex]['TotalWinnings']
            print(WOF_globals.fstr(WOF_globals.StringRscs['ContestantStatsBanner2'], locals()))
            print(WOF_globals.fstr(WOF_globals.StringRscs['StatsName'], locals()))
            print(WOF_globals.fstr(WOF_globals.StringRscs['StatsGamesPlayed'], locals()))
            print(WOF_globals.fstr(WOF_globals.StringRscs['StatsGamesWon'], locals()))
            print(WOF_globals.fstr(WOF_globals.StringRscs['StatsWinnings'], locals()))
            print('\n')
        print(WOF_globals.StringRscs['ExitGoodbye'])

    return result   
