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
    return render_template('gameScreen.html', maze=maze)

if __name__ == '__main__':
    app.run(debug=True)