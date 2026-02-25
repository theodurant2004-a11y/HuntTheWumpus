from flask import Flask, render_template 
from wumpus_engine import mazeGeneration

TOP = 99
BOTTOM = 98
LEFT = 97
RIGHT = 96
DIFFICULTY = 2

maze = []
vision_maze = []
coming_from_hist = []
bats_maze = []

app = Flask(__name__)

@app.route('/')
def login():
    return render_template("index.html")

@app.route('/podiumScreen')
def podiumScreen():
    return render_template('podiumScreen.html')

@app.route('/gameScreen')
def gameScreen():
    global vision_maze, coming_from_hist, maze, bats_maze

    maze = mazeGeneration.generateMaze(DIFFICULTY)
    vision_maze = [[0 for _ in range(8)] for _ in range(6)]
    coming_from_hist = []
    bats_maze = mazeGeneration.generateBats(DIFFICULTY)

    spawnpoint = mazeGeneration.starting_point(maze)
    vision_maze[spawnpoint[1]][spawnpoint[0]] = 2

    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)

@app.route('/move/up')# si fin de partie afficher tout le labyrinthe
def moveUp():
    global vision_maze
    vision_maze = mazeGeneration.move(maze, vision_maze, TOP, coming_from_hist)
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)

@app.route('/move/down')
def moveDown():
    global vision_maze
    vision_maze = mazeGeneration.move(maze, vision_maze, BOTTOM, coming_from_hist)
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)

@app.route('/move/left')
def moveLeft():
    global vision_maze
    vision_maze = mazeGeneration.move(maze, vision_maze, LEFT, coming_from_hist)
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)

@app.route('/move/right')
def moveRight():
    global vision_maze
    vision_maze = mazeGeneration.move(maze, vision_maze, RIGHT, coming_from_hist)
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze, bats=bats_maze)

if __name__ == '__main__':
    app.run(debug=True)