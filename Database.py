#ONLY DATABASE FETCHES HERE
import mysql.connector

connection = None
currentUserId = None

def Connect():
    user = input("Give database user: ")
    password = input("Give database users password: ")
    SqlConnect(user, password)
    return ()


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

def CreateUser (sqlConnection):
    global currentUserId
    username = input("Username: ")
    password = input("Password: ")
    sql = f"INSERT INTO user ('')"


def FetchLocation(ICAO, sqlConnection):
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{ICAO}'"
    cursor = sqlConnection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if(result):
        return result[0][0]
    else:
        return print("No location for that ICAO")

def FetchAirportName(ICAO, sqlConnection):
    sql = f"SELECT airport.name FROM airport WHERE ident='{ICAO}'"
    cursor = sqlConnection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if(result):
        return result[0][0]
    else:
        return print("No airport name for that ICAO")



def InsertInto(tableName: str, values: dict, sqlConnection):
    if (tableName == "game" or tableName == "scores"):
        #LAITA TÄHÄN, ETTÄ LISÄÄ NOITTEN DICTIONARYN ASIOITTEN LISÄKSI CURRENT_USER_ID:N!

mydict = {
    'location' : 'EFHK',
    'currentEnergy' : '50',
    'maxEnergy' : '100',
    'species_name' : 'pulla sorsa',
    'playerId' : 'id'
}

Connect()
#FetchAirportName("EFHK", connection)
#FetchLocation("EFHK", connection)