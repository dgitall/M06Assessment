import json
import random

# Global Return result codes
RSLT_NONE = 0
RSLT_STOP = -1
RSLT_ERROR = -2

RSLT_ENDTURN = -10
RSLT_SPINAGAIN = -11
RSLT_

WHEEL_BANKRUPT = -1
WHEEL_BANKRUPT2 = -2
WHEEL_MILLION = -3
WHEEL_LOSETURN = -4

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


def DisplayDirections():
    result = RSLT_NONE

    print(globalStringRscs['Directions'])
    input(globalStringRscs['DirectionsPrompt'])
    return result   

## Show the current game statistics for each player. This is not round statistics but only
## stats for cumulative games completed during this session.
def ShowPlayerStats(PlayerList):
    result = RSLT_NONE
    print(globalStringRscs['ContestantStatsBanner'])
    for ContestantIndex in range(0,3):
        name = PlayerList[ContestantIndex]['Name']
        played = PlayerList[ContestantIndex]['GamesPlayed']
        won = PlayerList[ContestantIndex]['GamesWon']
        winnings = PlayerList[ContestantIndex]['TotalWinnings']
        print(fstr(globalStringRscs['ContestantStatsBanner2'], locals()))
        print(fstr(globalStringRscs['StatsName'], locals()))
        print(fstr(globalStringRscs['StatsGamesPlayed'], locals()))
        print(fstr(globalStringRscs['StatsGamesWon'], locals()))
        print(fstr(globalStringRscs['StatsWinnings'], locals()))
        print('\n')
        
    input(globalStringRscs['StatsPrompt'])

    return result   

## Allow the user to change the game settings
def ChangeSettings(GameSettings):
    result = RSLT_NONE

    print(globalStringRscs['SettingsBanner'])
    # Show the list of settings to change and the current value. Repeat until they enter '0' for none
    UserInput = -1
    while(UserInput != '0'):
        million = GameSettings['MillionCard']
        print(fstr(globalStringRscs['SettingsMenu1'],locals()))
        print(globalStringRscs['SettingsMenu0'])
        UserInput = input(globalStringRscs['SettingsPrompt'])
        if UserInput == '1':
            GameSettings['MillionCard'] = not GameSettings['MillionCard']
            
    
    return result

## Exit Game selected from the menu. Check that the player wants to exit. If so, print
# the contestant statistics and exit.
def ExitGame(PlayerList):
    result = RSLT_NONE
    
    print('\n' + globalStringRscs['ExitBanner'])
    # Confirm they want to quit
    UserInput = input(globalStringRscs['ExitPrompt'])
    if UserInput == 'y':
        # If exiting, print out the player statistics and return code to exit the application
        result = RSLT_STOP
        print(globalStringRscs['ContestantStatsBanner'])
        for ContestantIndex in range(0, 3):
            name = PlayerList[ContestantIndex]['Name']
            played = PlayerList[ContestantIndex]['GamesPlayed']
            won = PlayerList[ContestantIndex]['GamesWon']
            winnings = PlayerList[ContestantIndex]['TotalWinnings']
            print(fstr(globalStringRscs['ContestantStatsBanner2'], locals()))
            print(fstr(globalStringRscs['StatsName'], locals()))
            print(fstr(globalStringRscs['StatsGamesPlayed'], locals()))
            print(fstr(globalStringRscs['StatsGamesWon'], locals()))
            print(fstr(globalStringRscs['StatsWinnings'], locals()))
            print('\n')
        print(globalStringRscs['ExitGoodbye'])

    return result   


## Menu selection to play a game
#  This contains the overall flow of the game with most of the complexity handled in other functions
def PlayGame(PuzzleDict, PlayerList, GameSettings):
    result = RSLT_NONE
    GameWheel = []
    GameControl = {}
    GamePlayers = {}
    
    # Initialize the game
    result = InitializeGame(PlayerList, GamePlayers,
                            GameWheel, GameSettings, GameControl)

    # Keep playing the game until it is done or there are problems
    PlayerTurn = 0
    while result == RSLT_NONE:
        result, RoundPuzzle = SelectPuzzle(PuzzleDict)
        
        # Check to see if the puzzle has only vowels. If so, need to branch off to a different algorithm to finish the puzzle
        if GameControl['VowelsOnly']:
            result = VowelsOnly(GameWheel, GamePlayers[PlayerTurn], GameControl)        
            
        spinresult = SpinTheWheel(GameWheel)
        
        result = EvaluateSpin(spinresult, GamePlayers, GameControl)
        
        
        pass

    return result

