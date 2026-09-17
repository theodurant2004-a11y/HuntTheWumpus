from flask import Blueprint, render_template, session, redirect, url_for, request
from wumpus_engine import mazeGeneration
from routes.auth import login_required, get_db_connection
import os

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
@login_required
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
#   Game Lobby
#====================
@game_bp.route('/gameLobby')
@login_required
def gameLobby():
    return render_template('gameLobby.html')

#====================
#   Difficulty Select
#====================
@game_bp.route('/difficultySelect', methods=['GET', 'POST'])
@login_required
def difficultySelect():
    if request.method == 'POST':
        # Récupération et stockage des choix en session
        difficulty = int(request.form.get('difficulty', 1))
        game_avatar = request.form.get('avatar', session.get('joueur_avatar', '1.png'))
        blind_mode = request.form.get('blind_mode') == '1'
        express_mode = request.form.get('express_mode') == '1'

        session['difficulty'] = difficulty
        session['game_avatar'] = game_avatar
        session['blind_mode'] = blind_mode
        session['express_mode'] = express_mode

        # Redirige vers gameScreen (dans l'iframe)
        return redirect(url_for('game.gameScreen'))

    # GET : affichage du formulaire de sélection
    from flask import current_app
    avatar_dir = os.path.join(current_app.static_folder, 'ASSETS', 'IMAGES', 'iconProfil')
    try:
        avatars = [f for f in os.listdir(avatar_dir) if f.endswith('.png')]
        avatars.sort(key=lambda x: int(x.split('.')[0]))
    except FileNotFoundError:
        avatars = []

    return render_template('difficultySelect.html', avatars=avatars)

#====================
#   gameScreen
#====================
@game_bp.route('/gameScreen')
@login_required
def gameScreen():
    DIFFICULTY = session.get('difficulty', 1)
    game_avatar = session.get('game_avatar', session.get('joueur_avatar', '1.png'))

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

    # game_over=False : partie qui commence, rien à révéler
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze, game_over=False, coming_from=None)

#====================
#   Mouvement
#====================
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

            # si le joueur est sur une chauve-souris on stop
            for y in range(len(new_vision)):
                for x in range(len(new_vision[0])):
                    if new_vision[y][x] == 2:
                        if x != -1 and bats_maze[y][x] > 0:
                            break

            next_move = mazeGeneration.get_next_corridor_direction(maze, new_vision, coming_from_hist)

            if next_move == NONE:
                break

            new_vision = mazeGeneration.move(maze, new_vision, next_move, coming_from_hist, bats_maze)

    # Actualisation session
    session['vision_maze'] = new_vision
    session['coming_from_hist'] = coming_from_hist
    session.modified = True

    # Gestion du blind mode
    display_vision = new_vision
    if blind_mode:
        display_vision = [[cell if cell == 2 else 0 for cell in row] for row in new_vision]

    # coming_from = dernière direction mémorisée (pour positionner le joueur dans le couloir)
    coming_from = coming_from_hist[-1] if coming_from_hist else None

    # game_over=False : la défaite par piège est détectée côté Jinja2
    return render_template('gameScreen.html', maze=maze, vision_maze=display_vision, bats=bats_maze, game_over=False, coming_from=coming_from)

#====================
#   Tir
#====================
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

    if direction != NONE:
        game_won = mazeGeneration.get_arrow_outcome(maze, vision_maze, direction)
    else:
        game_won = None

    if game_won:
        con, cur = get_db_connection()
        try:
            user_id = session['joueur_id']
            cur.execute("UPDATE users SET nbvictory = nbvictory + 1 WHERE id = %s", (user_id,))
            con.commit()
        finally:
            cur.close()
            con.close()

    # coming_from = dernière direction mémorisée
    coming_from_hist = session.get('coming_from_hist', [])
    coming_from = coming_from_hist[-1] if coming_from_hist else None

    # game_over=True uniquement si tir résolu (victoire ou défaite), pas si annulé (None)
    game_over = game_won is not None
    return render_template('fire.html', maze=maze, vision_maze=vision_maze, bats=bats_maze, game_won=game_won, game_over=game_over, coming_from=coming_from)