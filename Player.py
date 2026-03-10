import random

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

def check_energy(energy):
    if energy <= 0:
        print("Your no energy left. You lost the game!")
        return False
    return True

def choose_bird():
    birds = {
        "1": {"name": "Eagle", "energy": 50, "difficulty": "Easy"},
        "2": {"name": "Raven", "energy": 45, "difficulty": "Easy"},
        "3": {"name": "Sparrow", "energy": 40, "difficulty": "Medium"},
        "4": {"name": "Hawk", "energy": 35, "difficulty": "Medium"},
        "5": {"name": "Owl", "energy": 30, "difficulty": "Hard"},
        "6": {"name": "Pigeon", "energy": 32, "difficulty": "Hard"}
    }
        
    print("\nChoose your bird:")
    for key, bird in birds.items():
        print(f"{key} - {bird['name']} (Starting energy: {bird['energy']})")
        
    while True:
        choice = input("\nEnter number (1-5): ")
        if choice in birds:
            selected = birds[choice]
            print(f"\nYou chose {selected['name']}! Difficulty: {selected['difficulty']}")
            return selected["name"], selected["energy"] #tämä palauttaa linnun nimen ja energia määrän pelaajan valinnan mukaan :)
        else:
            print("Invalid choice. Please enter 1-5.")

def eat(bird_name):
    foods = {
        "worm": 8,
        "seeds": 5,
        "berry": 5,
        "insect": 8,
        "grain": 2,
        "fish": 10
        }
                    
    food = random.choice(list(foods.keys()))
    energy_gain = foods[food]
    print(f"{bird_name} found a {food}! You received {energy_gain} energy points.")
    input("(Enter to continue)")
    return energy_gain

def choose_weather():
    weathers = {
        "storm": {"multiplier": 1.4, "description": "A terrible storm is approaching!"},
        "rain": {"multiplier": 1.2, "description": "It's raining heavily."},
        "windy": {"multiplier": 1.1, "description": "Strong winds are blowing."},
        "sunny": {"multiplier": 1.0, "description": "Beautiful sunny weather!"}
    }
        
    weather = random.choice(list(weathers.keys()))
    weather_data = weathers[weather]
    print(f"\nWeather: {weather_data['description']}")
    print(f"Energy loss multiplier: {weather_data['multiplier']}x")
        
    return weather_data["multiplier"] #Tämä palauttaa sen pistemäärittäjä kertoimen :)
