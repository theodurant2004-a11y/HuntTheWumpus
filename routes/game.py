from flask import Blueprint, render_template, session, redirect, url_for
from wumpus_engine import mazeGeneration
from routes.auth import login_required, get_db_connection, login

TOP = 99
BOTTOM = 98
LEFT = 97
RIGHT = 96
NONE = -1

game_bp = Blueprint('game', __name__)

#====================
#   PodiumScreen
#====================
@game_bp.route('/podiumScreen')
@login_required#c'est le sécuriter du décorateur - Plus besoin de faire le "if session..."
def podiumScreen():
    con, cur = get_db_connection()
    try:
        cur.execute("SELECT pseudo, avatar, nbvictory FROM users ORDER BY nbVictory DESC")
        players = cur.fetchall()
    finally:
        cur.close()
        con.close()

    return render_template('podiumScreen.html', players=players)

#====================
#   gameScreen
#====================
@game_bp.route('/gameScreen')
@login_required
def gameScreen():
    avatar_du_joueur = session.get('joueur_avatar', '1.png')
    DIFFICULTY = session.get('difficulty', 1)
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

    blind_mode = session.get('blind_mode', False)
    express_mode = session.get('express_mode', False) 
    maze = session['maze']
    vision_maze = session['vision_maze']
    coming_from_hist = session['coming_from_hist']
    bats_maze = session['bats_maze']

    new_vision = mazeGeneration.move(maze, vision_maze, move_val, coming_from_hist, bats_maze)

    # Gestion du mode express
    if express_mode and move_val != NONE:
        while mazeGeneration.is_in_corridor(maze, new_vision):
            
            # si le joueur est sur une chauve souris on stop
            for y in range(len(new_vision)):
                for x in range(len(new_vision[0])):
                    if new_vision[y][x] == 2:

                        # si on passe sur une chauve souris ou stop
                        if x != -1 and bats_maze[y][x] > 0:
                            break

            # determination du prochain mouvement automatique
            next_move = mazeGeneration.get_next_corridor_direction(maze, new_vision, coming_from_hist)
            
            if next_move == NONE:
                break
                
            # execution du mouvement automatique
            new_vision = mazeGeneration.move(maze, new_vision, next_move, coming_from_hist, bats_maze)

    #actualisation des variables sessions
    session['vision_maze'] = new_vision
    session['coming_from_hist'] = coming_from_hist
    session.modified = True

    # Gestion du blind mode
    display_vision = new_vision
    if blind_mode:
        display_vision = [[cell if cell == 2 else 0 for cell in row] for row in new_vision]

    return render_template('gameScreen.html', maze=maze, vision_maze=display_vision, bats=bats_maze)

@game_bp.route('/shoot/<direction>')
@login_required
def handle_shoot(direction):
    if 'maze' not in session:
        return redirect(url_for('game.gameScreen'))

    directions_map = {
        'up': TOP,
        'down': BOTTOM,
        'left': LEFT,
        'right': RIGHT,
        'none': NONE
    }

    direction = directions_map.get(direction, NONE)
    bats_maze = session['bats_maze']
    maze = session['maze']
    vision_maze = session['vision_maze']

    #mecanique de tir
    if(direction != NONE):
        game_won = mazeGeneration.get_arrow_outcome(maze, vision_maze, direction)
        #return avec la victoire ou la défaite
    else:
        game_won = None

    if( game_won ):
        # ajouter la modification en DB pour dire +1 en nombre de victoire
        con, cur = get_db_connection()
        try:
            # On sélectionne le pseudo au lieu de l'email
            user_id = session['joueur_id']
            cur.execute("UPDATE users SET nbvictory = nbvictory + 1 WHERE id = %s", (user_id,))
            con.commit()
        finally:
            cur.close()
            con.close()
    return render_template('fire.html', maze=maze, vision_maze=vision_maze, bats=bats_maze, game_won=game_won)