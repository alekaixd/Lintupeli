import Database
import MigrationScript
import Player

"""
This script is used for the main game loop logic
"""


def main():
    # starting point

    # "login" user
    #   ask for screen name
    # ask for save
    #   load game/new game
    #       new game => ask for bird name
    #       load game => select your bird
    # start game
    # print info
    # choose action
    #   fly
    #       choose how long to fly (longer distance => more risk)
    #   eat (raises max energy)
    #   rest (restores all energy)
    #   quit game
    #       save game
    # day cycle
    #   change location
    #   change weather
    #   change energy
    #   change date (optional)
    # check if energy is depleted
    # check if winter is coming
    # check for win condition
    # loop back

    winCondition = False
    # Database.checkForSave()
    while winCondition is False:
        action = input("Choose action ('fly', 'eat', 'rest' or 'quit'): ")
        if action == "fly":
            flyLength = 0
            while flyLength == 0:  # Inputting might be changed here.
                try:
                    flyLength = int(input("How long to fly? "))
                    if flyLength == 0:
                        print("cant be 0")
                except ValueError:
                    print("Please only input integers")
            # fly
            print("flying...")
        elif action == "eat":
            Player.eat()  # unwritten function
        elif action == "rest":
            Player.rest()
        elif action == "quit":
            saveAction = ""
            while saveAction != "y" or saveAction != "n":
                saveAction = input("Save game (y/n)? ")
                if saveAction == "y":
                    Database.saveGame()  # unwritten function
                elif saveAction == "n":
                    return
        else:
            print("Wrong input")

    return


main()
