from flask import Flask, render_template 
from wumpus_engine import mazeGeneration

app = Flask(__name__)

@app.route('/')
def login():
    return render_template("index.html")

@app.route('/podiumScreen')
def podiumScreen():
    return render_template('podiumScreen.html')

@app.route('/gameScreen')
def gameScreen():
    maze = mazeGeneration.generateMaze(1)
    vision_maze = [[0 for _ in range(8)] for _ in range(6)]
    spawnpoint = mazeGeneration.starting_point(maze)
    vision_maze[spawnpoint[1]][spawnpoint[0]] = 2

    return render_template('gameScreen.html', maze=maze, vision_maze=vision_maze)

if __name__ == '__main__':
    app.run(debug=True)