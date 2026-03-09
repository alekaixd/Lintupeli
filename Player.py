# HERE ARE ALL THE FUNCTIONS AND OTHER STUFF FOR THE PLAYERS STATS

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

import random

# Player Actions


def newgame_intro():
    print("Welcome to Bird Game!")
    print("=" * 40)
    print("\nYou are a bird trying to survive the winter.")
    print("Manage your energy wisely to reach your safe destination.")
    input("\nPress 'Enter' to get started!\n")


def move_forward(energy):
    loss = random.randint(5, 10)
    energy -= loss
    print(f"You moved forward and lost {loss} energy.")
    return energy


def eat():
    gain = random.randint(4, 12)
    print(f"You ate some food and gained {gain} max energy.")
    input("(Enter to continue)")
    return gain


# Check game status

def check_energy(energy):
    if energy <= 0:
        print("Your no energy left. You lost the game!")
        return False
    return True


# Game loop
"""
def game():
    playing = True

    print("Game started! Your energy:", energy)

    while playing:
        print("\nChoose action:")
        print("1 - Move Forward")
        print("2 - Rest")
        print("3 - Eat")

        choice = input("Type here--> ")

        if choice == "1":
            energy = move_forward(energy)
        elif choice == "2":
            energy = rest(energy)
        elif choice == "3":
            energy = eat(energy)
        else:
            print("Invalid choice.")
            continue

        print("Current energy:", energy)
        playing = check_energy(energy)
"""

# --- Start Game ---
# game()
