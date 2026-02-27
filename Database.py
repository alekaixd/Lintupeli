#ONLY DATABASE FETCHES HERE
import mysql.connector

def SqlLoginCheck(user, password):
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            port = 3306,
            database = 'bird_game',
            user = user,
            password = password,
            autocommit = True
        )
        if (connection.is_connected()):
            print("Is connected!")
            return
    except:
        print("Couldn't log in!")