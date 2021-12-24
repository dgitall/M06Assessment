import json


# Global Return result codes
RSLT_NONE = 0
RSLT_STOP = -1

# Load the string dictionary from the JSON file
globalStringRscs = {}
with open('stringfile.json') as json_file:
    globalStringRscs = json.load(json_file)

# Function to evaluate the loaded f-strings. This is necessary because you can't include
# dictionary keys if doing it inline due to interference with single and double quotes.
# Taken from: https://stackoverflow.com/questions/47597831/python-fstring-as-function
def fstr(fstring_text, locals, globals=None):
    # Dynamically evaluate the provided fstring_text. Passing in locals and globals allows us
    # to access variables to insert into the f string.
    locals = locals or {}
    globals = globals or {}
    ret_val = eval(f'f"{fstring_text}"', locals, globals)
    return ret_val
    
## Prepare the application and print a greeting
def ApplicationStartup():
    PuzzleDict = {}
    PlayerList = []
    GameSettings = {}
    # Greeting
    print(globalStringRscs['StartBanner'])
    
    # Load the list of puzzles and clues
    with open('phrases.json') as json_file:
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
    result = RSLT_NONE
    
    print(globalStringRscs['ContestantSignupBanner'])
    for ContestantIndex in range(0,3):
        print(fstr(globalStringRscs['ContestantBanner'], locals()))
        name = str()
        while len(name) == 0:
            name = input(globalStringRscs['ContestantName'])
        bio = input(globalStringRscs['ContestantBio'])
        PlayerList[ContestantIndex]['Name'] = name
        if len(bio)==0:
            PlayerList[ContestantIndex]['Bio'] = None
        else:
            PlayerList[ContestantIndex]['Bio'] = bio
        
    return result


def PlayGame(PuzzleDict, PlayerList, GameSettings):
    result = RSLT_NONE

    return result   


def DisplayDirections():
    result = RSLT_NONE

    return result   


def ShowPlayerStats(PlayerList):
    result = RSLT_NONE

    return result   


def ChangeSettings(GameSettings):
    result = RSLT_NONE

    return result

def ExitGame(PlayerList):
    result = RSLT_STOP

    return result   





## The Main Application where everything starts and ends
def MainApplication():
    result = RSLT_NONE
    
    PlayerList = list()
    PuzzleDict = dict()
    GameSettings = dict()
    
    PuzzleDict, PlayerList, GameSettings = ApplicationStartup()
    
    ContestantSignin(PlayerList)
    
    # Show Main Menu
    print(globalStringRscs['MainMenu'])
    
    # Get User Input and direct to the function dealing with the selection
    while result != RSLT_STOP:
        UserInput = input(globalStringRscs['MenuPrompt'])
        if UserInput == '1':
            pass
            result = PlayGame(PuzzleDict, PlayerList, GameSettings)
        elif UserInput == '2':
            pass
            result = DisplayDirections()
        elif UserInput == '3':
            pass
            result = ShowPlayerStats(PlayerList)
        elif UserInput == '4':
            pass
            result = ChangeSettings(GameSettings)
        elif UserInput == '5':
            result = ExitGame(PlayerList)
        
    
    return result


## Main Body of the application
MainApplication()
