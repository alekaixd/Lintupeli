import Database
import MigrationScript
import Player
from geopy import distance

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
        print(f"\nCurrent airport: {Database.FetchAirportName(
            currentAirport)}")
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
                    print("\nchoose where to fly\n")

                    for i, f in enumerate(flights):
                        print(f"({i + 1}) fly to {
                              Database.FetchAirportName(f)}")
                        print(f"Distance to destination is {
                              CalculateDistance(currentAirport, f):.0f}km\n")
                    cancelCall = False
                    while True:  # ik while true is bad but atleast its not chatgpt
                        flyInput = input(
                            f"Input number (1 - {len(flights)}) or cancel with (c): ")
                        if flyInput == "c":
                            print("cancelling...")
                            cancelCall = True
                            break
                        elif 0 < int(flyInput) <= len(flights):
                            chosenDestination = flights[int(flyInput) - 1]
                            break
                        else:
                            print("Wrong input")
                            flyinput = None
                    if cancelCall is True:
                        continue

                else:  # if only 1 destination
                    cancelCall = False
                    while True:
                        print(f"\nfly to {
                              Database.FetchAirportName(flights[0])}")
                        print(f"Distance to destination is {
                              CalculateDistance(currentAirport, flights[0]):.0f}km")
                        flyinput = input("Do you want to fly (y/n)")
                        if flyinput == 'y':
                            break
                        elif flyinput == 'n':
                            cancelCall = True
                            break
                        else:
                            print("Wrong input")
                    if cancelCall is True:
                        continue
                    chosenDestination = flights[0]

                # if player flew
                input(f"flap flap... you soar the skies towards {
                      Database.FetchAirportName(chosenDestination)}.\n(any key to continue...) ")
                currentAirport = chosenDestination

            else:  # if player at the end
                input("You migrated successfully!!1!1 :D")
                winCondition = True

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


def CalculateDistance(icao1: str, icao2: str):
    i1 = Database.FetchLocation(icao1)
    i2 = Database.FetchLocation(icao2)
    dist = distance.distance(i1, i2).km
    return dist


main()
