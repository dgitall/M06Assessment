import json
import random

# Global Return result codes
RSLT_NONE = 0
RSLT_STOP = -1
RSLT_ERROR = -2

RSLT_ENDTURN = -10
RSLT_SPINAGAIN = -11
RSLT_VOWELS_ONLY = -12
RSLT_ROUNDOVER = -13
RSLT_FINALROUND = -14
RSLT_FINALWON = -15
RSLT_FINALLOST = -15
RSLT_GAMEEND = -16

WHEEL_BANKRUPT = -1
WHEEL_BANKRUPT2 = -2
WHEEL_MILLION = -3
WHEEL_LOSETURN = -4

globalFinalRoundLetters = ['R', 'S', 'T', 'L', 'N', 'E']

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
    result, GameControl, GameWheel = InitializeGame(PlayerList, GamePlayers,
                            GameWheel, GameSettings, GameControl)

    # Keep playing the game until it is done or there are problems
    PlayerTurn = 0
    RoundCount = 1
    while result == RSLT_NONE:
        GamePlayers[0]['RoundTotal'] = 0
        GamePlayers[1]['RoundTotal'] = 0
        GamePlayers[2]['RoundTotal'] = 0
        GameControl['VowelsOnly'] = False
        GameControl['VowelSolveAllowed'] = False
        GameControl['GuessList'] = None
        GameControl['DisplayList'] = None
        
        #print("\n")
        print(globalStringRscs['RoundBanner1'])
        print(fstr(globalStringRscs['RoundBanner2'], locals()))
        print(globalStringRscs['RoundBanner1'])

        
        result, RoundPuzzle, GameControl = SelectPuzzle(PuzzleDict, GameControl)
        
        # Keep playing the round until someone finishes
        continueround = True
        while continueround:
            result = ShowPuzzle(RoundPuzzle, GameControl)
            print("%s: $%d    %s: $%d     %s: $%d" %
                  (GamePlayers[0]['Player']['Name'], GamePlayers[0]['RoundTotal'],
                   GamePlayers[1]['Player']['Name'], GamePlayers[1]['RoundTotal'],
                   GamePlayers[2]['Player']['Name'], GamePlayers[2]['RoundTotal']))
            print(fstr(globalStringRscs['TurnMessage'], locals()))
            print("\n")
            
            # Check if all letters have been filled in and give current player a shot to solve the puzzle
            if(sum(GameControl['DisplayList']) == len(GameControl['DisplayList'])):
                result, GamePlayers[PlayerTurn], GameControl = SolvePuzzle(
                    GamePlayers[PlayerTurn], GameControl, RoundPuzzle)
                if(result == RSLT_ROUNDOVER):
                    continueround = False
                    break

            # Check to see if the puzzle has only vowels. If so, need to branch off to a different algorithm to finish the puzzle
            if GameControl['VowelsOnly']:
                result, GamePlayers, PlayerTurn, GameControl = VowelsOnly(GamePlayers, PlayerTurn, GameControl, RoundPuzzle)
                continueround = False
                break
                
            input(fstr(globalStringRscs['SpinTheWheel'], locals()))
            print("\n")
            spinresult = SpinTheWheel(GameWheel)
            if(spinresult != RSLT_ERROR):
                result, GamePlayers[PlayerTurn], GameControl = EvaluateSpin(
                    spinresult, GamePlayers[PlayerTurn], GameControl, RoundPuzzle)
            else:
                result = RSLT_ERROR
                
            if result == RSLT_ENDTURN:
                # Move to the next player
                PlayerTurn = PlayerTurn + 1
                if PlayerTurn > 2:
                    PlayerTurn = 0
                # Reset if vowels and solving the puzzle are allowed.
                GameControl['VowelSolveAllowed'] = False
            elif result == RSLT_ROUNDOVER:
                continueround = False
                
        # The round has been completed
        # Move the players round total over to the game total.
        GamePlayers[PlayerTurn]['GameTotal'] += GamePlayers[PlayerTurn]['RoundTotal']        
        print(fstr(globalStringRscs['EndRoundCongrats1'], locals()))
        print(fstr(globalStringRscs['EndRoundCongrats2'], locals()))
        print(fstr(globalStringRscs['EndRoundCongrats3'], locals()))

        

        
        if(RoundCount < 2):
            RoundCount += 1
            PlayerTurn = 1
            result = RSLT_NONE
        else:
            result = RSLT_FINALROUND
            
    # The normal part of the game has completed
    # If this was due to normal play, continue to the final round, otherwise just exit.
    if(result == RSLT_FINALROUND):
        result, GamePlayers, GameControl = PlayFinalRound(GamePlayers, GameControl, PuzzleDict)
        # If the game was completed without error, update the player stats
        for index in range(0,3):
            GamePlayers[index]['Player']['GamesPlayed'] += 1
            GamePlayers[index]['Player']['TotalWinnings'] += GamePlayers[index]['GameTotal']
            # If the player in the final round, update their win total
            if(index == PlayerTurn):
                GamePlayers[index]['Player']['GamesWon'] += 1
        result = RSLT_GAMEEND
                
    return result, PlayerList

