from flask import Blueprint, render_template
from wumpus_engine import mazeGeneration

game_bp = Blueprint('game', __name__)

@game_bp.route('/podiumScreen')
def podiumScreen():
    return render_template('podiumScreen.html')

@game_bp.route('/gameScreen')
def gameScreen():
    maze = mazeGeneration.generateMaze(1)
    return render_template('gameScreen.html', maze=maze)