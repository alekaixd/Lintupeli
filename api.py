from flask import Flask
import MigrationScript
import Player
import Database

app = Flask(__name__)
MigrationScript.InitMap()


@app.route('/map/<ICAO>', methods=['GET'])
def GetNextMaps(ICAO):
    try:
        return MigrationScript.GetNextPort(ICAO)
    except Exception as e:
        return f"invalid ICAO code: {e}"


@app.route('/eat', methods=['GET'])
def EatFood():
    return {"addedEnergy": Player.eat()}


@app.route('/chirp', methods=['GET'])
def Chirp():
    return {"addedScore": Player.chirp()}


@app.route('/fly/<ICAO>', methods=['GET'])
def FlyToLocation(ICAO):
    try:
        pos = Database.FetchLocation(ICAO)
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
