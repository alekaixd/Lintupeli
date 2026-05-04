from flask import Flask
from flask_cors import CORS
from apidb import user_bp
import Player
# import Database

app = Flask(__name__)

app.secret_key = "9f3c1a7d8b2e4f6a9c0d1e3f5a7b9c2d4e6f8a0b1c3d5e7f9a2b4c6d8e0f1"

CORS(app)


app.register_blueprint(user_bp)


@app.route('/eat', methods=['GET'])
def EatFood():
    return {"addedEnergy": Player.eat()}


@app.route('/chirp', methods=['GET'])
def Chirp():
    return {"addedScore": Player.chirp()}


if __name__ == "__main__":
    app.run(debug=True, port=3000)