def PlayFinalRound(GamePlayers, GameControl, PuzzleDict):
    result =RSLT_NONE
    
    GameControl['DisplayList'] = None
    GameControl['GuessList'] = globalFinalRoundLetters
    GameControl['VowelSolveAllowed'] = True
    
    # Determine which player gets to move into the final round.
    max = 0
    winner = -1
    for index in range(0,3):
        if (GamePlayers[index]['GameTotal'] > max):
            max = GamePlayers[index]['GameTotal']
            winner = index
        elif (GamePlayers[index]['GameTotal'] == max):
            if (max == -1):
                winner = index
            else:
                coin = random.randint(0,1)
                if(coin == 0):
                    winner = index
    if winner == -1:
        result = RSLT_ERROR
    
    if(result == RSLT_NONE):            
        FinalPlayer = GamePlayers[winner]
        print(f"\n\nFINAL ROUND\n")
        print(f"Congratulation, {FinalPlayer['Player']['Name']} on making it to the final round")
        print(f"You will play for a cash prize of $100,000")
        print(f"<cheers><cheers>")
        print("You will start with the letters R-S-T-L-N-E filled in and then select three additional consonants and one vowel.")
        
        # Create the puzzles
        result, RoundPuzzle, GameControl = SelectPuzzle(PuzzleDict, GameControl)
        
        # Call CheckGuess on the 6 starter guesses and show the puzzle
        for i, value in enumerate(globalFinalRoundLetters):
            numfound, GameControl = CheckGuess(value, RoundPuzzle, GameControl)
        result = ShowPuzzle(RoundPuzzle, GameControl)
        
        # Have the player enter 3 consonants
        for i in range(0,3):
            invalidinput = True
            userinput = 0
            while invalidinput:
                userinput = input(fstr(globalStringRscs['FinalRoundConsonantPrompt'], locals())).upper()
                if userinput not in ('A', 'E', 'I', 'O', 'U'):
                    if GameControl['GuessList'] == None:
                        invalidinput = False
                    elif userinput not in GameControl['GuessList']:
                        invalidinput = False
            numfound, GameControl = CheckGuess(userinput, RoundPuzzle, GameControl)
        
        # Have the player enter 1 vowel
        invalidinput = True
        userinput = 0
        while invalidinput:
            userinput = input(
                globalStringRscs['FinalRoundVowelPrompt']).upper()
            if userinput in ('A', 'E', 'I', 'O', 'U'):
                if GameControl['GuessList'] == None:
                    invalidinput = False
                elif userinput not in GameControl['GuessList']:
                    invalidinput = False
        numfound, GameControl = CheckGuess(userinput, RoundPuzzle, GameControl)
        
        
        result, FinalPlayer, GameControl = SolvePuzzle(FinalPlayer, GameControl, RoundPuzzle)
        if(result == RSLT_ROUNDOVER):
            print(globalStringRscs['FinalRoundWinnerBanner1'])
            print(globalStringRscs['FinalRoundWinnerBanner2'])
            print(globalStringRscs['FinalRoundWinnerBanner3'])
            print(globalStringRscs['FinalRoundWinnerBanner2'])
            print(globalStringRscs['FinalRoundWinnerBanner1'])
            print("\n\n")
            print(fstr(globalStringRscs['FinalRoundWinnerMessage1'], locals()))
            FinalPlayer['GameTotal'] += 100000
            print(fstr(globalStringRscs['FinalRoundWinnerMessage2'], locals()))
        elif (result == RSLT_ENDTURN):
            print(globalStringRscs['FinalRoundLoserBanner1'])
            print(globalStringRscs['FinalRoundLoserBanner1'])
            print(globalStringRscs['FinalRoundLoserBanner2'])
            print(globalStringRscs['FinalRoundLoserBanner1'])
            print(globalStringRscs['FinalRoundLoserBanner1'])
            print("\n\n")
            print(fstr(globalStringRscs['FinalRoundLoserMessage'], locals()))
 
    return result, GamePlayers, GameControl


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
    GameControl = {'VowelsOnly': False, 'FinalRound': False, 'DisplayList': None, 'GuessList': None, 'VowelSolveAllowed': False}
    
    
    return result, GameControl, GameWheel

