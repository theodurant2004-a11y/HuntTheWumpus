from random import randint, sample, choice
# code à optimiser avec dictionnaire pour les couloir
# calcul de set(all_coords - corridor_spots) pour calculer les case restantes rapidement
# all(cell == 1 ...) pour verifier plus rapidement que toutes les case de la matrice verif sont à 1

CAVERN = 0
PATH1 = 1
PATH2 = 2
SLIMEPIT = 3
SLIMEMARKED = 4
BLOODMARKED = 5
SLIMENBLOOD = 6
WUMPUS = 7

TOP = 99
BOTTOM = 98
LEFT = 97
RIGHT = 96
NONE = -1

def create_maze(difficulty):
    maze = [[CAVERN for _ in range(8)] for _ in range(6)]

    if difficulty == 1 :
        corridor = randint(8, 14)
    elif difficulty == 2 :
        corridor = 18
    elif difficulty == 3 :
        corridor = 26

    #remplissage de la matrice avec les cases couloir
    all_coord = []
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            all_coord.append((x,y))

    chosen_spots = sample(all_coord, corridor)#tirage sans remise dans 'all_cord' un nombre 'corridor' de fois

    for (x, y) in chosen_spots:
        maze[y][x] = choice([PATH1, PATH2]) # prend un élément au hasard dans la liste avec remise

    #ajout du wumpus et des puis
    spots_left = []
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 0:
                spots_left.append((x,y))
    
    random_point = sample(spots_left, 3)

    wx, wy = random_point[0]
    maze[wy][wx] = WUMPUS

    px1, py1 = random_point[1]
    maze[py1][px1] = SLIMEPIT

    px2, py2 = random_point[2]
    maze[py2][px2] = SLIMEPIT

    return maze

def floodfill(matrix, verification_matrix, x, y, coming_from, visited_states):
    x = x % len(matrix[0]) # fait en sorte que si on dépasse de la matrice on fait le tour et va à l'endroit correspondant
    y = y % len(matrix)
    current_state = (x, y, coming_from)

    if not current_state in visited_states:
        visited_states.add(current_state)# ajoute l'état de la visite
        verification_matrix[y][x] = 1 # dis qu'on est passé au moins une fois par cette case
        case_type = matrix[y][x] #reucpère le type de la case

        next_x, next_y = x, y
        next_coming_from = -1
        direction_found = False

        # determination du prochain floodfill en fonction du type de virage
        if case_type == PATH1:
            if coming_from == LEFT:
                next_y = y - 1
                next_coming_from = BOTTOM
                direction_found = True
            elif coming_from == TOP:
                next_x = x - 1
                next_coming_from = RIGHT
                direction_found = True
            elif coming_from == RIGHT:
                next_y = y + 1
                next_coming_from = TOP
                direction_found = True
            elif coming_from == BOTTOM:
                next_x = x + 1
                next_coming_from = LEFT
                direction_found = True

        elif case_type == PATH2:
            if coming_from == LEFT:
                next_y = y + 1
                next_coming_from = TOP
                direction_found = True
            elif coming_from == TOP:
                next_x = x + 1
                next_coming_from = LEFT
                direction_found = True
            elif coming_from == RIGHT:
                next_y = y - 1
                next_coming_from = BOTTOM
                direction_found = True
            elif coming_from == BOTTOM:
                next_x = x - 1
                next_coming_from = RIGHT
                direction_found = True

        # applique le floodFill en fonction de la case sur laquelle on est
        elif case_type == CAVERN:
            floodfill(matrix, verification_matrix, x-1, y, RIGHT, visited_states)
            floodfill(matrix, verification_matrix, x+1, y, LEFT, visited_states)
            floodfill(matrix, verification_matrix, x, y-1, BOTTOM, visited_states)
            floodfill(matrix, verification_matrix, x, y+1, TOP, visited_states)

        if direction_found:
            floodfill(matrix, verification_matrix, next_x, next_y, next_coming_from, visited_states)

#point de départ utilisé pour faire le floodfill et point de départ du joueur
def starting_point(maze):
    good_to_start = False
    while not good_to_start:
        x = randint(0,7)
        y = randint(0,5)
        if maze[y][x] == CAVERN or maze[y][x] == SLIMEMARKED or maze[y][x] == BLOODMARKED or maze[y][x] == SLIMENBLOOD:
            good_to_start = True
    return (x, y)
        
# verification du fonctionnement du floodfill
def floodfill_worked(verification_maze):
    worked = True
    y = len(verification_maze)
    
    while y > 0 and worked:
        y -= 1
        x = len(verification_maze[y])
        while x > 0 and worked:
            x -= 1
            if verification_maze[y][x] == 0:
                worked = False
    
    return worked

