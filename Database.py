#ONLY DATABASE FETCHES HERE
import mysql.connector

connection = None

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

def FetchLocation(ICAO, sqlConnection):
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{ICAO}'"
    cursor = sqlConnection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if(cursor.rowcount > 0):
        for row in result:
            return print(row)
    else:
        return print("No location for that ICAO")

def FetchAirportName(ICAO, sqlConnection):
    sql = f"SELECT airport.name FROM airport WHERE ident='{ICAO}'"
    cursor = sqlConnection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if(cursor.rowcount > 0):
        for row in result:
            return print(row)
    else:
        return print("No airport name for that ICAO")

Connect()
FetchAirportName("EFHK", connection)
FetchLocation("EFHK", connection)