## Setup to play the game. Create the game wheel, create the game player data object and pick the order
def InitializeGame(PlayerList, GamePlayers, GameWheel, GameSettings, GameControl):
    result = RSLT_NONE
    
    print(globalStringRscs['PlayGameBanner'])
    
    print(globalStringRscs['CreateWheel'])   
    GameWheel = [WHEEL_BANKRUPT,WHEEL_LOSETURN,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,
                 850,900,100,150,200,250,300]
    if(GameSettings['MillionCard']):
        GameWheel[2] = WHEEL_BANKRUPT2

    ## Initialize the game player data
    GamePlayers[0] = {'Player': PlayerList[0], 'RoundTotal': 0, 'GameTotal': 0}
    GamePlayers[1] = {'Player': PlayerList[1], 'RoundTotal': 0, 'GameTotal': 0}
    GamePlayers[2] = {'Player': PlayerList[2], 'RoundTotal': 0, 'GameTotal': 0}
    
    # Set the order of the players
    print(globalStringRscs['PickingPlayerOrder'])
    random.shuffle(GamePlayers)
    print(fstr(globalStringRscs['FirstPlayerOrder'],locals()))
    if GamePlayers[0]['Player']['Bio'] != None:
        print(fstr(globalStringRscs['FirstPlayerBio'], locals()))
    print(fstr(globalStringRscs['SecondPlayerOrder'], locals()))
    if GamePlayers[1]['Player']['Bio'] != None:
        print(fstr(globalStringRscs['SecondPlayerBio'], locals()))
    print(fstr(globalStringRscs['ThirdPlayerOrder'], locals()))
    if GamePlayers[2]['Player']['Bio'] != None:
        print(fstr(globalStringRscs['ThirdPlayerBio'], locals()))
        
    # Initialize the values used to manage the games
    GameControl = {'VowelsOnly': False, 'FinalRound': False, 'DisplayList': None}
    
    
    return result

## Select a random choice from the list of puzzles loaded in. Pulling it out of the loaded list
## So that we don't pick the same puzzle again later
def SelectPuzzle(PuzzleDict):
    result = RSLT_ERROR
    Puzzle = {}
    
    # Check if a valid puzzle dictionary then proceed to pick a puzzle for this round
    if((PuzzleDict is not None) and (len(PuzzleDict) != 0)):
        pick = random.choice(list(PuzzleDict))
        Puzzle = {'Puzzle': pick.upper(), 'Clue': PuzzleDict[pick].title()}
        PuzzleDict.pop(pick)
        result = RSLT_NONE
        
    return result, Puzzle


def SpinTheWheel(GameWheel):
    result = WHEEL_BANKRUPT
    
    # Spin the wheel by making a randomm selection
    result = random.choice(GameWheel)
    ## If the pick was the special bankruptcy then do another roll to see if they got the million dollar prize.
    ## If they do get that remove it from the wheel by turning the slot into a normal bankruptcy slot. NOTE: only
    ## Available if they change the setting to allow it. 
    if(result == WHEEL_BANKRUPT2):
        pick = random.randint(1,3)
        if(pick == 1):
            result = WHEEL_MILLION
            GameWheel[2] = WHEEL_BANKRUPT
        else:
            result = WHEEL_BANKRUPT
            
    return result

def VowelsOnly():
    result = RSLT_NONE
    
    return result

def EvaluateSpin(SpinResult, Player, GameControl):
    result = RSLT_NONE
    
    if(SpinResult == WHEEL_LOSETURN):
        print(fstr(globalStringRscs['LoseTurnMessage'], locals()))
        result = RSLT_ENDTURN
    elif (SpinResult == WHEEL_BANKRUPT):
        print(fstr(globalStringRscs['BankruptMessage'], locals()))
        Player['RoundTotal'] = 0
        result = RSLT_ENDTURN
    else:
        result = PlayNormalGuess(SpinResult, Player, GameControl)
    
    return result


def PlayNormalGuess(SpinResult, Player, GameControl):
    result = RSLT_NONE
    
    if(SpinResult == WHEEL_MILLION):
        SpinResult = 1000000000
    print(fstr(globalStringRscs['SpinResult'], locals()))
    
    userinput = 0
    invalidinput = True
    while invalidinput:
        userinput = input(print(globalStringRscs['PlayerTurnMenu']))
        if userinput in ['1', '2', '3']:
            invalidinput = False
    
    if userinput == '1':
        result = GuessConsonant(SpinResult, Player, GameControl)
    elif userinput == '2':
        result = BuyVowel(SpinResult, Player, GameControl)
    else:
        result = SolvePuzzle(SpinResult, Player, GameControl)

    
    return result


def GuessConsonant(SpinResult, Player, GameControl):
    result = RSLT_NONE
    
    return result


def BuyVowel(SpinResult, Player, GameControl):
    result = RSLT_NONE
    
    return result


def SolvePuzzle(SpinResult, Player, GameControl):
    result = RSLT_NONE
    
    return result

## The Main Application where everything starts and ends
def MainApplication():
    result = RSLT_NONE
    
    PlayerList = list()
    PuzzleDict = dict()
    GameSettings = dict()
    
    PuzzleDict, PlayerList, GameSettings = ApplicationStartup()
    
    ContestantSignin(PlayerList)
      
    # Get User Input and direct to the function dealing with the selection
    while result != RSLT_STOP:
        print(globalStringRscs['MainMenu'])
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