## Select a random choice from the list of puzzles loaded in. Pulling it out of the loaded list
## So that we don't pick the same puzzle again later
def SelectPuzzle(PuzzleDict, GameControl):
    result = RSLT_ERROR
    Puzzle = {}
    
    # Check if a valid puzzle dictionary then proceed to pick a puzzle for this round
    if((PuzzleDict is not None) and (len(PuzzleDict) != 0)):
        pick = random.choice(list(PuzzleDict))
        Puzzle = {'Puzzle': pick.upper(), 'Clue': PuzzleDict[pick].title()}
        # Pop the pick out of the dictionary to avoid picking again
        PuzzleDict.pop(pick)
        # Initialize the displaylist for this puzzles. Set to automatically show non-alpha characters at the start
        GameControl['DisplayList'] = [False]*len(Puzzle['Puzzle'])
        for i in range(0, len(Puzzle['Puzzle'])):
            if(Puzzle['Puzzle'][i].isalpha() == False):
                GameControl['DisplayList'][i] = True

        result = RSLT_NONE
        
    return result, Puzzle, GameControl

## Display the puzzle, revealing the correctly guessed letter, the clue, and the list of already buessed letters
def ShowPuzzle(RoundPuzzle, GameControl):
    result = RSLT_NONE
    
    print(globalStringRscs['ShowPuzzleBanner'])
    displayword = ''
    for i, value in enumerate(GameControl['DisplayList']):
        if value:
            displayword += RoundPuzzle['Puzzle'][i] + ' '
        else:
            displayword += '_ '
    print(displayword)
    print(RoundPuzzle['Clue'])
    if(GameControl['GuessList'] != None):
        print(fstr(globalStringRscs['ShowGuesses'], locals()))
        
    print(globalStringRscs['ShowPuzzleBanner'])
    
    return result

## Spin the wheel by randomly picking a spot in the list. Handle the special case where there might be a million spin.
def SpinTheWheel(GameWheel):
    result = WHEEL_BANKRUPT
    
    # Make sure we got a valid wheel
    if(len(GameWheel) != 0):
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
    else:
        result = RSLT_ERROR
            
    return result

## Play the case where there are only vowels left. Cycle through players who guess a vowel and if it is there
## try to solve the puzzle.
def VowelsOnly(GamePlayers, PlayerTurn, GameControl, RoundPuzzle):
    result = RSLT_NONE
    
    print(globalStringRscs['VowelsOnlyBanner'])
    while result != RSLT_ROUNDOVER:
        # Get the player's guess and check that it's a consonant and hasn't already been guessed
        result = ShowPuzzle(RoundPuzzle, GameControl)
        if(sum(GameControl['DisplayList']) == len(GameControl['DisplayList'])):
            print("\nThere are no letters remaining....")
            print(fstr(globalStringRscs['VowelTurn'], locals()))
            result, Player, GameControl = SolvePuzzle(Player, GameControl, RoundPuzzle)
        else:
            print(fstr(globalStringRscs['VowelTurn'], locals()))
            GameControl['VowelSolveAllowed'] = True
            invalidinput = True
            userinput = 0
            while invalidinput:
                userinput = input(globalStringRscs['VowelsOnlyPrompt']).upper()
                if userinput in ('A', 'E', 'I', 'O', 'U'):
                    if GameControl['GuessList'] == None:
                        invalidinput = False
                    elif userinput not in GameControl['GuessList']:
                        invalidinput = False

            ## Call the function to check how many times the guess is in the puzzle
            numfound, GameControl = CheckGuess(userinput, RoundPuzzle, GameControl)
            if numfound == 0:
                Player = GamePlayers[PlayerTurn]
                print(fstr(globalStringRscs['BadGuessMessage'], locals()))
                result = RSLT_ENDTURN
            else:
                print(fstr(globalStringRscs['GoodConsGuessMessage'], locals()))
                
            # result = ShowPuzzle(RoundPuzzle, GameControl)
                Player = GamePlayers[PlayerTurn]
                result, Player, GameControl = SolvePuzzle(Player, GameControl, RoundPuzzle)

        if(result==RSLT_ENDTURN):
            PlayerTurn += 1
            if(PlayerTurn > 2):
                PlayerTurn = 0
            
        # add the guess to the guess list and return that it's the end of the turn
        if (GameControl['GuessList'] == None):
            GameControl['GuessList'] = [userinput]
        else:
            GameControl['GuessList'].append(userinput)
            
        
    return result, GamePlayers, PlayerTurn, GameControl

