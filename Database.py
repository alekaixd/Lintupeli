#ONLY DATABASE FETCHES HERE
import mysql.connector
import bcrypt

connection = None
currentUserId = None

# creates SQL connection and saves it to global variable connection
def SqlConnect(user, password):
    global connection
    try:
        connect = mysql.connector.connect(
            host = 'localhost',
            port = 3306,
            database = 'bird_game',
            user = user,
            password = password,
            autocommit = True
        )
        if (connect.is_connected()):
            print (f"Is connected!")
            connection = connect
            return True
    except:
        print("Couldn't log in!")
        return False

def Connect():
    while True:
        user = input("Give database user: ")
        password = input("Give database users password: ")
        if(SqlConnect(user, password) is True):
            break
    return()

Connect()

def FetchLocation(ICAO):
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{ICAO}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if(result):
        return result[0][0]
    else:
        return print("No location for that ICAO")

def FetchAirportName(ICAO):
    sql = f"SELECT airport.name FROM airport WHERE ident='{ICAO}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if(result):
        return result[0][0]
    else:
        return print("No airport name for that ICAO")

def CreateUserOrLogin ():
    command = int(input("Would you like to login (1) or create a new user (2): "))
    if(command == 1):
        global currentUserId
        username = input("Username: ")
        password = input("Password: ")
        sql = f"SELECT password_hash, player_id FROM user WHERE username = '{username}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
        storedHash = result[0].encode()
        if(bcrypt.checkpw(password.encode(), storedHash)):
            print("login successful")
            currentUserId = result[1]
            return()

    if(command == 2):
        username = input("Username: ")
        password = input("Password: ")

        mydict = {
            'username': username,
            'password_hash': password,
        }

        InsertInto("user", mydict)
        return ()


#Inserts data into the given table from the given dictionary
def InsertInto(tableName: str, dictionary: dict):
    cursor = connection.cursor()

    if(tableName == "user"):

        password = dictionary['password_hash']
        username = dictionary['username']

        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(password.encode(), salt)

        sql = f"INSERT INTO {tableName} (username, password_hash) VALUES ( %s ,%s );"
        cursor.execute(sql, (username, hashedPassword.decode()))
    else:
        columns = ', '.join(str(x).replace('/', '_') for x in dictionary.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in dictionary.values())

        sql = f"INSERT INTO %s ( %s ) VALUES ( %s );" % (tableName, columns, values)
        cursor.execute(sql)

    if(cursor.rowcount > 0):
        print("Data was successfully saved")
    else:
        print("No data was inserted")

CreateUserOrLogin()