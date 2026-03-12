from flask import Blueprint, render_template, session, redirect, url_for
from wumpus_engine import mazeGeneration
from routes.auth import login_required, get_db_connection

TOP = 99
BOTTOM = 98
LEFT = 97
RIGHT = 96

# TMP
DIFFICULTY = 1
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

@game_bp.route('/Maze')
@login_required
def showMaze():
    if 'maze' not in session:
        return redirect(url_for('game.gameScreen'))
    
    maze = session['maze']
    vision_maze = session['vision_maze']
    coming_from_hist = session['coming_from_hist']
    bats_maze = session['bats_maze']

    # TODO : faire en sorte que ça ne soit pas TOP mais une valeur qui dis qu'on ne se déplace pas vraiment
    vision_maze = mazeGeneration.move(maze, vision_maze, 5, coming_from_hist, bats_maze)

    # session['vision_maze'] = vision_maze
    # session['coming_from_hist'] = coming_from_hist

    session.modified = True
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)

@game_bp.route('/move/up')
@login_required
def moveUp():
    if 'maze' not in session:
        return redirect(url_for('game.gameScreen'))

    maze = session['maze']
    vision_maze = session['vision_maze']
    coming_from_hist = session['coming_from_hist']
    bats_maze = session['bats_maze']

    vision_maze = mazeGeneration.move(maze, vision_maze, TOP, coming_from_hist, bats_maze)

    session['vision_maze'] = vision_maze
    session['coming_from_hist'] = coming_from_hist

    session.modified = True
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)

@game_bp.route('/move/down')
@login_required
def moveDown():
    if 'maze' not in session:
        return redirect(url_for('game.gameScreen'))
    
    maze = session['maze']
    vision_maze = session['vision_maze']
    coming_from_hist = session['coming_from_hist']
    bats_maze = session['bats_maze']

    vision_maze = mazeGeneration.move(maze, vision_maze, BOTTOM, coming_from_hist, bats_maze)

    session['vision_maze'] = vision_maze
    session['coming_from_hist'] = coming_from_hist

    session.modified = True
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)

@game_bp.route('/move/left')
@login_required
def moveLeft():
    if 'maze' not in session:
        return redirect(url_for('game.gameScreen'))
    
    maze = session['maze']
    vision_maze = session['vision_maze']
    coming_from_hist = session['coming_from_hist']
    bats_maze = session['bats_maze']

    vision_maze = mazeGeneration.move(maze, vision_maze, LEFT, coming_from_hist, bats_maze)

    session['vision_maze'] = vision_maze
    session['coming_from_hist'] = coming_from_hist

    session.modified = True
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)

@game_bp.route('/move/right')
@login_required
def moveRight():
    if 'maze' not in session:
        return redirect(url_for('game.gameScreen'))
    
    maze = session['maze']
    vision_maze = session['vision_maze']
    coming_from_hist = session['coming_from_hist']
    bats_maze = session['bats_maze']

    vision_maze = mazeGeneration.move(maze, vision_maze, RIGHT, coming_from_hist, bats_maze)

    session['vision_maze'] = vision_maze
    session['coming_from_hist'] = coming_from_hist

    session.modified = True
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)