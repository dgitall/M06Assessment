
import WOF_globals
import WOF_mainmenu
import WOF_maingame



## The Main Application where everything starts and ends
def MainApplication():
    result = WOF_globals.RSLT_NONE

    PlayerList = list()
    PuzzleDict = dict()
    GameSettings = dict()

    PuzzleDict, PlayerList, GameSettings = WOF_mainmenu.ApplicationStartup()

    WOF_mainmenu.ContestantSignin(PlayerList)

    # Get User Input and direct to the function dealing with the selection
    while result != WOF_globals.RSLT_STOP:
        print(WOF_globals.StringRscs['MainMenu'])
        UserInput = input(WOF_globals.StringRscs['MenuPrompt'])
        if UserInput == '1':
            pass
            result, PlayerList = WOF_maingame.PlayGame(PuzzleDict, PlayerList, GameSettings)
            if(result == WOF_globals.RSLT_GAMEEND):
                WOF_mainmenu.ShowPlayerStats(PlayerList)
        elif UserInput == '2':
            pass
            result = WOF_mainmenu.DisplayDirections()
        elif UserInput == '3':
            pass
            result = WOF_mainmenu.ShowPlayerStats(PlayerList)
        elif UserInput == '4':
            pass
            result = WOF_mainmenu.ChangeSettings(GameSettings)
        elif UserInput == '5':
            result = WOF_mainmenu.ExitGame(PlayerList)


    return result



## Main Body of the application
MainApplication()
