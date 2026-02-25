from flask import Flask, render_template 
from wumpus_engine import mazeGeneration

maze = mazeGeneration.generateMaze(1)
vision_maze = [[0 for _ in range(8)] for _ in range(6)]
coming_from_hist = []

app = Flask(__name__)

@app.route('/')
def login():
    return render_template("index.html")

@app.route('/podiumScreen')
def podiumScreen():
    return render_template('podiumScreen.html')

@app.route('/gameScreen')
def gameScreen():
    global vision_maze, coming_from_hist

    vision_maze = [[0 for _ in range(8)] for _ in range(6)]
    coming_from_hist = []

    spawnpoint = mazeGeneration.starting_point(maze)
    vision_maze[spawnpoint[1]][spawnpoint[0]] = 2

    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze)

TOP = 99
BOTTOM = 98
LEFT = 97
RIGHT = 96

@app.route('/move/up')
def moveUp():
    global vision_maze
    vision_maze = mazeGeneration.move(maze, vision_maze, TOP, coming_from_hist)
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze)

@app.route('/move/down')
def moveDown():
    global vision_maze
    vision_maze = mazeGeneration.move(maze, vision_maze, BOTTOM, coming_from_hist)
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze)

@app.route('/move/left')
def moveLeft():
    global vision_maze
    vision_maze = mazeGeneration.move(maze, vision_maze, LEFT, coming_from_hist)
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze)

@app.route('/move/right')
def moveRight():
    global vision_maze
    vision_maze = mazeGeneration.move(maze, vision_maze, RIGHT, coming_from_hist)
    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze)

if __name__ == '__main__':
    app.run(debug=True)