import mysql.connector
import bcrypt
from flask import Flask, request, jsonify, send_file, g, Blueprint, current_app
import MigrationScript
from geopy import distance


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


MigrationScript.InitMap()


@user_bp.route('/fly/<ICAO>', methods=['GET'])
def FlyToLocation(ICAO):
    try:
        currentICAO = request.args.get('currentICAO')
        combo = float(request.args.get('combo'))
        sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident=%s"
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql, (ICAO,))
        result = cursor.fetchall()
        if currentICAO != None:
            dist = round(CalculateDistance(currentICAO, ICAO))
            energyUsed = round(dist/10)
            gainedScore = CalculateFlightScore(combo, energyUsed)
        else:
            dist = 0
            energyUsed = 0
            gainedScore = 0

        pos = result[0]
        locationData = {
            "ICAO": ICAO,
            "lat": pos[0],
            "lon": pos[1],
            "distance": dist,
            "energyUsed": energyUsed,
            "gainedScore": gainedScore
        }
        return locationData
    except Exception as e:
        return f"invalid ICAO code: {e}"


def CalculateDistance(icao1: str, icao2: str):
    i1 = FetchLocation(icao1)
    i2 = FetchLocation(icao2)
    dist = distance.distance(i1, i2).km
    return dist


def CalculateFlightScore(combo: int, energyUsed: int):
    return energyUsed * combo * 2


def FetchLocation(ICAO):
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident=%s"
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql, (ICAO,))
    result = cursor.fetchall()
    if (result):
        return result[0]
    else:
        return 0


@user_bp.route('/start', methods=['GET'])
def GetFirstICAO():
    try:
        port = MigrationScript.GetFirstPort()
        sql = f"SELECT ident, name, latitude_deg, longitude_deg FROM airport WHERE ident='{
            port}'"
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        firstPort = {
            "icao": result[0][0],
            "name": result[0][1],
            "lat": result[0][2],
            "lon": result[0][3]
        }
        return firstPort
    except Exception as e:
        return f"invalid ICAO code: {e}"


@user_bp.route('/map/<ICAO>', methods=['GET'])
def GetNextMaps(ICAO):
    try:
        ports = MigrationScript.GetNextPort(ICAO)
        portData = {"Ports": {}}
        db = get_db()
        cursor = db.cursor()
        for i, port in enumerate(ports):
            sql = f"SELECT name FROM airport WHERE ident='{port}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            dist = round(CalculateDistance(ICAO, port))
            portData["Ports"][i] = {"icao": port,
                                    "name": result[0][0],
                                    "distance": dist}

        return portData
    except Exception as e:
        return f"invalid ICAO code: {e}"


@user_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    username = data["username"]
    password = data["password"]

    sql = f"SELECT player_id, password_hash FROM user WHERE username='{username}'"
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()

    if result is None:
        return jsonify(success=False)

    user_id = result[0]

    print(user_id)

    storedHash = result[1].encode()

    if bcrypt.checkpw(password.encode(), storedHash):
        return jsonify(success=True, user_id = user_id)

    return jsonify(success=False)


@user_bp.route('/createUser', methods=['POST'])
def createUser():

    data = request.get_json()

    username = data["username"]
    password = data["password"]

    if not username:
        return jsonify(success=False, message="Give a username!")

    if not password:
        return jsonify(success=False, message="Give a password!")

    success = InsertUser(username, password)

    if not success:
        return jsonify(success=False, message="Username already exists")

    db = get_db()
    cursor = db.cursor()

    sql = "SELECT player_id FROM user WHERE username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    player_id = result[0]

    return jsonify(success=True, player_id = player_id)


def InsertUser(username, password):
    db = get_db()
    cursor = db.cursor()

    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode(), salt)

    sql = "INSERT INTO user (username, password_hash) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (username, hashedPassword.decode()))
        db.commit()
        return True

    except mysql.connector.IntegrityError:
        db.rollback()
        return False


@user_bp.route('/difficulty', methods=['POST'])
def Difficulty():

    data = request.get_json()

    name = data["name"]
    maxEnergy = data["maxEnergy"]

    return jsonify(success=True, name = name, maxEnergy = maxEnergy)

"""
@user_bp.route("/logout", methods=["POST"])
def Logout():
    session.clear()
    return jsonify(success=True)
"""


@user_bp.route("/oldGameData")
def OldGameData():
    userId = request.args.get("userId")

    games = FetchGameData(userId)

    result = []

    for game in games:
        result.append({
            "id": game[0],
            "location": game[1],
            "current_energy": game[2],
            "max_energy": game[3],
            "species_name": game[4],
            "score": game[5]
        })

    return jsonify(result)


def FetchGameData(userId, status="saved"):
    db = get_db()
    cursor = db.cursor()
    sql = "SELECT id, location, current_energy, max_energy, species_name, score FROM game WHERE status=%s AND player_id=%s"
    cursor.execute(sql, (status, userId))
    games = cursor.fetchall()
    return games
