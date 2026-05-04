from flask import Flask
from flask_cors import CORS
from apidb import user_bp
import MigrationScript
import Player
import os
# import Database

app = Flask(__name__)

CORS(app)

MigrationScript.InitMap()

app.register_blueprint(user_bp)

app.secret_key = os.urandom(24)

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


if __name__ == "__main__":
    app.run(debug=True, port=3000)


