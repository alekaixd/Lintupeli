import Database
import MigrationScript
import Player
from geopy import distance
import platform
import os

"""
This script is used for the main game loop logic
"""

currentGameId = None

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

    global currentGameId

    Clear()
    Player.newgame_intro()

    MigrationScript.InitMap()
    winCondition = False

    savedGame = Database.LoadGame()
    if savedGame:
        # Load data from saved game
        currentAirport = savedGame[0]
        energy = savedGame[1]
        maxEnergy = savedGame[2]
        birdName = savedGame[3]
        score = savedGame[4]
        currentGameId = Database.SetCurrentGameId()
    else:
        # Start new game
        bird = Player.choose_bird()
        birdName = bird[0]
        energy = bird[1]
        maxEnergy = energy
        score = 0
        currentAirport = MigrationScript.GetFirstPort()
        Database.InsertGame(currentAirport, energy, maxEnergy, birdName, score, "ongoing")
        currentGameId = Database.SetCurrentGameId()

    notMoved = 0

    while winCondition is False:
        Clear()
        if notMoved >= 3:
            LoseGame(1)
        print(f"Current airport: {Database.FetchAirportName(
            currentAirport)}")
        print(f"Energy: {energy:.0f}/{maxEnergy}")
        print(f"Score: {int(score)}")
        action = input(
            "Write action (fly, chirp, eat, sleep or quit): ")

        if action == "fly" or action == "f":
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

                energyUsed = round(CalculateDistance(
                    currentAirport, chosenDestination)) / 10
                energy -= energyUsed
                if energy <= 0:
                    LoseGame(0)

                score += energyUsed

                # if player flew
                print(f"\nflap flap... The {birdName} soars the skies towards {
                      Database.FetchAirportName(chosenDestination)}.")
                print(f"You lost {energyUsed:.0f} energy")
                input("(Enter to continue)")
                currentAirport = chosenDestination
                notMoved = 0

            else:  # if player at the end
                input("You migrated successfully!!1!1 :D")
                winCondition = True

        elif action == "eat" or action == "e":
            addEnergy = Player.bird_food_find(birdName)
            maxEnergy += addEnergy
            energy += addEnergy
            notMoved += 1
        elif action == "sleep" or action == "s":
            energy = maxEnergy
            input("You slept well and restored all your energy!\n(Enter to continue)")
            notMoved += 1
        elif action == "chirp" or action == "c":
            score += 50
            input(
                "chirp chirp!\nLocal residents are happy! + 50 points :D\n(Enter to continue)")
            notMoved += 1
        elif action == "quit" or action == "q":
            saveAction = ""
            while saveAction != "y" or saveAction != "n":
                saveAction = input("Save game (y/n)? ")
                if saveAction == "y":
                    Database.InsertGame(currentAirport, energy, maxEnergy, birdName, int(score), gameId=currentGameId)
                    return
                elif saveAction == "n":
                    Database.DeleteGame(currentGameId)
                    return
        else:
            print("Wrong input")

    return


def CalculateDistance(icao1: str, icao2: str):
    i1 = Database.FetchLocation(icao1)
    i2 = Database.FetchLocation(icao2)
    dist = distance.distance(i1, i2).km
    return dist


def LoseGame(reason: int):
    global currentGameId
    Database.DeleteGame(currentGameId)
    if reason == 0:
        print("You ran out of energy and you fell from the sky :(")
    elif reason == 1:
        print("The cold caught up to you. You lose D:")
    quit()


def Clear():  # if for some reason clear command is different
    if platform.system() == "Linux":
        os.system('clear')
    elif platform.system() == "Windows":
        os.system('cls')


def CalculateFlightScore(combo: int):
    return


main()
