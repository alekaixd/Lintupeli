import mysql.connector
import bcrypt
from flask import Flask, request, jsonify, send_file, g, Blueprint, session, current_app

key = current_app.config['SECRET_KEY']

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

user_bp = Blueprint('user_bp', __name__)

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


@user_bp.teardown_app_request
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@user_bp.route('/fly/<ICAO>', methods=['GET'])
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


@user_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    username = data["username"]
    password = data["password"]

    sql = "SELECT password_hash FROM user WHERE username=%s"
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    if result is None:
        return (jsonify(success=False))

    storedHash = result[0].encode()

    if bcrypt.checkpw(password.encode(), storedHash):
        session["user_id"] = result[0]
        return (jsonify(success=True))
    else:
        return (jsonify(success=False))


@user_bp.route('/createUser', methods=['POST'])
def createUser():

    data = request.get_json()

    username = data["username"]
    password = data["password"]

    if (not username):
        return jsonify(success=False, message="Give a username!")

    if (not password):
        return jsonify(success=False, message="Give a password!")

    try:

        import bcrypt
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        InsertUser(username, hashed_password)

        sql = "SELECT player_id FROM user WHERE username = %s"
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql, (username,))
        result = cursor.fetchone()

        if result:
            session["user_id"] = result[0]
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Could not fetch user ID")

    except Exception as e:
        return jsonify(success=False, message="Username already exists")


def InsertUser(username, password):
    db = get_db()
    cursor = db.cursor()

    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode(), salt)

    sql = "INSERT INTO user (username, password_hash) VALUES (%s, %s)"
    cursor.execute(sql, (username, hashedPassword.decode()))
