import WOF_globals
import WOF_maingame
import random


def PlayFinalRound(GamePlayers, GameControl, PuzzleDict):
    result =WOF_globals.RSLT_NONE

    GameControl['DisplayList'] = None
    GameControl['GuessList'] = WOF_globals.FinalRoundLetters
    GameControl['VowelSolveAllowed'] = True

    # Determine which player gets to move into the final round.
    max = 0
    winner = -1
    for index in range(0,3):
        if GamePlayers[index]['GameTotal'] > max:
            max = GamePlayers[index]['GameTotal']
            winner = index
        elif GamePlayers[index]['GameTotal'] == max:
            if max == -1:
                winner = index
            else:
                coin = random.randint(0,1)
                if coin == 0:
                    winner = index
    if winner == -1:
        result = WOF_globals.RSLT_ERROR

    if result == WOF_globals.RSLT_NONE:            
        FinalPlayer = GamePlayers[winner]
        print(f"\n\nFINAL ROUND\n")
        print(f"Congratulation, {FinalPlayer['Player']['Name']} on making it to the final round")
        print(f"You will play for a cash prize of $100,000")
        print(f"<cheers><cheers>")
        print("You will start with the letters R-S-T-L-N-E filled in and then select three additional consonants and one vowel.")

        # Create the puzzles
        result, RoundPuzzle, GameControl = WOF_maingame.SelectPuzzle(PuzzleDict, GameControl)

        # Call WOF_maingame.CheckGuess on the 6 starter guesses and show the puzzle
        for i, value in enumerate(WOF_globals.FinalRoundLetters):
            numfound, GameControl = WOF_maingame.CheckGuess(value, RoundPuzzle, GameControl)
        result = WOF_maingame.ShowPuzzle(RoundPuzzle, GameControl)

        # Have the player enter 3 consonants
        for i in range(0,3):
            invalidinput = True
            userinput = 0
            while invalidinput:
                userinput = input(WOF_globals.fstr(WOF_globals.StringRscs['FinalRoundConsonantPrompt'], locals())).upper()
                if userinput not in ('A', 'E', 'I', 'O', 'U'):
                    if GameControl['GuessList'] == None:
                        invalidinput = False
                    elif userinput not in GameControl['GuessList']:
                        invalidinput = False
                    if len(userinput)==0:
                        invalidinput = True

            numfound, GameControl = WOF_maingame.CheckGuess(userinput, RoundPuzzle, GameControl)
            GameControl['GuessList'].append(userinput)

        # Have the player enter 1 vowel
        invalidinput = True
        userinput = 0
        while invalidinput:
            userinput = input(
                WOF_globals.StringRscs['FinalRoundVowelPrompt']).upper()
            if userinput in ('A', 'E', 'I', 'O', 'U'):
                if GameControl['GuessList'] == None:
                    invalidinput = False
                elif userinput not in GameControl['GuessList']:
                    invalidinput = False
                if len(userinput)==0:
                    invalidinput = True

        numfound, GameControl = WOF_maingame.CheckGuess(userinput, RoundPuzzle, GameControl)


        result, FinalPlayer, GameControl = WOF_maingame.SolvePuzzle(FinalPlayer, GameControl, RoundPuzzle)
        if result == WOF_globals.RSLT_ROUNDOVER:
            print(WOF_globals.StringRscs['FinalRoundWinnerBanner1'])
            print(WOF_globals.StringRscs['FinalRoundWinnerBanner2'])
            print(WOF_globals.StringRscs['FinalRoundWinnerBanner3'])
            print(WOF_globals.StringRscs['FinalRoundWinnerBanner2'])
            print(WOF_globals.StringRscs['FinalRoundWinnerBanner1'])
            print("\n\n")
            print(WOF_globals.fstr(WOF_globals.StringRscs['FinalRoundWinnerMessage1'], locals()))
            FinalPlayer['GameTotal'] += 100000
            print(WOF_globals.fstr(WOF_globals.StringRscs['FinalRoundWinnerMessage2'], locals()))
        elif result == WOF_globals.RSLT_ENDTURN:
            print(WOF_globals.StringRscs['FinalRoundLoserBanner1'])
            print(WOF_globals.StringRscs['FinalRoundLoserBanner1'])
            print(WOF_globals.StringRscs['FinalRoundLoserBanner2'])
            print(WOF_globals.StringRscs['FinalRoundLoserBanner1'])
            print(WOF_globals.StringRscs['FinalRoundLoserBanner1'])
            print("\n\n")
            print(WOF_globals.fstr(WOF_globals.StringRscs['FinalRoundLoserMessage'], locals()))

        # Show the final puzzle
        GameControl['DisplayList'] = [True]*len(RoundPuzzle['Puzzle'])
        result = WOF_maingame.ShowPuzzle(RoundPuzzle, GameControl)


    return result, GamePlayers, GameControl, winner

