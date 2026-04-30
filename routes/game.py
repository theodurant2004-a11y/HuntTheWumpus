from flask import Blueprint, render_template, session, redirect, url_for
from wumpus_engine import mazeGeneration
from routes.auth import login_required, get_db_connection

TOP = 99
BOTTOM = 98
LEFT = 97
RIGHT = 96
NONE = -1

# TMP --> à récuprer en session
DIFFICULTY = 1
BLIND_MODE = False
EXPRESS_MODE = False # à intégrer
#############

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
    avatar_du_joueur = session.get('joueur_avatar', '1.png') 
    #c'est au cas ou y a un bug dans la session, on s'en fous de l'avatar donc on en donne un par défault si il en a pas 

    maze = mazeGeneration.generateMaze(DIFFICULTY)
    vision_maze = [[0 for _ in range(8)] for _ in range(6)]
    coming_from_hist = []
    bats_maze = mazeGeneration.generateBats(DIFFICULTY)

    spawnpoint = mazeGeneration.starting_point(maze)
    vision_maze[spawnpoint[1]][spawnpoint[0]] = 2

    session['maze'] = maze
    session['vision_maze'] = vision_maze
    session['coming_from_hist'] = coming_from_hist
    session['bats_maze'] = bats_maze

    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)



@game_bp.route('/move/<direction>')
@login_required
def handle_move(direction):
    if 'maze' not in session:
        return redirect(url_for('game.gameScreen'))

    directions_map = {
        'up': TOP,
        'down': BOTTOM,
        'left': LEFT,
        'right': RIGHT,
        'none': NONE
    }

    move_val = directions_map.get(direction, NONE)

    maze = session['maze']
    vision_maze = session['vision_maze']
    coming_from_hist = session['coming_from_hist']
    bats_maze = session['bats_maze']

    new_vision = mazeGeneration.move(maze, vision_maze, move_val, coming_from_hist, bats_maze)

    session['vision_maze'] = new_vision
    session['coming_from_hist'] = coming_from_hist
    session.modified = True

    display_vision = new_vision
    if BLIND_MODE:
        display_vision = [[cell if cell == 2 else 0 for cell in row] for row in new_vision]

    return render_template('gameScreen.html', maze=maze, vision_maze=display_vision, bats=bats_maze)