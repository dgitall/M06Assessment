import WOF_globals
import random
import WOF_finalround

## Menu selection to play a game
#  This contains the overall flow of the game with most of the complexity handled in other functions
def PlayGame(PuzzleDict, PlayerList, GameSettings):
    result = WOF_globals.RSLT_NONE
    GameWheel = []
    GameControl = {}
    GamePlayers = {}

    # Initialize the game
    result, GameControl, GameWheel = InitializeGame(PlayerList, GamePlayers,
                                                    GameWheel, GameSettings, GameControl)

    # Keep playing the game until it is done or there are problems
    PlayerTurn = 0
    RoundCount = 1
    while result == WOF_globals.RSLT_NONE:
        GamePlayers[0]['RoundTotal'] = 0
        GamePlayers[1]['RoundTotal'] = 0
        GamePlayers[2]['RoundTotal'] = 0
        GameControl['VowelsOnly'] = False
        GameControl['VowelSolveAllowed'] = False
        GameControl['GuessList'] = None
        GameControl['DisplayList'] = None

        #print("\n")
        print(WOF_globals.StringRscs['RoundBanner1'])
        print(WOF_globals.fstr(
            WOF_globals.StringRscs['RoundBanner2'], locals()))
        print(WOF_globals.StringRscs['RoundBanner1'])

        result, RoundPuzzle, GameControl = SelectPuzzle(
            PuzzleDict, GameControl)

        # Keep playing the round until someone finishes
        continueround = True
        while continueround:
            result = ShowPuzzle(RoundPuzzle, GameControl)
            print("%s: $%d    %s: $%d     %s: $%d" %
                  (GamePlayers[0]['Player']['Name'], GamePlayers[0]['RoundTotal'],
                   GamePlayers[1]['Player']['Name'], GamePlayers[1]['RoundTotal'],
                   GamePlayers[2]['Player']['Name'], GamePlayers[2]['RoundTotal']))
            print(WOF_globals.fstr(
                WOF_globals.StringRscs['TurnMessage'], locals()))
            print("\n")

            # Check if all letters have been filled in and give current player a shot to solve the puzzle
            if sum(GameControl['DisplayList']) == len(GameControl['DisplayList']):
                result, GamePlayers[PlayerTurn], GameControl = SolvePuzzle(
                    GamePlayers[PlayerTurn], GameControl, RoundPuzzle)
                if result == WOF_globals.RSLT_ROUNDOVER:
                    continueround = False
                    break

            # Check to see if the puzzle has only vowels. If so, need to branch off to a different algorithm to finish the puzzle
            if GameControl['VowelsOnly']:
                result, GamePlayers, PlayerTurn, GameControl = VowelsOnly(
                    GamePlayers, PlayerTurn, GameControl, RoundPuzzle)
                continueround = False
                break

            input(WOF_globals.fstr(
                WOF_globals.StringRscs['SpinTheWheel'], locals()))
            print("\n")
            spinresult = SpinTheWheel(GameWheel)
            if spinresult != WOF_globals.RSLT_ERROR:
                result, GamePlayers[PlayerTurn], GameControl = EvaluateSpin(
                    spinresult, GamePlayers[PlayerTurn], GameControl, RoundPuzzle)
            else:
                result = WOF_globals.RSLT_ERROR

            if result == WOF_globals.RSLT_ENDTURN:
                # Move to the next player
                PlayerTurn = PlayerTurn + 1
                if PlayerTurn > 2:
                    PlayerTurn = 0
                # Reset if vowels and solving the puzzle are allowed.
                GameControl['VowelSolveAllowed'] = False
            elif result == WOF_globals.RSLT_ROUNDOVER:
                continueround = False

        # The round has been completed
        # Move the players round total over to the game total.
        GamePlayers[PlayerTurn]['GameTotal'] += GamePlayers[PlayerTurn]['RoundTotal']
        print(WOF_globals.fstr(
            WOF_globals.StringRscs['EndRoundCongrats1'], locals()))
        print(WOF_globals.fstr(
            WOF_globals.StringRscs['EndRoundCongrats2'], locals()))
        print(WOF_globals.fstr(
            WOF_globals.StringRscs['EndRoundCongrats3'], locals()))
        input("Press <enter> to continue: ")

        if RoundCount < 2:
            RoundCount += 1
            PlayerTurn = 1
            result = WOF_globals.RSLT_NONE
        else:
            result = WOF_globals.RSLT_FINALROUND

    # The normal part of the game has completed
    # If this was due to normal play, continue to the final round, otherwise just exit.
    if result == WOF_globals.RSLT_FINALROUND:
        result, GamePlayers, GameControl, finalplayer = WOF_finalround.PlayFinalRound(
            GamePlayers, GameControl, PuzzleDict)
        # If the game was completed without error, update the player stats
        for index in range(0, 3):
            GamePlayers[index]['Player']['GamesPlayed'] += 1
            GamePlayers[index]['Player']['TotalWinnings'] += GamePlayers[index]['GameTotal']
            # If the player in the final round, update their win total
            if index == finalplayer:
                GamePlayers[index]['Player']['GamesWon'] += 1
        result = WOF_globals.RSLT_GAMEEND

    return result, PlayerList


