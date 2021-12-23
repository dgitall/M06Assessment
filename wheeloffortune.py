import json


# Global Return result codes
RSLT_NONE = 0
RSLT_STOP = -1

# Load the string dictionary from the JSON file
globalStringRscs = {}
with open('stringfile.json') as json_file:
    globalStringRscs = json.load(json_file)
    
def ApplicationStartup():
    PuzzleDict = {}
    PlayerList = []
    GameSettings = {}
    
    return PuzzleDict, PlayerList, GameSettings

def ContestantSignin(PlayerList):
    result = RSLT_NONE
    
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
    result = 0
    
    PlayerList = list()
    PuzzleDict = dict()
    GameSettings = dict()
    
    PuzzleDict, PlayerList, GameSettings = ApplicationStartup()
    
    ContestantSignin(PlayerList)
    
    # Show Main Menu
    print(globalStringRscs['MainMenu'])
    
    # Get User Input
    while result != RSLT_STOP:
        UserInput = input(globalStringRscs['MenuPrompt'])
        UserInput = RSLT_NONE
        if UserInput == 1:
            pass
            result = PlayGame(PuzzleDict, PlayerList, GameSettings)
        elif UserInput == 2:
            pass
            result = DisplayDirections()
        elif UserInput == 3:
            pass
            result = ShowPlayerStats(PlayerList)
        elif UserInput == 4:
            pass
            result = ChangeSettings(GameSettings)
        elif UserInput == 5:
            pass
            result = ExitGame(PlayerList)
        
    
    return result


## Main Body of the application
MainApplication()