## Evaluate the results of the spin. Check for the special cases, otherwise pass on to a function to allow 
## The player to take their turn
def EvaluateSpin(SpinResult, Player, GameControl, RoundPuzzle):
    result = RSLT_NONE
    
    if(SpinResult == WHEEL_LOSETURN):
        print(fstr(globalStringRscs['LoseTurnMessage'], locals()))
        result = RSLT_ENDTURN
    elif (SpinResult == WHEEL_BANKRUPT):
        print(fstr(globalStringRscs['BankruptMessage'], locals()))
        Player['RoundTotal'] = 0
        result = RSLT_ENDTURN
    else:
        result, Player, GameControl = PlayNormalGuess(SpinResult, Player, GameControl, RoundPuzzle)
    
    return result, Player, GameControl


def PlayNormalGuess(SpinResult, Player, GameControl, RoundPuzzle):
    result = RSLT_NONE
    
    ## If the player got the million dollar spin substitute in the dollar value. 
    ## NOTE: This is a change to the game rules agreed upon in the class. Change later to keep the million card
    ## stored with the player who can only redeem it if they win the final round. 
    if(SpinResult == WHEEL_MILLION):
        SpinResult = 1000000000
    print(fstr(globalStringRscs['SpinResult'], locals()))
    
    invalidturn = True    
    ## Check if the puzzle is all filled in and auto-jump to solve the puzzle.
    if(sum(GameControl['DisplayList']) == len(GameControl['DisplayList'])):
        result, Player, GameControl = SolvePuzzle(Player, GameControl, RoundPuzzle)

        invalidturn = False
    
    ## Show the menu for the player to choose how they want to play their turn

    while invalidturn:
        userinput = 0
        invalidinput = True
        while invalidinput:
            print(globalStringRscs['PlayerTurnMenu'])
            userinput = input(globalStringRscs['PlayerTurnPrompt'])
            if userinput in ['1', '2', '3']:
                invalidinput = False
        
        ## Go off to the appropriate function to handle what the player selected to do
        if userinput == '1':
            result, Player, GameControl = GuessConsonant(SpinResult, Player, GameControl, RoundPuzzle)
            if result != RSLT_NONE:
                invalidturn = False       
        elif userinput == '2':
            result, Player, GameControl = BuyVowel(Player, GameControl, RoundPuzzle)
            if result != RSLT_NONE:
                invalidturn = False
        else:
            result, Player, GameControl = SolvePuzzle(Player, GameControl, RoundPuzzle)
            if result != RSLT_NONE:
                invalidturn = False
                
    return result, Player, GameControl

## The player wants to guess a consonant
def GuessConsonant(SpinResult, Player, GameControl, RoundPuzzle):
    result = RSLT_NONE
    result = ShowPuzzle(RoundPuzzle, GameControl)
    print(globalStringRscs['ConsonantBanner'])
    
    # Get the player's guess and check that it's a consonant and hasn't already been guessed
    invalidinput = True
    userinput = 0
    while invalidinput:
        userinput = input(globalStringRscs['ConsonantPrompt']).upper()
        if userinput not in ('A', 'E', 'I', 'O', 'U'):
            if GameControl['GuessList'] == None:
                invalidinput = False
            elif userinput not in GameControl['GuessList']:
                invalidinput = False
    
    ## Call the function to check how many times the guess is in the puzzle
    numfound, GameControl = CheckGuess(userinput, RoundPuzzle, GameControl)
    if numfound == 0:
        print(fstr(globalStringRscs['BadGuessMessage'], locals()))
        result = RSLT_ENDTURN
    else:
        guessamount = numfound * SpinResult
        Player['RoundTotal'] += guessamount
        print(fstr(globalStringRscs['GoodConsGuessMessage'], locals()))
        print(fstr(globalStringRscs['GoodConsGuessMessage2'], locals()))
        if IsVowelsOnly(RoundPuzzle, GameControl):
            GameControl['VowelsOnly'] = True
            result = RSLT_SPINAGAIN
        else:
            GameControl['VowelSolveAllowed'] = True
            result = RSLT_SPINAGAIN
    # add the incorrect guess to the guess list and return that it's the end of the turning
    if (GameControl['GuessList'] == None):
        GameControl['GuessList'] = [userinput]
    else:
        GameControl['GuessList'].append(userinput)
        
    return result, Player, GameControl