## Setup to play the game. Create the game wheel, create the game player data object and pick the order
def InitializeGame(PlayerList, GamePlayers, GameWheel, GameSettings, GameControl):
    result = WOF_globals.RSLT_NONE

    print(WOF_globals.StringRscs['PlayGameBanner'])

    print(WOF_globals.StringRscs['CreateWheel'])
    GameWheel = [WOF_globals.WHEEL_BANKRUPT, WOF_globals.WHEEL_LOSETURN, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800,
                 850, 900, 100, 150, 200, 250, 300]
    if GameSettings['MillionCard']:
        GameWheel[2] = WOF_globals.WHEEL_BANKRUPT2

    ## Initialize the game player data
    GamePlayers[0] = {'Player': PlayerList[0], 'RoundTotal': 0, 'GameTotal': 0}
    GamePlayers[1] = {'Player': PlayerList[1], 'RoundTotal': 0, 'GameTotal': 0}
    GamePlayers[2] = {'Player': PlayerList[2], 'RoundTotal': 0, 'GameTotal': 0}

    # Set the order of the players
    print(WOF_globals.StringRscs['PickingPlayerOrder'])
    random.shuffle(GamePlayers)
    print(WOF_globals.fstr(
        WOF_globals.StringRscs['FirstPlayerOrder'], locals()))
    if GamePlayers[0]['Player']['Bio'] != None:
        print(WOF_globals.fstr(
            WOF_globals.StringRscs['FirstPlayerBio'], locals()))
    print(WOF_globals.fstr(
        WOF_globals.StringRscs['SecondPlayerOrder'], locals()))
    if GamePlayers[1]['Player']['Bio'] != None:
        print(WOF_globals.fstr(
            WOF_globals.StringRscs['SecondPlayerBio'], locals()))
    print(WOF_globals.fstr(
        WOF_globals.StringRscs['ThirdPlayerOrder'], locals()))
    if GamePlayers[2]['Player']['Bio'] != None:
        print(WOF_globals.fstr(
            WOF_globals.StringRscs['ThirdPlayerBio'], locals()))

    # Initialize the values used to manage the games
    GameControl = {'VowelsOnly': False, 'FinalRound': False,
                   'DisplayList': None, 'GuessList': None, 'VowelSolveAllowed': False}

    return result, GameControl, GameWheel

## Select a random choice from the list of puzzles loaded in. Pulling it out of the loaded list
## So that we don't pick the same puzzle again later


def SelectPuzzle(PuzzleDict, GameControl):
    result = WOF_globals.RSLT_ERROR
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
            if Puzzle['Puzzle'][i].isalpha() == False:
                GameControl['DisplayList'][i] = True

        result = WOF_globals.RSLT_NONE

    return result, Puzzle, GameControl

## Display the puzzle, revealing the correctly guessed letters, the clue, and the list of already guessed letters


def ShowPuzzle(RoundPuzzle, GameControl):
    result = WOF_globals.RSLT_NONE

    print("\n")
    print(WOF_globals.StringRscs['ShowPuzzleBanner'])
    displayword = ''
    for i, value in enumerate(GameControl['DisplayList']):
        if value:
            displayword += RoundPuzzle['Puzzle'][i] + ' '
        else:
            displayword += '_ '
    print(displayword)
    print("Clue: " + RoundPuzzle['Clue'])
    if GameControl['GuessList'] != None:
        print(WOF_globals.fstr(
            WOF_globals.StringRscs['ShowGuesses'], locals()))

    print(WOF_globals.StringRscs['ShowPuzzleBanner'])

    return result