def floodmark(matrix, x, y, coming_from, floodtype, floodsize):
    x = x % len(matrix[0])
    y = y % len(matrix)
    case_type = matrix[y][x]

    next_x, next_y = x, y
    next_coming_from = -1
    direction_found = False

    if case_type == PATH1:# faire le dicionnaire
        if coming_from == LEFT:
            next_y = y - 1
            next_coming_from = BOTTOM
            direction_found = True
        elif coming_from == TOP:
            next_x = x - 1
            next_coming_from = RIGHT
            direction_found = True
        elif coming_from == RIGHT:
            next_y = y + 1
            next_coming_from = TOP
            direction_found = True
        elif coming_from == BOTTOM:
            next_x = x + 1
            next_coming_from = LEFT
            direction_found = True

    elif case_type == PATH2:
        if coming_from == LEFT:
            next_y = y + 1
            next_coming_from = TOP
            direction_found = True
        elif coming_from == TOP:
            next_x = x + 1
            next_coming_from = LEFT
            direction_found = True
        elif coming_from == RIGHT:
            next_y = y - 1
            next_coming_from = BOTTOM
            direction_found = True
        elif coming_from == BOTTOM:
            next_x = x - 1
            next_coming_from = RIGHT
            direction_found = True

    if not (case_type == WUMPUS or case_type == SLIMEPIT or direction_found):
        if case_type == CAVERN:
            matrix[y][x] = floodtype
        elif case_type != floodtype:
            matrix[y][x] = SLIMENBLOOD

    # applique le floodFill en fonction de la case sur laquelle on est
    if floodsize > 0 and not direction_found:
        floodmark(matrix, x-1, y, RIGHT, floodtype, floodsize-1)
        floodmark(matrix, x+1, y, LEFT, floodtype, floodsize-1)
        floodmark(matrix, x, y-1, BOTTOM, floodtype, floodsize-1)
        floodmark(matrix, x, y+1, TOP, floodtype, floodsize-1)

    if direction_found:
        floodmark(matrix, next_x, next_y, next_coming_from, floodtype, floodsize)

def putmarks(maze):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == SLIMEPIT:
                floodmark(maze, x, y, -1, SLIMEMARKED, 1)
            elif maze[y][x] == WUMPUS:
                floodmark(maze, x, y, -1, BLOODMARKED, 2)

def generateMaze(difficulty):
    maze_valid = False
    while not maze_valid:
        maze = create_maze(difficulty)
        verification_maze = [[0 for j in range(8)] for i in range (6)]
        starting_pos = starting_point(maze)
        states = set()# set qui premet de vérifier si on rentre dans une case de la même manière plusieurs fois
        floodfill(maze, verification_maze, starting_pos[0], starting_pos[1], -1, states)
        maze_valid = floodfill_worked(verification_maze)
    # si le labyrinthe est valide on regarde pour mettre les tâches de sang et de slime.
    putmarks(maze)

    return maze

def generateBats(difficulty):
    bats = [[0 for _ in range(8)] for _ in range(6)]
    all_coord = []
    for y in range(len(bats)):
        for x in range(len(bats[0])):
            all_coord.append((x,y))

    if difficulty == 1:
        nb_bats = 1
    elif difficulty == 2 or difficulty == 3:
        nb_bats = 2

    chosen_spots = sample(all_coord, nb_bats)

    for (x, y) in chosen_spots:
        bats[y][x] = 1
    
    return bats

def move(maze, vision_maze, direction, coming_from_hist, bats):
    for y in range(len(vision_maze)):
        for x in range(len(vision_maze[0])):
            if vision_maze[y][x] == 2:
                case_type = maze[y][x]

                if not player_bats_interaction(maze, vision_maze, bats, x, y) and direction != -1:

                    if direction == TOP:
                        new_y = (y - 1) % len(vision_maze)
                        new_x = x
                        coming_from = BOTTOM
                    elif direction == BOTTOM:
                        new_y = (y + 1) % len(vision_maze)
                        new_x = x
                        coming_from = TOP
                    elif direction == LEFT:
                        new_y = y
                        new_x = (x - 1) % len(vision_maze[0])
                        coming_from = RIGHT
                    elif direction == RIGHT:
                        new_y = y
                        new_x = (x + 1) % len(vision_maze[0])
                        coming_from = LEFT

                    if len(coming_from_hist) > 0:
                        came_from_last = coming_from_hist[-1]
                    else:
                        came_from_last = None

                    authorised_mov = True

                    if case_type == PATH1:
                        if direction == TOP and came_from_last not in [LEFT, TOP, None]:
                            authorised_mov = False
                        elif direction == LEFT and came_from_last not in [TOP, LEFT, None]:
                            authorised_mov = False
                        elif direction == BOTTOM and came_from_last not in [RIGHT, BOTTOM, None]:
                            authorised_mov = False
                        elif direction == RIGHT and came_from_last not in [BOTTOM, RIGHT, None]:
                            authorised_mov = False

                    elif case_type == PATH2:
                        if direction == TOP and came_from_last not in [RIGHT, TOP, None]:
                            authorised_mov = False
                        elif direction == RIGHT and came_from_last not in [TOP, RIGHT, None]:
                            authorised_mov = False
                        elif direction == BOTTOM and came_from_last not in [LEFT, BOTTOM, None]:
                            authorised_mov = False
                        elif direction == LEFT and came_from_last not in [BOTTOM, LEFT, None]:
                            authorised_mov = False

                    elif case_type == WUMPUS or case_type == SLIMEPIT:
                        authorised_mov = False
                    
                    if authorised_mov :
                        coming_from_hist.append(coming_from)
                        if len(coming_from_hist) > 2:
                            coming_from_hist.pop(0)
                        vision_maze[y][x] = 1
                        vision_maze[new_y][new_x] = 2
                        if maze[new_y][new_x] == WUMPUS or maze[new_y][new_x] == SLIMEPIT:
                            for row in range(len(vision_maze)):
                                for col in range(len(vision_maze[0])):
                                    if vision_maze[row][col] != 2:
                                        vision_maze[row][col] = 1
                    
                    return vision_maze
    return vision_maze

