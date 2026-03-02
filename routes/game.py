from flask import Blueprint, render_template, session
from wumpus_engine import mazeGeneration
from routes.auth import login_required, get_db_connection

TOP = 99
BOTTOM = 98
LEFT = 97
RIGHT = 96

# TMP
DIFFICULTY = 2

maze = []
vision_maze = []
coming_from_hist = []
bats_maze = []
####################

game_bp = Blueprint('game', __name__)

@game_bp.route('/podiumScreen')
@login_required#c'est le sécuriter du décorateur - Plus besoin de faire le "if session..."
def podiumScreen():
    con, cur = get_db_connection()
    try:
        # On sélectionne le pseudo au lieu de l'email
        cur.execute("SELECT pseudo, avatar, nbVictory FROM users ORDER BY nbVictory DESC")
        players = cur.fetchall()
    finally:
        cur.close()
        con.close()

    return render_template('podiumScreen.html', players=players)

@game_bp.route('/gameScreen')
@login_required
def gameScreen():
    global vision_maze, coming_from_hist, maze, bats_maze

    avatar_du_joueur = session.get('joueur_avatar', '1.png') 
    #c'est au cas ou y a un bug dans la session, on s'en fous de l'avatar donc on en donne un par défault si il en a pas 

    #TODO
    #mettre en variable session
    maze = mazeGeneration.generateMaze(DIFFICULTY)
    vision_maze = [[0 for _ in range(8)] for _ in range(6)]
    coming_from_hist = []
    bats_maze = mazeGeneration.generateBats(DIFFICULTY)
    ###########################

    spawnpoint = mazeGeneration.starting_point(maze)
    vision_maze[spawnpoint[1]][spawnpoint[0]] = 2

    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)

@game_bp.route('/move/up')# si fin de partie afficher tout le labyrinthe
@login_required
def moveUp():
    global vision_maze
    vision_maze = mazeGeneration.move(maze, vision_maze, TOP, coming_from_hist)
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)

@game_bp.route('/move/down')
@login_required
def moveDown():
    global vision_maze
    vision_maze = mazeGeneration.move(maze, vision_maze, BOTTOM, coming_from_hist)
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)

@game_bp.route('/move/left')
@login_required
def moveLeft():
    global vision_maze
    vision_maze = mazeGeneration.move(maze, vision_maze, LEFT, coming_from_hist)
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)

@game_bp.route('/move/right')
@login_required
def moveRight():
    global vision_maze
    vision_maze = mazeGeneration.move(maze, vision_maze, RIGHT, coming_from_hist)
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)
