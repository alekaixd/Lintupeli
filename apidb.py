import mysql.connector
from flask import Flask, request, jsonify, send_file, g
from flask_cors import CORS


def GetDatabaseLoginCredentials():
    username = ""
    password = ""

    with open("databaseLoginCredentials.txt", "r") as f:
        for line in f:
            key, value = line.strip().split("=")
            key = key.strip()
            value = value.strip()

            if (key == "username"):
                username = value
            if (key == "password"):
                password = value

    return (username, password)


usr, passwd = GetDatabaseLoginCredentials()

app = Flask(__name__)

pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_size=5,
    host='localhost',
    database='bird_game',
    user=usr,
    password=passwd,
    port=3306
)


def get_db():
    if 'db' not in g:
        g.db = pool.get_connection()
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close


@app.route('/fly/<ICAO>', methods=['GET'])
def FlyToLocation(ICAO):
    try:
        sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident=%s"
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql, (ICAO,))
        result = cursor.fetchall()

        pos = result[0]
        locationData = {
            "ICAO": ICAO,
            "lon": pos[0],
            "lat": pos[1]
        }
        return locationData
    except Exception as e:
        return f"invalid ICAO code: {e}"


if __name__ == "__main__":
    app.run(debug=True, port=3000)