def player_bats_interaction(maze, vision_maze, bats, x, y):
    player_moved = False
    if bats[y][x] > 1:
        player_moved = True
        #déplacer le joueur
        vision_maze[y][x] = 1 #enleve le joueur de la ou il est
        new_spot = starting_point(maze)
        vision_maze[new_spot[1]][new_spot[0]] = 2 #replace le joueur
        #déplacer la chauve-souris
        bats[y][x] = 0
        changed = False
        while not changed:
            new_x = randint(0,7)
            new_y = randint(0,5)
            if bats[new_y][new_x] == 0:
                changed = True
                bats[new_y][new_x] = 1
    else:
        if bats[y][x] != 0:
            bats[y][x] += 1

    return player_moved

def is_in_corridor(maze, vision_maze):
    for y in range(len(vision_maze)):
        for x in range(len(vision_maze[0])):
            if vision_maze[y][x] == 2: 
                case_type = maze[y][x]
                if case_type == PATH1 or case_type == PATH2:
                    return True
                return False
    return False

def get_next_corridor_direction(maze, vision_maze, coming_from_hist):
    player_x, player_y = -1, -1
    for y in range(len(vision_maze)):
        for x in range(len(vision_maze[0])):
            if vision_maze[y][x] == 2:
                player_x, player_y = x, y
                break

    if player_x == -1:
        return NONE

    case_type = maze[player_y][player_x]
    
    came_from = None
    if len(coming_from_hist) > 0:
        came_from = coming_from_hist[-1]

    if case_type == PATH1: 
        if came_from == LEFT: return TOP
        if came_from == TOP: return LEFT
        if came_from == RIGHT: return BOTTOM
        if came_from == BOTTOM: return RIGHT

    elif case_type == PATH2: 
        if came_from == LEFT: return BOTTOM
        if came_from == BOTTOM: return LEFT
        if came_from == RIGHT: return TOP
        if came_from == TOP: return RIGHT
    return NONE

def get_arrow_outcome(maze, vision_maze, direction):
# True = victoire, False = defaite
    if not direction == NONE:
        for y in range(len(vision_maze)):
            for x in range(len(vision_maze[0])):
                if vision_maze[y][x] == 2:
                    #on part de la position du joueur
                    #on determine la prochaine case
                    outcome_case = get_final_arrow_slot(maze, direction, x, y)
                    
                    return outcome_case == WUMPUS
    return False


def get_final_arrow_slot(maze, direction, x, y):
    if direction == TOP: 
        coming_from = BOTTOM
        y = (y-1) % len(maze)
    elif direction == BOTTOM: 
        coming_from = TOP
        y = (y+1) % len(maze)
    elif direction == LEFT: 
        coming_from = RIGHT
        x = (x-1) % len(maze[0])
    elif direction == RIGHT: 
        coming_from = LEFT
        x = (x+1) % len(maze[0])
    case_type = maze[y][x]

    while( case_type == PATH1 or case_type == PATH2):
        x, y, coming_from = handle_path(maze, case_type, coming_from, x, y)
        case_type = maze[y][x]
    
    return case_type

    

def handle_path(maze, case_type, coming_from, x, y):
    # return next x and y coordonates and next coming from
    if case_type == PATH1:
        if coming_from == LEFT:
            next_y = (y - 1) % len(maze)
            next_x = x
            next_coming_from = BOTTOM
        elif coming_from == TOP:
            next_x = (x - 1) % len(maze[0])
            next_y = y
            next_coming_from = RIGHT
        elif coming_from == RIGHT:
            next_y = (y + 1) % len(maze)
            next_x = x
            next_coming_from = TOP
        elif coming_from == BOTTOM:
            next_x = (x + 1) % len(maze[0])
            next_y = y
            next_coming_from = LEFT

    elif case_type == PATH2:
        if coming_from == LEFT:
            next_y = (y + 1) % len(maze)
            next_x = x
            next_coming_from = TOP
        elif coming_from == TOP:
            next_x = (x + 1) % len(maze[0])
            next_y = y
            next_coming_from = LEFT
        elif coming_from == RIGHT:
            next_y = (y - 1) % len(maze)
            next_x = x
            next_coming_from = BOTTOM
        elif coming_from == BOTTOM:
            next_x = (x - 1) % len(maze[0])
            next_y = y
            next_coming_from = RIGHT

    return(next_x, next_y, next_coming_from)