## Spin the wheel by randomly picking a spot in the list. Handle the special case where there might be a million spin.


def SpinTheWheel(GameWheel):
    result = WOF_globals.WHEEL_BANKRUPT

    # Make sure we got a valid wheel
    if len(GameWheel) != 0:
        # Spin the wheel by making a randomm selection
        result = random.choice(GameWheel)
        ## If the pick was the special bankruptcy then do another roll to see if they got the million dollar prize.
        ## If they do get that remove it from the wheel by turning the slot into a normal bankruptcy slot. NOTE: only
        ## Available if they change the setting to allow it.
        if result == WOF_globals.WHEEL_BANKRUPT2:
            pick = random.randint(1, 3)
            if pick == 1:
                result = WOF_globals.WHEEL_MILLION
                GameWheel[2] = WOF_globals.WHEEL_BANKRUPT
            else:
                result = WOF_globals.WHEEL_BANKRUPT
    else:
        result = WOF_globals.RSLT_ERROR

    return result

## Play the case where there are only vowels left. Cycle through players who guess a vowel and if it is there
## try to solve the puzzle.


def VowelsOnly(GamePlayers, PlayerTurn, GameControl, RoundPuzzle):
    result = WOF_globals.RSLT_NONE

    print(WOF_globals.StringRscs['VowelsOnlyBanner'])
    input("Press <enter> to continue: ")
    while result != WOF_globals.RSLT_ROUNDOVER:
        # Get the player's guess and check that it's a consonant and hasn't already been guessed
        result = ShowPuzzle(RoundPuzzle, GameControl)
        if sum(GameControl['DisplayList']) == len(GameControl['DisplayList']):
            print("\nThere are no letters remaining....")
            print(WOF_globals.fstr(
                WOF_globals.StringRscs['VowelTurn'], locals()))
            result, Player, GameControl = SolvePuzzle(
                Player, GameControl, RoundPuzzle)
        else:
            print(WOF_globals.fstr(
                WOF_globals.StringRscs['VowelTurn'], locals()))
            GameControl['VowelSolveAllowed'] = True
            invalidinput = True
            userinput = 0
            while invalidinput:
                userinput = input(
                    WOF_globals.StringRscs['VowelsOnlyPrompt']).upper()
                if userinput in ('A', 'E', 'I', 'O', 'U'):
                    if GameControl['GuessList'] == None:
                        invalidinput = False
                    elif userinput not in GameControl['GuessList']:
                        invalidinput = False
                    if len(userinput) == 0:
                        invalidinput = True

            ## Call the function to check how many times the guess is in the puzzle
            numfound, GameControl = CheckGuess(
                userinput, RoundPuzzle, GameControl)
            if numfound == 0:
                Player = GamePlayers[PlayerTurn]
                print(WOF_globals.fstr(
                    WOF_globals.StringRscs['BadGuessMessage'], locals()))
                input("Press <enter> to continue: ")
                result = WOF_globals.RSLT_ENDTURN
            else:
                print(WOF_globals.fstr(
                    WOF_globals.StringRscs['GoodConsGuessMessage'], locals()))

            # result = ShowPuzzle(RoundPuzzle, GameControl)
                Player = GamePlayers[PlayerTurn]
                result, Player, GameControl = SolvePuzzle(
                    Player, GameControl, RoundPuzzle)

        if result == WOF_globals.RSLT_ENDTURN:
            PlayerTurn += 1
            if PlayerTurn > 2:
                PlayerTurn = 0

        # add the guess to the guess list and return that it's the end of the turn
        if GameControl['GuessList'] is None:
            GameControl['GuessList'] = [userinput]
        else:
            GameControl['GuessList'].append(userinput)

    return result, GamePlayers, PlayerTurn, GameControl

## Evaluate the results of the spin. Check for the special cases, otherwise pass on to a function to allow
## The player to take their turn


