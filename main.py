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

    MigrationScript.InitMap()
    winCondition = False
    score = 0
    currentAirport = MigrationScript.GetFirstPort()
    # Database.checkForSave()
    while winCondition is False:
        print(f"Current airport: {Database.FetchAirportName(
            currentAirport, Database.connection)}")
        action = input(
            "Write action (fly, chirp, eat, rest or quit): ")
        if action == "fly" or action == "f":

            # get flight locations from MigrationScript
            # calculate distance between locations
            # get energy levels from Player
            # distance < energy * 10
            #   good
            # else
            #   bad
            flights = MigrationScript.GetNextPort(currentAirport)
            chosenDestination = None
            if len(flights) >= 1:  # if destinations exist
                if len(flights) > 1:  # if more than 1 destination
                    print("choose where to fly: ")
                    for i, f in enumerate(flights):
                        print(f"({i + 1}) fly to {
                              Database.FetchAirportName(f, Database.connection)}")
                    flyInput = int(
                        input(f"Input number (1 - {len(flights)}): "))
                    chosenDestination = flights[flyInput - 1]
                else:  # if only 1 destination
                    chosenDestination = flights[0]
                input(f"flap flap... you soar the skies towards {
                      Database.FetchAirportName(chosenDestination, Database.connection)}. (any key to continue...) ")
                currentAirport = chosenDestination
            else:
                input("nowhere to fly. (any key to continue...)")

        elif action == "eat" or action == "e":
            Player.eat()  # unwritten function
        elif action == "rest" or action == "r":
            Player.rest()
        elif action == "chirp" or action == "c":
            score += 50
            print("chirp chirp!\nLocal residents are happy! + 50 points :D")
        elif action == "quit" or action == "q":
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
