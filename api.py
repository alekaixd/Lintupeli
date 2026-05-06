from flask import Flask
from flask_cors import CORS
from apidb import user_bp
import Player
# import Database

app = Flask(__name__)

CORS(app)


app.register_blueprint(user_bp)


@app.route('/eat', methods=['GET'])
def EatFood():
    return Player.eat()


@app.route('/chirp', methods=['GET'])
def Chirp():
    return {"addedScore": Player.chirp()}


if __name__ == "__main__":
    app.run(debug=True, port=3000)