def EvaluateSpin(SpinResult, Player, GameControl, RoundPuzzle):
    result = WOF_globals.RSLT_NONE

    if SpinResult == WOF_globals.WHEEL_LOSETURN:
        print(WOF_globals.fstr(
            WOF_globals.StringRscs['LoseTurnMessage'], locals()))
        input("Press <enter> to continue: ")
        result = WOF_globals.RSLT_ENDTURN
    elif SpinResult == WOF_globals.WHEEL_BANKRUPT:
        print(WOF_globals.fstr(
            WOF_globals.StringRscs['BankruptMessage'], locals()))
        Player['RoundTotal'] = 0
        input("Press <enter> to continue: ")
        result = WOF_globals.RSLT_ENDTURN
    else:
        result, Player, GameControl = PlayNormalGuess(
            SpinResult, Player, GameControl, RoundPuzzle)

    return result, Player, GameControl


def PlayNormalGuess(SpinResult, Player, GameControl, RoundPuzzle):
    result = WOF_globals.RSLT_NONE

    ## If the player got the million dollar spin substitute in the dollar value.
    ## NOTE: This is a change to the game rules agreed upon in the class. Change later to keep the million card
    ## stored with the player who can only redeem it if they win the final round.
    if SpinResult == WOF_globals.WHEEL_MILLION:
        SpinResult = 1000000000
    print(WOF_globals.fstr(WOF_globals.StringRscs['SpinResult'], locals()))

    invalidturn = True
    ## Check if the puzzle is all filled in and auto-jump to solve the puzzle.
    if sum(GameControl['DisplayList']) == len(GameControl['DisplayList']):
        result, Player, GameControl = SolvePuzzle(
            Player, GameControl, RoundPuzzle)

        invalidturn = False

    ## Show the menu for the player to choose how they want to play their turn

    while invalidturn:

        ## If they can't choose a vowel or to solve, don't do the menu
        if GameControl['VowelSolveAllowed']:
            userinput = 0
            invalidinput = True
            while invalidinput:
                print(WOF_globals.StringRscs['PlayerTurnMenu'])
                userinput = input(WOF_globals.StringRscs['PlayerTurnPrompt'])
                if userinput in ['1', '2', '3']:
                    invalidinput = False
        else:
            userinput = '1'

        ## Go off to the appropriate function to handle what the player selected to do
        if userinput == '1':
            result, Player, GameControl = GuessConsonant(
                SpinResult, Player, GameControl, RoundPuzzle)
            if result != WOF_globals.RSLT_NONE:
                invalidturn = False
        elif userinput == '2':
            result, Player, GameControl = BuyVowel(
                Player, GameControl, RoundPuzzle)
            if result != WOF_globals.RSLT_NONE:
                invalidturn = False
        else:
            result, Player, GameControl = SolvePuzzle(
                Player, GameControl, RoundPuzzle)
            if result != WOF_globals.RSLT_NONE:
                invalidturn = False

    return result, Player, GameControl

## The player wants to guess a consonant


def GuessConsonant(SpinResult, Player, GameControl, RoundPuzzle):
    result = WOF_globals.RSLT_NONE
    result = ShowPuzzle(RoundPuzzle, GameControl)
    print(WOF_globals.StringRscs['ConsonantBanner'])

    # Get the player's guess and check that it's a consonant and hasn't already been guessed
    invalidinput = True
    userinput = 0
    while invalidinput:
        userinput = input(WOF_globals.StringRscs['ConsonantPrompt']).upper()
        if userinput not in ('A', 'E', 'I', 'O', 'U'):
            if GameControl['GuessList'] == None:
                invalidinput = False
            elif userinput not in GameControl['GuessList']:
                invalidinput = False
            if len(userinput) == 0:
                invalidinput = True

    ## Call the function to check how many times the guess is in the puzzle
    numfound, GameControl = CheckGuess(userinput, RoundPuzzle, GameControl)
    if numfound == 0:
        print("\n")
        print(WOF_globals.fstr(
            WOF_globals.StringRscs['BadGuessMessage'], locals()))
        input("Press <enter> to continue: ")
        result = WOF_globals.RSLT_ENDTURN
    else:
        guessamount = numfound * SpinResult
        Player['RoundTotal'] += guessamount
        print("\n")
        print(WOF_globals.fstr(
            WOF_globals.StringRscs['GoodConsGuessMessage'], locals()))
        print(WOF_globals.fstr(
            WOF_globals.StringRscs['GoodConsGuessMessage2'], locals()))
        if IsVowelsOnly(RoundPuzzle, GameControl):
            GameControl['VowelsOnly'] = True
        GameControl['VowelSolveAllowed'] = True
        result = WOF_globals.RSLT_SPINAGAIN

    # add the guess to the guess list
    if GameControl['GuessList'] is None:
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
            if RoundPuzzle['Puzzle'][i] not in ('A', 'E', 'I', 'O', 'U'):
                result = False
                break

    return result

