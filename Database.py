# ONLY DATABASE FETCHES HERE
import mysql.connector
import bcrypt

connection = None
currentUserId = None
currentGameId = None

open("loginCredentials.txt", "a").close()
open("databaseLoginCredentials.txt", "a").close()

def SaveLoginCredentials(username, passwordHash):
    with open("loginCredentials.txt", "w") as f:
        f.write(f"username = {username}\n")
        f.write(f"password hash = {passwordHash.decode()}\n")


def GetLoginCredentials():
    username = ""
    passwordHash = ""

    with open("loginCredentials.txt", "r") as f:
        for line in f:
            key, values = line.strip().split("=")
            key = key.strip()
            values = values.strip()

            if (key == "username"):
                username = values
            if (key == "password hash"):
                passwordHash = values

    return (username, passwordHash)

def SaveDatabaseLoginCredentials(user, password):
    with open("databaseLoginCredentials.txt", "w") as f:
        f.write(f"username = {user}\n")
        f.write(f"password = {password}\n")


def GetDatabaseLoginCredentials():
    username = ""
    password = ""

    with open("databaseLoginCredentials.txt", "r") as f:
        for line in f:
            key, value = line.strip().split("=")
            key = key.strip()
            value = value.strip()

            if(key == "username"):
                username = value
            if(key == "password"):
                password = value

    return(username, password)


# creates SQL connection and saves it to global variable connection


def SqlConnect(user, password):
    global connection
    try:
        connect = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='bird_game',
            user=user,
            password=password,
            autocommit=True
        )
        if (connect.is_connected()):
            print(f"Is connected!")
            connection = connect
            return True
    except:
        print("Couldn't log in!")
        return False


def Connect():
    dbUsername, dbPassword = GetDatabaseLoginCredentials()

    if(dbUsername != "" and dbPassword != ""):
        if(SqlConnect(dbUsername, dbPassword) is True):
            print("Database auto-login successfull!")
            return
    else:
        while True:
            user = input("Database username: ")
            password = input("Database password: ")
            if (user != "" and password != ""):
                if (SqlConnect(user, password) is True):
                    SaveDatabaseLoginCredentials(user, password)
                    break
            else:
                print("Anna nimi ja salasana!")


Connect()


def FetchLocation(ICAO):
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident=%s"
    cursor = connection.cursor()
    cursor.execute(sql, (ICAO,))
    result = cursor.fetchall()
    if (result):
        return result[0]
    else:
        return print("No location for that ICAO")


def FetchAirportName(ICAO):
    sql = f"SELECT airport.name FROM airport WHERE ident='{ICAO}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if (result):
        return result[0][0]
    else:
        return print("No airport name for that ICAO")


def CreateUserOrLogin():
    global currentUserId

    while True:
        try:
            command = int(
                input("Would you like to login (1) or create a new user (2): "))
        except ValueError:
            print("Incorrect input!")
            continue

        if (command == 1):
            username = input("Username: ")
            password = input("Password: ")

            sql = "SELECT password_hash, player_id FROM user WHERE username = %s"
            cursor = connection.cursor()
            cursor.execute(sql, (username,))
            result = cursor.fetchone()

            if (result is None):
                print("User not found! Try again!")
                continue

            storedHash = result[0].strip().encode()

            if (bcrypt.checkpw(password.encode(), storedHash)):
                print("Login successful")
                currentUserId = result[1]

                SaveLoginCredentials(username, storedHash)

                return ()
            else:
                print("Wrong password or username")

        elif (command == 2):
            username = input("Username: ")
            password = input("Password: ")

            if (username == ""):
                print("Give a username!")
                continue
            if (password == ""):
                print("Give a password!")
                continue

            try:
                InsertUser(username, password)
                print("User created successfully!")
                break
            except Exception:
                print("Username already exists! Please choose another.")
                continue
        else:
            print("Incorrect input")

# Inserts data into the given table from the given dictionary

def InsertUser(username, password):
    cursor = connection.cursor()

    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode(), salt)

    sql = "INSERT INTO user (username, password_hash) VALUES (%s, %s)"
    cursor.execute(sql, (username, hashedPassword.decode()))

    if cursor.rowcount > 0:
        print("User created successfully")
    else:
        print("No user was inserted")


def InsertScore(player_id, total_score, days_survived, game_id):
    cursor = connection.cursor()

    sql = f"INSERT INTO scores (player_id, total_score, days_survived, game_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (player_id, total_score, days_survived, game_id))

    if cursor.rowcount > 0:
        print("Score inserted")
    else:
        print("No score inserted")

def InsertGame (location, currentEnergy, maxEnergy, speciesName, status, score, gameId=None):
    #muista player id
    playerId = currentUserId

    if gameId is None:
        sql = f"INSERT INTO game (location, current_energy, max_energy, species_name, player_id, status, score) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql,(location, currentEnergy, maxEnergy, speciesName, playerId, status, score))
        print("New game created!")
        SetCurrentGameId()
    else:
        sql = f"UPDATE game SET location = %s, current_energy = %s, max_energy = %s, species_name = %s, status = %s, score = %s WHERE id = %s"

        cursor.execute(sql,(location, currentEnergy, maxEnergy, speciesName, status, score, gameId))
        print("Game saved!")

def SetCurrentGameId():
    global currentGameId
    sql = f"SELECT id FROM game WHERE player_id = {currentUserId} AND status = 'ongoing'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
    currentGameId = result[0]


def LoadGame():
    savedGames = FetchGameData(currentUserId)
    if len(savedGames) > 0:
        loadInput = input("Found saved games. Do you want to continue(y/n)? ")
        if loadInput == "y":
            ChooseGame(savedGames)
        else:
            return


def FetchGameData(userId, status="ongoing"):
    sql = "SELECT location, current_energy, max_energy, species_name, score FROM game WHERE status=%s AND player_id=%s"
    cursor = connection.cursor()
    cursor.execute(sql, (status, userId))
    games = cursor.fetchall()
    return games

def FetchScoresData():
    sql = f"SELECT scores.total_score, user.username, game.species_name FROM user JOIN scores ON scores.player_id = user.player_id JOIN game ON game.id = scores.game_id AND game.player_id = user.player_id WHERE game.status = 'completed'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def ChooseGame(games):
    i = 1
    for game in games:
        location, current_energy, max_energy, species_name, score = game
        print(f"{i}. {species_name} | Location: {location} | Energy: {
              current_energy}/{max_energy} | Score: {score}")
        i += 1
        while True:
            try:
                choice = int(input("Choose a game to load: ")) - 1
                if 0 <= choice < len(games):
                    return games[choice]
                else:
                    print("Give a valid number!")
            except:
                print("Please enter a valid number.")

username, passwordHash = GetLoginCredentials()

if (username != "" and passwordHash != ""):
    sql = "SELECT password_hash, player_id FROM user WHERE username = %s"
    cursor = connection.cursor()
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    if result:
        hash = result[0].strip()

        if hash == passwordHash:
            print("Auto login successfull!")
            currentUserId = result[1]
        else:
            print("Saved user or password invalid!")
            CreateUserOrLogin()
    else:
        print("Saved user not found!")
        CreateUserOrLogin()
else:
    CreateUserOrLogin()

"""
Game taululle:
values = {"location":location,
          "current_energy":currentEnergy,
          "max_energy":maxEnergy,
          "species_name":speciesName,
          "player_id":currentUserId
          }
          
Scores taululle:
values = {"player_id":currentUserId,
        "total_score":totalScore,
        "days_survived":date
        "game_id":currentGameId

InsertInto("game", values)"""
