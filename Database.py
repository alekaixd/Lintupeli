# ONLY DATABASE FETCHES HERE
import mysql.connector
import bcrypt

connection = None
currentUserId = None
currentGameId = None

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
    while True:
        user = input("Database username: ")
        password = input("Database password: ")
        if (SqlConnect(user, password) is True):
            break
    return ()


Connect()

def FetchLocation(ICAO):
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{
        ICAO}'"
    cursor = connection.cursor()
    cursor.execute(sql)
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
    command = int(
        input("Would you like to login (1) or create a new user (2): "))
    if (command == 1):
        global currentUserId
        username = input("Username: ")
        password = input("Password: ")
        sql = f"SELECT password_hash, player_id FROM user WHERE username = '{
            username}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        storedHash = result[0].strip().encode()
        if(result is None):
            print("User not found!")
            CreateUserOrLogin()
            return()
        else:
            if (bcrypt.checkpw(password.encode(), storedHash)):
                print("login successful")
                currentUserId = result[1]
                return()
            else:
                print("Couldn't log in!")
                CreateUserOrLogin()

    if (command == 2):
        username = input("Username: ")
        password = input("Password: ")

        mydict = {
            'username': username,
            'password_hash': password,
        }

        InsertInto("user", mydict)
        return ()


# Inserts data into the given table from the given dictionary
def InsertInto(tableName: str, dictionary: dict):
    cursor = connection.cursor()

    if (tableName == "user"):

        password = dictionary['password_hash']
        username = dictionary['username']

        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(password.encode(), salt)

        sql = f"INSERT INTO {
            tableName} (username, password_hash) VALUES ( %s ,%s );"
        cursor.execute(sql, (username, hashedPassword.decode()))
    else:
        columns = ', '.join(str(x).replace('/', '_')
                            for x in dictionary.keys())
        values = ', '.join("'" + str(x).replace('/', '_') +
                           "'" for x in dictionary.values())

        sql = f"INSERT INTO %s ( %s ) VALUES ( %s );" % (
            tableName, columns, values)
        cursor.execute(sql)

    if (cursor.rowcount > 0):
        print("Data was successfully saved")
    else:
        print("No data was inserted")

def SetCurrentGameId():
    global currentGameId
    sql = f"SELECT id FROM game WHERE player_id = {currentUserId} AND status = 'ongoing'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
    currentGameId = result[0]

def UpdateGameStatus(newStatus, gameId):
    sql = "UPDATE game SET status = %s WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(sql, (newStatus, gameId))
    connection.commit()

def SaveGame():
    SetCurrentGameId()

    if currentGameId is not None:
        status = input("Give game status (ongoing/completed): ")
        UpdateGameStatus(status, currentGameId)
        print("Game saved")
    else:
        print("No game to save")

def FetchGameData(userId, status="ongoing"):
    sql = "SELECT location, current_energy, max_energy, species_name, score FROM game WHERE status=%s AND user_id=%s"
    cursor = connection.cursor()
    cursor.execute(sql, (status, userId))
    games = cursor.fetchall()
    return games

def ChooseGame(games):
    i = 1
    for game in games:
        location, current_energy, max_energy, species_name, score = game
        print(f"{i}. {species_name} | Location: {location} | Energy: {current_energy}/{max_energy} | Score: {score}")
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

def FetchScoresData():
    sql = f"SELECT "

#games = FetchGameData(currentUserId)
#ChooseGame(games)
#CreateUserOrLogin()

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