## Count how many times the guessed character is part of the puzzle. If so, change the display list to show


def CheckGuess(Guess, Puzzle, GameControl):
    count = 0

    # Quick check to see if the guess is in the puzzle
    count = Puzzle['Puzzle'].count(Guess)
    # If it is there, we need to find all the locations to set DisplayList to allow revealing that character in the puzzle
    if count > 0:
        startindex = 0
        # Start at the left and keep finding occurrences
        for i in range(0, count):
            index = Puzzle['Puzzle'].find(Guess, startindex)
            GameControl['DisplayList'][index] = True
            startindex = index + 1
            if startindex >= len(GameControl['DisplayList']):
                startindex = len(GameControl['DisplayList'])-1

    return count, GameControl

# Player wants to buy a vowel


def BuyVowel(Player, GameControl, RoundPuzzle):
    result = WOF_globals.RSLT_NONE

    # Check to see if it is allowed to buy a vowel
    if((GameControl['VowelSolveAllowed']) and Player['RoundTotal'] >= 250):

        Player['RoundTotal'] -= 250

        result = ShowPuzzle(RoundPuzzle, GameControl)

        print(WOF_globals.StringRscs['VowelBanner'])
        # Get the player's guess and check that it's a vowel and hasn't already been guessed
        invalidinput = True
        userinput = 0
        while invalidinput:
            userinput = input(WOF_globals.StringRscs['VowelPrompt']).upper()
            if userinput in ('A', 'E', 'I', 'O', 'U'):
                if GameControl['GuessList'] == None:
                    invalidinput = False
                elif userinput not in GameControl['GuessList']:
                    invalidinput = False
                if len(userinput) == 0:
                    invalidinput = True

        ## Call the function to check how many times the guess is in the puzzle
        numfound, GameControl = CheckGuess(userinput, RoundPuzzle, GameControl)
        if numfound == 0:
            print("\n")
            print(WOF_globals.fstr(
                WOF_globals.StringRscs['BadGuessMessage'], locals()))
            input("Press <enter> to continue: ")
            result = WOF_globals.RSLT_ENDTURN
        else:
            print("\n")
            print(WOF_globals.fstr(
                WOF_globals.StringRscs['GoodConsGuessMessage'], locals()))
            result = WOF_globals.RSLT_SPINAGAIN
        # add the incorrect guess to the guess list and return that it's the end of the turning
        if GameControl['GuessList'] is None:
            GameControl['GuessList'] = [userinput]
        else:
            GameControl['GuessList'].append(userinput)

    else:
        print("\n")
        print(WOF_globals.StringRscs['CantBuyVowel'])

    return result, Player, GameControl

## Player wants to solve the puzzle


def SolvePuzzle(Player, GameControl, RoundPuzzle):
    result = WOF_globals.RSLT_NONE

    userinput = 0
    if GameControl['VowelSolveAllowed']:
        result = ShowPuzzle(RoundPuzzle, GameControl)
        print(WOF_globals.StringRscs['SolveBanner'])
        # Get the player's guess and check that it's not empty
        print("Guesses must be entered exactly with all punctuation. Capitalization doesn't matter, though.")
        invalidinput = True
        while invalidinput:
            userinput = input(WOF_globals.StringRscs['SolvePrompt']).upper()
            if len(userinput) > 0:
                invalidinput = False
    else:
        print("\n")
        print(WOF_globals.StringRscs['CantSolvePuzzle'])

    if GameControl['VowelSolveAllowed']:
        if userinput == RoundPuzzle['Puzzle']:
            print("\n")
            print(WOF_globals.StringRscs['SolveSuccessBanner'])
            print(WOF_globals.fstr(
                WOF_globals.StringRscs['SolveSuccessMessage'], locals()))
            print(WOF_globals.StringRscs['SolveSuccessBanner'])

            result = WOF_globals.RSLT_ROUNDOVER
        else:
            print(WOF_globals.fstr(
                WOF_globals.StringRscs['SolveFailMessage'], locals()))
            result = WOF_globals.RSLT_ENDTURN

    return result, Player, GameControl
