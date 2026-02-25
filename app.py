from flask import Flask
import os
from dotenv import load_dotenv

from routes.auth import auth_bp
from routes.game import game_bp

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
app.register_blueprint(auth_bp)
app.register_blueprint(game_bp)

if __name__ == '__main__':
    app.run(debug=True)