## Check to see if the remaining characters in the puzzle are all vowels or not
def IsVowelsOnly(RoundPuzzle, GameControl):
    result = True
    
    # Check all the places where DisplayList is False and see if there are any consonants left.
    for i, value in enumerate(GameControl['DisplayList']):
        if not value:
            if(RoundPuzzle['Puzzle'][i] not in ('A', 'E', 'I', 'O', 'U')):
                result = False
                break
    
    return result

## Count how many times the guessed character is part of the puzzle. If so, change the display list to show
def CheckGuess(Guess, Puzzle, GameControl):
    count = 0
    
    # Quick check to see if the guess is in the puzzle
    count = Puzzle['Puzzle'].count(Guess)
    # If it is there, we need to find all the locations to set DisplayList to allow revealing that character in the puzzle
    if(count > 0):
        startindex = 0
        # Start at the left and keep finding occurrences
        for i in range(0, count):
            index = Puzzle['Puzzle'].find(Guess, startindex)
            GameControl['DisplayList'][index] = True
            startindex = index + 1
            
    return count, GameControl

# Player wants to buy a vowel
def BuyVowel(Player, GameControl, RoundPuzzle):
    result = RSLT_NONE
    
    # Check to see if it is allowed to buy a vowel
    if((GameControl['VowelSolveAllowed']) and Player['RoundTotal'] >= 250):
        
        Player['RoundTotal'] -= 250
    
        result = ShowPuzzle(RoundPuzzle, GameControl)
        
        print(globalStringRscs['VowelBanner'])
        # Get the player's guess and check that it's a vowel and hasn't already been guessed
        invalidinput = True
        userinput = 0
        while invalidinput:
            userinput = input(globalStringRscs['VowelPrompt']).upper()
            if userinput in ('A', 'E', 'I', 'O', 'U'):
                if GameControl['GuessList'] == None:
                    invalidinput = False
                elif userinput not in GameControl['GuessList']:
                    invalidinput = False
                    
        ## Call the function to check how many times the guess is in the puzzle
        numfound, GameControl = CheckGuess(userinput, RoundPuzzle, GameControl)
        if numfound == 0:
            print(fstr(globalStringRscs['BadGuessMessage'], locals()))
            result = RSLT_ENDTURN
        else:
            print(fstr(globalStringRscs['GoodConsGuessMessage'], locals()))
            result = RSLT_SPINAGAIN
        # add the incorrect guess to the guess list and return that it's the end of the turning
        if (GameControl['GuessList'] == None):
            GameControl['GuessList'] = [userinput]
        else:
            GameControl['GuessList'].append(userinput)

    else:
        print("\n")
        print(globalStringRscs['CantBuyVowel'])
    
    return result, Player, GameControl

## Player wants to solve the puzzle
def SolvePuzzle(Player, GameControl, RoundPuzzle):
    result = RSLT_NONE
    
    userinput = 0    
    if(GameControl['VowelSolveAllowed']):
        result = ShowPuzzle(RoundPuzzle, GameControl)
        print(globalStringRscs['SolveBanner'])
        # Get the player's guess and check that it's not empty
        invalidinput = True
        while invalidinput:
            userinput = input(globalStringRscs['SolvePrompt']).upper()
            if len(userinput) > 0:
                invalidinput = False
    else:
        print("\n")
        print(globalStringRscs['CantSolvePuzzle'])
       
    if(GameControl['VowelSolveAllowed']):
        if (userinput == RoundPuzzle['Puzzle']):
            print("\n")
            print(globalStringRscs['SolveSuccessBanner'])
            print(fstr(globalStringRscs['SolveSuccessMessage'], locals()))
            print(globalStringRscs['SolveSuccessBanner'])

            result = RSLT_ROUNDOVER       
        else:
            print(fstr(globalStringRscs['SolveFailMessage'], locals()))
            result = RSLT_ENDTURN
        
    return result, Player, GameControl

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
            result, PlayerList = PlayGame(PuzzleDict, PlayerList, GameSettings)
            if(result == RSLT_GAMEEND):
                ShowPlayerStats(PlayerList)
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
