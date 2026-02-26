from flask import Blueprint, render_template, session
from wumpus_engine import mazeGeneration
from routes.auth import login_required

game_bp = Blueprint('game', __name__)

@game_bp.route('/podiumScreen')
@login_required#c'est le sécuriter du décorateur - Plus besoin de faire le "if session..."
def podiumScreen():
    return render_template('podiumScreen.html')

@game_bp.route('/gameScreen')
@login_required
def gameScreen():
    maze = mazeGeneration.generateMaze(1)
    avatar_du_joueur = session.get('joueur_avatar', '1.png') 
    #c'est au cas ou y a un bug dans la session, on s'en fous de l'avatar donc on en donne un par défault si il en a pas 
    return render_template('gameScreen.html', maze=maze)